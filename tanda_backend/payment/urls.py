from django.urls import path
from .views import CreatePaymentView, FinikWebhookView

urlpatterns = [
    path('', CreatePaymentView.as_view(), name='create_payment'),
    path('webhook/', FinikWebhookView.as_view(), name='finik_webhook'),
]
