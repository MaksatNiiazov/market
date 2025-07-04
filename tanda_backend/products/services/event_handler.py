from esdbclient import RecordedEvent
from django.db import models

from tanda_backend.common.eventstore import deserialize


from tanda_backend.merchant.models import Provider, Merchant
from tanda_backend.orders.models import Order, OrderStatus, OrderItem
from tanda_backend.products.models import OptionType, Product, OptionValue, ProductVariant, VariantOption, Category
from tanda_backend.products.services.external_product_service import SourceService
from tanda_backend.orders.services.order_events import send_order_status_changed_event


def _handle_new_variant_event(event: RecordedEvent):
    data = deserialize(event.data)

    if data.get("source_service") == SourceService.TANDA:
        return

    product = Product.objects.get(
        stock_id=data["product_id"],
    )

    variant, is_created = ProductVariant.objects.get_or_create(
        stock_id=data["variant_id"],
        defaults={
            "product": product,
            "article": data["provider_sku"],
            "available_quantity": 0,
            "cost_price": data["cost_price"] or 0,
            "selling_price": data["price"] or 0,
            "images": data["photos"],
            "provider_sku": data["provider_sku"],
            "sku": data["sku"],
            "barcode": data["barcode"],
            "source_service": data.get("source_service") or "",
        }
    )

    if is_created:
        for option_data in data.get("variant_options", []):
            option_type, _ = OptionType.objects.get_or_create(
                public_id=option_data["option_type"]["id"],
                defaults={
                    "name": option_data["option_type"]["name"],
                    "code": option_data["option_type"]["code"],
                }
            )

            option_value, _ = OptionValue.objects.get_or_create(
                public_id=option_data["option_value"]["id"],
                defaults={
                    "option_type": option_type,
                    "value": option_data["option_value"]["value"],
                    "meta_data": option_data["option_value"]["value_metadata"],
                }
            )

            VariantOption.objects.get_or_create(
                product_variant=variant,
                option_value=option_value,
            )


def _handle_new_product_event(event: RecordedEvent):
    data = deserialize(event.data)

    if data.get("source_service") == SourceService.TANDA:
        return

    provider = Provider.objects.get(
        public_id=data["provider_id"],
    )
    merchant = Merchant.objects.get(
        provider=provider
    )

    group_by_option, _ = OptionType.objects.get_or_create(
        public_id=data["group_by_option"]["id"],
        defaults={
            "name": data["group_by_option"]["name"],
            "code": data["group_by_option"]["code"],
        }
    )
    category = Category.objects.get(
        public_id=data["category_id"],
    )

    Product.objects.get_or_create(
        stock_id=data["product_id"],
        defaults={
            "merchant": merchant,
            "provider": provider,
            "group_by_option_id": group_by_option,
            "title": data["title"],
            "description": data["description"] or "",
            "category": category,
            "brand": data["brand"] or "",
            "selling_price": data["base_price"] or 0,
            "slug": data["slug"],
            "images": data["product_photos"],
            "source_service": data.get("source_service") or "",
        }
    )


def _handle_shipment_done_event(event: RecordedEvent):
    data = deserialize(event.data)

    tanda_order_id = data.get("tanda_order_id")
    if not tanda_order_id:
        return

    order = Order.objects.filter(public_id=tanda_order_id).select_for_update().first()
    order_items = OrderItem.objects.filter(order=order).select_for_update()

    for item in data.get("items", []):
        variant_id = item.get("variant_id")
        quantity = item.get("quantity", 0)

        order_item = order_items.get(variant__stock_id=variant_id)
        order_item.shipped_quantity += quantity
        order_item.save(update_fields=['shipped_quantity'])

    if order.order_items.filter(shipped_quantity__lt=models.F('quantity')).exists():
        return

    if order.status == OrderStatus.READY_TO_SHIPMENT:
        previous_status = order.status
        order.status = OrderStatus.IN_WAY
        order.save(update_fields=['status'])

        send_order_status_changed_event(order=order, previous_status=previous_status)


handlers = {
    "ProductCreatedInStock": _handle_new_product_event,
    "ProductVariantCreatedInStock": _handle_new_variant_event,
    "ShipmentDone": _handle_shipment_done_event
}
