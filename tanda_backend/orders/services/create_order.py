from collections import defaultdict
from typing import Iterable, List

from tanda_backend.orders.models import PaymentType, DeliveryType, Order, OrderItem
from tanda_backend.products.models import ProductVariant
from tanda_backend.users.models import User


def create_orders(
    user: User,
    full_name: str,
    phone_number: str,
    payment_type: PaymentType,
    city: str,
    address: str,
    delivery_type: DeliveryType,
    comments: str,
    variants: Iterable,
) -> List[Order]:
    variant_groups: dict[int, list[tuple[ProductVariant, int]]] = defaultdict(list)

    for variant in variants:
        product_variant = ProductVariant.objects.get(id=variant.variant_id)
        merchant_id = product_variant.product.merchant_id
        variant_groups[merchant_id].append((product_variant, variant.quantity))

    if not variant_groups:
        raise ValueError("Cannot create an order with no products")

    created_orders: list[Order] = []

    for merchant_id, items in variant_groups.items():
        order = Order.objects.create(
            user=user,
            full_name=full_name,
            phone_number=phone_number,
            payment_type=payment_type,
            city=city,
            address=address,
            delivery_type=delivery_type,
            comments=comments,
            merchant_id=merchant_id,
        )

        for product_variant, quantity in items:
            OrderItem.objects.create(
                order=order,
                variant=product_variant,
                quantity=quantity,
                selling_price=product_variant.selling_price,
            )

        created_orders.append(order)

    return created_orders
