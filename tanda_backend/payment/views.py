import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Payment
from .services import create_finik_qr_payment, create_finik_card_payment


@method_decorator(csrf_exempt, name='dispatch')
class FinikWebhookView(APIView):
    def post(self, request):
        data = request.data
        item_id = data.get("id")
        status_result = data.get("status")

        payment = Payment.objects.filter(finik_item_id=item_id).first()
        if payment:
            if status_result == "SUCCEEDED":
                payment.status = "succeeded"
            elif status_result == "FAILED":
                payment.status = "failed"
            payment.save()

        return Response({"status": "ok"})


class CreatePaymentView(APIView):
    def post(self, request):
        order_id = request.data.get("order_id")
        amount = request.data.get("amount")
        name_en = request.data.get("name_en", f"Order {order_id}")
        method = request.data.get("method", "qr")

        if not order_id or not amount:
            return Response({"error": "order_id and amount are required"}, status=400)

        if Payment.objects.filter(order_id=order_id).exists():
            return Response({"error": "Payment with this order_id already exists"}, status=400)

        payment = Payment.objects.create(order_id=order_id, amount=amount)

        try:
            if method == "qr":
                result = create_finik_qr_payment(order_id, amount, name_en)
                payment.finik_item_id = result["item_id"]
                payment.qr_url = result["qr_url"]
                payment.qr_image = result["qr_image"]
                payment.save()
            elif method == "card":
                result = create_finik_card_payment(order_id, amount, name_en)
                payment.finik_item_id = result["item_id"]
                payment.qr_url = result["qr_url"]
                payment.save()
            else:
                return Response({"error": "Invalid method"}, status=400)

        except requests.HTTPError as e:
            error_response = e.response
            return Response({
                "error": f"Finik HTTP {error_response.status_code}: {error_response.text}"
            }, status=error_response.status_code)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

        return Response({
            "order_id": payment.order_id,
            "amount": payment.amount,
            "qr_url": payment.qr_url,
            "qr_image": payment.qr_image,
            "finik_item_id": payment.finik_item_id,
        })
