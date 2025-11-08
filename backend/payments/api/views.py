import base64
import json
from datetime import timedelta
from decimal import Decimal, ROUND_HALF_UP

from django.db import transaction
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from payments.api.serializers import MomoPaymentInitSerializer, SubscriptionPlanSerializer
from payments.models import Payment, UserSubscription, SubscriptionPlan
from payments.services.momo_client import MoMoAIOClient


class MoMoPaymentInitView(APIView):
    """Khởi tạo giao dịch MoMo từ FE."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = MomoPaymentInitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        plan = serializer.validated_data["plan"]
        amount = serializer.validated_data["amount"]
        description = serializer.validated_data["description"]
        flow = request.data.get("flow", "pay_with_method")
        payment_code = request.data.get("payment_code", "")

        payment = Payment.objects.create(
            user=request.user,
            plan=plan,
            amount=amount,
            status="pending",
            metadata={"gateway": "momo", "flow": flow},
        )

        order_id = payment.id.hex
        extra_payload = {
            "payment_id": str(payment.id),
            "user_id": str(request.user.id),
        }
        if plan:
            extra_payload["plan_id"] = str(plan.id)
        extra_data = base64.b64encode(json.dumps(extra_payload).encode("utf-8")).decode("utf-8")

        amount_vnd = int(amount.quantize(Decimal("1"), rounding=ROUND_HALF_UP))
        redirect_url = getattr(settings, "MOMO_REDIRECT_URL", None) or request.build_absolute_uri("/")
        ipn_url = getattr(settings, "MOMO_IPN_URL", None) or request.build_absolute_uri(reverse("payments:momo-ipn"))

        client = MoMoAIOClient()

        try:
            if flow == "pay_with_method":
                momo_response = client.create_pay_with_method(
                    amount=amount_vnd,
                    order_id=order_id,
                    order_info=description,
                    redirect_url=redirect_url,
                    ipn_url=ipn_url,
                    extra_data=extra_data,
                )
            elif flow == "pos":
                momo_response = client.create_pos_payment(
                    amount=amount_vnd,
                    order_id=order_id,
                    order_info=description,
                    payment_code=payment_code,
                    ipn_url=ipn_url,
                    extra_data=extra_data,
                )
            else:
                momo_response = client.create_payment(
                    amount=amount_vnd,
                    order_id=order_id,
                    order_info=description,
                    redirect_url=redirect_url,
                    ipn_url=ipn_url,
                    extra_data=extra_data,
                )
        except ValueError as exc:
            payment.status = "failed"
            payment.metadata["error"] = str(exc)
            payment.save(update_fields=["status", "metadata"])
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        updated_metadata = {
            **payment.metadata,
            "orderId": momo_response.get("orderId"),
            "requestId": momo_response.get("requestId"),
            "payUrl": momo_response.get("payUrl"),
        }
        payment.metadata = updated_metadata
        payment.save(update_fields=["metadata"])

        return Response(
            {
                "payment_id": str(payment.id),
                "payUrl": momo_response.get("payUrl"),
                "deeplink": momo_response.get("deeplink"),
                "qrCodeUrl": momo_response.get("qrCodeUrl"),
                "resultCode": momo_response.get("resultCode"),
                "message": momo_response.get("message"),
            }
        )


class MoMoIPNView(APIView):
    """Endpoint nhận thông báo thanh toán từ MoMo."""

    authentication_classes: list = []
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        client = MoMoAIOClient()

        if not client.verify_ipn(data):
            return Response({"message": "invalid signature"}, status=status.HTTP_400_BAD_REQUEST)

        order_id = data.get("orderId")
        if not order_id:
            return Response({"message": "orderId missing"}, status=status.HTTP_400_BAD_REQUEST)

        payment = Payment.objects.filter(metadata__orderId=order_id).first()
        if not payment:
            return Response({"message": "payment not found"}, status=status.HTTP_404_NOT_FOUND)

        payment.metadata = {**payment.metadata, "momo_ipn": data}
        result_code = data.get("resultCode")

        if result_code == 0:
            with transaction.atomic():
                payment.status = "paid"
                payment.transaction_id = data.get("transId")
                payment.paid_at = payment.paid_at or timezone.now()
                payment.save(update_fields=["status", "transaction_id", "paid_at", "metadata"])

                if payment.plan:
                    subscription, created = UserSubscription.objects.get_or_create(
                        user=payment.user,
                        plan=payment.plan,
                        defaults={
                            "start_date": timezone.now(),
                            "end_date": timezone.now() + timedelta(days=payment.plan.duration_days),
                            "active": True,
                            "payment": payment,
                        },
                    )
                    if not created:
                        base_date = max(subscription.end_date, timezone.now())
                        subscription.end_date = base_date + timedelta(days=payment.plan.duration_days)
                        subscription.active = True
                        subscription.payment = payment
                        subscription.save(update_fields=["end_date", "active", "payment"])
        else:
            payment.status = "failed"
            payment.save(update_fields=["status", "metadata"])

        return Response({"message": "success"}, status=status.HTTP_200_OK)


class SubscriptionPlanListView(generics.ListAPIView):
    """
    Public endpoint to expose active subscription plans for the frontend.
    """

    queryset = SubscriptionPlan.objects.all().order_by("price")
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.AllowAny]
