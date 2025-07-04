from __future__ import annotations

from django.db import transaction
from django.utils.text import slugify

from tanda_backend.products.models import Product
from tanda_backend.products.services.external_product_service import ExternalProductUpdateRequest
from tanda_backend.products.services.external_product_service import update_external_product


def update_product(
    product_id: int,
    *,
    title: str | None = None,
    description: str | None = None,
    category_id: int | None = None,
    brand: str | None = None,
) -> Product:
    """Update product and propagate changes to the external service."""
    with transaction.atomic():
        product = Product.objects.select_for_update().get(id=product_id)

        if title is not None:
            product.title = title
            product.slug = slugify(title)
        if description is not None:
            product.description = description
        if category_id is not None:
            product.category_id = category_id
        if brand is not None:
            product.brand = brand

        product.save()

        external_request = ExternalProductUpdateRequest(
            title=title,
            description=description,
            brand=brand,
            category_public_id=str(product.category.public_id)
            if category_id is not None and product.category
            else None,
        )
        update_external_product(product.stock_id, external_request)

    return product
