from decimal import Decimal

from rest_framework import serializers

from payments.models import SubscriptionPlan


class MomoPaymentInitSerializer(serializers.Serializer):
    plan_id = serializers.UUIDField(required=False)
    amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal("0.01"),
        required=False,
    )
    description = serializers.CharField(max_length=255, required=False, allow_blank=True)

    def validate(self, attrs):
        plan_id = attrs.get("plan_id")
        amount = attrs.get("amount")
        if not plan_id and amount is None:
            raise serializers.ValidationError("Either plan_id or amount is required.")
        if plan_id and amount is not None:
            raise serializers.ValidationError("Provide either plan_id or amount, not both.")

        if plan_id:
            try:
                plan = SubscriptionPlan.objects.get(id=plan_id)
            except SubscriptionPlan.DoesNotExist as exc:
                raise serializers.ValidationError({"plan_id": "Subscription plan not found."}) from exc
            attrs["plan"] = plan
            attrs["amount"] = plan.price
            if not attrs.get("description"):
                attrs["description"] = f"Thanh toán gói {plan.name}"
        else:
            attrs["plan"] = None
            if not attrs.get("description"):
                attrs["description"] = "Thanh toán MoMo"

        return attrs


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ("id", "name", "price", "duration_days", "features")
