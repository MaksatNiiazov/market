from tanda_backend.orders.models import PaymentType, DeliveryType, Order, OrderItem
from tanda_backend.products.models import ProductVariant
from tanda_backend.users.models import User


def create_order(
    user: User,
    full_name: str,
    phone_number: str,
    payment_type: PaymentType,
    city: str,
    address: str,
    delivery_type: DeliveryType,
    comments: str,
    variants,
):
    product_variants = []
    merchant_ids = set()

    for variant in variants:
        product_variant = ProductVariant.objects.get(id=variant.variant_id)
        product_variants.append((product_variant, variant.quantity))

        if product_variant.product.merchant_id:
            merchant_ids.add(product_variant.product.merchant_id)

    if len(merchant_ids) > 1:
        raise ValueError("Cannot create an order with products from different merchants")

    if len(merchant_ids) == 0:
        raise ValueError("Cannot create an order with no products")

    order = Order.objects.create(
        user=user,
        full_name=full_name,
        phone_number=phone_number,
        payment_type=payment_type,
        city=city,
        address=address,
        delivery_type=delivery_type,
        comments=comments,
        merchant_id=merchant_ids.pop(),
    )

    for product_variant, quantity in product_variants:
        OrderItem.objects.create(
            order=order,
            variant=product_variant,
            quantity=quantity,
            selling_price=product_variant.selling_price,
        )

    return order
