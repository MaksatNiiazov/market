from django.db import models

from tanda_backend.common.models import PublicModel


class PaymentType(models.TextChoices):
    CASH = "cash"


class DeliveryType(models.TextChoices):
    SELF_DELIVERY = "self_delivery"
    COURIER = "courier"


class OrderStatus(models.TextChoices):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    READY_TO_SHIPMENT = "ready_to_shipment"
    IN_WAY = "in_way"
    DELIVERED = "delivered"


class Order(PublicModel):

    stock_task_id = models.UUIDField(null=True)

    merchant = models.ForeignKey("merchant.Merchant", on_delete=models.CASCADE, null=True)

    payment_type = models.CharField(max_length=255, choices=PaymentType.choices, default=PaymentType.CASH)

    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    delivery_type = models.CharField(max_length=255, choices=DeliveryType.choices, default=DeliveryType.SELF_DELIVERY)
    comments = models.TextField(null=True, blank=True)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)

    status = models.CharField(max_length=255, choices=OrderStatus.choices, default=OrderStatus.NEW)

    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderItem(PublicModel):
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="order_items")
    variant = models.ForeignKey("products.ProductVariant", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipped_quantity = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Заказанный товар"
        verbose_name_plural = "Заказанные товары"
