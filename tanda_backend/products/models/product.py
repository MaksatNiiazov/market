from django.contrib.postgres.fields.array import ArrayField
from django.db import models

from tanda_backend.common.models import PublicModel


class Product(PublicModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    images = ArrayField(models.CharField(max_length=255))
    slug = models.CharField(max_length=255)

    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)
    group_by_option_id = models.ForeignKey("OptionType", on_delete=models.SET_NULL, null=True)

    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    brand = models.CharField(max_length=255, default="")

    # unique identifier in the stock
    stock_id = models.CharField(max_length=255, unique=True)
    merchant = models.ForeignKey("merchant.Merchant", on_delete=models.SET_NULL, null=True)
    provider = models.ForeignKey("merchant.Provider", on_delete=models.SET_NULL, null=True)

    source_service = models.CharField(max_length=255, null=True)

    is_approved = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.title


class ProductVariant(PublicModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    article = models.CharField(max_length=500, null=True)

    # unique identifier in the stock
    stock_id = models.CharField(max_length=255, unique=True)
    images = ArrayField(models.CharField(max_length=255), null=True)
    available_quantity = models.PositiveIntegerField()
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    provider_sku = models.CharField(max_length=255, null=True)
    sku = models.CharField(max_length=255, null=True)
    barcode = models.CharField(max_length=255, null=True)
    source_service = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name = "Вариант товара"
        verbose_name_plural = "Варианты товаров"


class VariantOption(PublicModel):
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    option_value = models.ForeignKey("OptionValue", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Вариант опции"
