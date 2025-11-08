from django.urls import path

from payments.api.views import MoMoPaymentInitView, MoMoIPNView, SubscriptionPlanListView

app_name = "payments"

urlpatterns = [
    path("plans/", SubscriptionPlanListView.as_view(), name="plan-list"),
    path("momo/initiate/", MoMoPaymentInitView.as_view(), name="momo-init"),
    path("momo/ipn/", MoMoIPNView.as_view(), name="momo-ipn"),
]
