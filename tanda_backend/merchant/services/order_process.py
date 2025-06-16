from tanda_backend.orders.models import Order, OrderStatus
from tanda_backend.orders.services.order_events import send_order_status_changed_event


def process_order(order: Order):
    current_status = order.status

    allowed_transitions = {
        OrderStatus.NEW: OrderStatus.IN_PROGRESS,
        OrderStatus.IN_PROGRESS: OrderStatus.READY_TO_SHIPMENT,
        OrderStatus.IN_WAY: OrderStatus.DELIVERED,
    }

    if current_status not in allowed_transitions:
        raise Exception(f"Does not allow to change status from '{current_status}'")

    next_status = allowed_transitions[current_status]

    # Store previous status for event
    order.status = next_status
    order.save(update_fields=['status'])

    send_order_status_changed_event(order=order, previous_status=current_status)
