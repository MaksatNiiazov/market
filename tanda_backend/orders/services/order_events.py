from esdbclient import NewEvent

from tanda_backend.common.eventstore import serialize, append_to_stream
from tanda_backend.orders.models import Order, OrderStatus


def send_order_status_changed_event(order: Order, previous_status: OrderStatus) -> None:
    """Send event to eventstore when order status is changed."""
    data = {
        "public_id": str(order.public_id),
        "previous_status": previous_status,
        "status": order.status,
        "merchant_id": str(order.merchant.public_id),
        "user_id": str(order.user.sso_id),
        "payment_type": order.payment_type,
        "delivery_type": order.delivery_type,
        "created_at": order.created_at.isoformat(),
        "provider_id": str(order.merchant.provider.public_id),
        "city": order.city,
        "address": order.address,
        "full_name": order.full_name,
        "phone_number": order.phone_number,
        "comments": order.comments,
        "items": [
            {
                "variant_id": str(item.variant.stock_id),
                "quantity": item.quantity,
                "selling_price": str(item.selling_price),
            } for item in order.order_items.all()
        ]
    }

    event = NewEvent(
        type="OrderStatusChanged",
        data=serialize(data),
    )
    stream_name = f"tanda-orders-{order.public_id}"
    append_to_stream(event, stream_name)
