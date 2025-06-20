from decimal import Decimal
from typing import Optional, Iterable
from urllib.parse import urlparse

from django.db import transaction

from tanda_backend.products.models import (
    ProductVariant,
    VariantOption,
    OptionValue,
    Image,
)


def update_product_variant(
    variant_id: int,
    article: Optional[str] = None,
    cost_price: Optional[Decimal] = None,
    selling_price: Optional[Decimal] = None,
    option_value_ids: Optional[Iterable[int]] = None,
    image_id: Optional[int] = None,
) -> ProductVariant:
    """Update product variant fields and options."""
    variant = ProductVariant.objects.select_related("product__merchant").get(id=variant_id)

    update_fields = []

    if article is not None and article != variant.article:
        exists = ProductVariant.objects.filter(
            article=article,
            product__merchant=variant.product.merchant,
        ).exclude(id=variant.id).exists()
        if exists:
            raise ValueError("Article already exists for this merchant.")
        variant.article = article
        update_fields.append("article")

    if cost_price is not None:
        variant.cost_price = cost_price
        update_fields.append("cost_price")

    if selling_price is not None:
        variant.selling_price = selling_price
        update_fields.append("selling_price")

    if image_id is not None:
        image = Image.objects.get(id=image_id)
        variant.images = [urlparse(image.file.url).path.lstrip("/")]
        update_fields.append("images")

    with transaction.atomic():
        if update_fields:
            variant.save(update_fields=update_fields)

        if option_value_ids is not None:
            VariantOption.objects.filter(product_variant=variant).delete()
            for value_id in option_value_ids:
                if not OptionValue.objects.filter(id=value_id).exists():
                    raise ValueError(f"Value option with ID {value_id} does not exist.")
                VariantOption.objects.create(
                    product_variant=variant,
                    option_value_id=value_id,
                )

    return variant
