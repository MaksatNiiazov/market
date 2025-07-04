import logging
from django.core.management.base import BaseCommand
from esdbclient import RecordedEvent

from tanda_backend.common.eventstore import get_event_store_client, deserialize

from django.conf import settings

from tanda_backend.merchant.models import Provider, Merchant
from tanda_backend.products.models import OptionType, Product, OptionValue, ProductVariant, VariantOption, Category

logger = logging.getLogger(__name__)


def _handle_new_variant_event(event: RecordedEvent):
    data = deserialize(event.data)

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
            "source_service": "sew_booster",
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
    provider = Provider.objects.get(
        public_id=data["provider_id"],
    )
    merchant = Merchant.objects.filter(
        provider=provider
    ).first()

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
            "source_service": "sew_booster",
        }
    )


handlers = {
    "ProductCreatedInStock": _handle_new_product_event,
    "ProductVariantCreatedInStock": _handle_new_variant_event
}


class Command(BaseCommand):
    help = "Run cutting service consumer."

    def handle(self, *args, **options) -> None:
        # Category.objects.all().delete()
        # OptionType.objects.all().delete()
        # OptionValue.objects.all().delete()
        # Provider.objects.create(
        #     name="Тестовый провайдер",
        #     public_id="78af3eb3-f501-4691-8958-e935bf151e96",
        # )
        # Category.objects.get_or_create(
        #     public_id="e56b9562-9886-463b-b04f-2d0e1e1be0cf",
        #     name="Одежда",
        # )
        Product.objects.all().delete()
        client = get_event_store_client(uri=settings.ESDB_URI)
        catchup_subscription = client.subscribe_to_all(
            filter_include=[r"products",],
            filter_by_stream_name=True,
        )
        for event in catchup_subscription:
                handler = handlers.get(event.type)
                if handler:
                    print(event.type)
                    handler(event)
