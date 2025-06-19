from typing import Optional

from django.utils.text import slugify

from tanda_backend.products.models import Product


def update_product(
    product_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    brand: Optional[str] = None,
) -> Product:
    """Update product fields."""
    product = Product.objects.get(id=product_id)

    update_fields = []

    if title is not None:
        product.title = title
        product.slug = slugify(title)
        update_fields.extend(["title", "slug"])

    if description is not None:
        product.description = description
        update_fields.append("description")

    if brand is not None:
        product.brand = brand
        update_fields.append("brand")

    if update_fields:
        product.save(update_fields=update_fields)

    return product
