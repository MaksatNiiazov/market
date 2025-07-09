import time
import json
import requests
from authorizer import Signer
from urllib.parse import urlparse
from django.conf import settings


def _create_finik_payment(order_id, amount, name_en, card_type: str):
    """Send request to Finik acquiring service."""
    method = "POST"
    path = "/v1/payment"
    if getattr(settings, "FINIK_TEST", False):
        url = settings.FINIK_TEST_PAYMENT_URL
    else:
        url = settings.FINIK_PAYMENT_URL
    host = urlparse(url).netloc

    # Формируем тело запроса
    body = {
        "Amount": int(amount),
        "CardType": card_type,
        "Data": {
            "accountId": settings.FINIK_ACCOUNT_ID,
            "merchantCategoryCode": settings.FINIK_MCC_CODE,
            "name_en": name_en,
        },
        "PaymentId": order_id,
        "RedirectUrl": f"{settings.FINIK_CARD_REDIRECT_BASE}{order_id}",
    }

    # Сериализуем тело запроса
    payload = json.dumps(body, sort_keys=True, separators=(",", ":"))

    # Заголовки
    timestamp = str(int(time.time() * 1000))
    headers = {
        "Host": host,
        "x-api-key": settings.FINIK_API_KEY,
        "x-api-timestamp": timestamp,
    }

    # Создаём объект подписчика
    request_data = {
        "http_method": method,
        "path": path,
        "headers": headers,
        "body": body,
        "query_string_parameters": {},  # без query
    }

    signer = Signer(**request_data)

    # Подписываем
    with open(settings.FINIK_PRIVATE_KEY_PATH, "rb") as f:
        private_key = f.read()

    signature = signer.sign(private_key)

    # Финальные заголовки запроса
    request_headers = {
        "x-api-key": settings.FINIK_API_KEY,
        "x-api-timestamp": timestamp,
        "signature": signature,
        "Content-Type": "application/json",
    }

    # Отправляем POST-запрос
    response = requests.post(url, data=payload, headers=request_headers)

    try:
        response.raise_for_status()
        print("Ответ Finik:", response.text)

    except requests.HTTPError:
        print("Ответ Finik:", response.text)
        raise Exception("Finik REST error")

    # Безопасная обработка ответа
    if response.headers.get("Content-Type", "").startswith("application/json"):
        result = response.json()
        redirect_url = result.get("redirectUrl", "")
        item_id = result.get("id", order_id)
    else:
        # если это HTML, выдёргиваем redirect из самого URL (если можешь)
        redirect_url = response.url  # fallback
        item_id = order_id

    return {
        "item_id": item_id,
        "qr_url": redirect_url,
        "qr_image": "",
    }


def create_finik_qr_payment(order_id, amount, name_en):
    """Create Finik QR payment (production endpoint)."""
    return _create_finik_payment(order_id, amount, name_en, "FINIK_QR")


def create_finik_card_payment(order_id, amount, name_en):
    """Create Finik card payment (production endpoint)."""
    return _create_finik_payment(order_id, amount, name_en, "FINIK_CARD")
