from django.urls import path
from .views import CreatePaymentView, FinikWebhookView, PaymentDetailView

urlpatterns = [
    path('', CreatePaymentView.as_view(), name='create_payment'),
    path('webhook/', FinikWebhookView.as_view(), name='finik_webhook'),
    path('<str:order_id>/', PaymentDetailView.as_view(), name='payment_detail'),
]
