from django.db import models


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидается'),
        ('succeeded', 'Успешно'),
        ('failed', 'Ошибка'),
    ]

    order_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    qr_url = models.URLField(blank=True, null=True)
    qr_image = models.URLField(blank=True, null=True)
    finik_item_id = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order_id} ({self.status})"
