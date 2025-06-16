import logging
from django.core.management.base import BaseCommand
from esdbclient import RecordedEvent

from tanda_backend.common.eventstore import get_event_store_client, deserialize

from django.conf import settings

from tanda_backend.merchant.models import Provider, Merchant

logger = logging.getLogger(__name__)


def _provider_created_event(event: RecordedEvent) -> None:
    data = deserialize(event.data)

    provider, _ = Provider.objects.update_or_create(
        public_id=data["public_id"],
        defaults={
            "name": data["name"],
            "is_active": data["is_active"],
        },
    )

    Merchant.objects.get_or_create(
        provider_id=provider.id,
        defaults={
            "name": data["name"],
        }
    )


handlers = {
    "ProviderCreated": _provider_created_event,
    "ProviderUpdated": _provider_created_event
}


class Command(BaseCommand):
    help = "Run cutting service consumer."

    def handle(self, *args, **options) -> None:
        client = get_event_store_client(uri=settings.BOOSTER_ESDB_URI)
        catchup_subscription = client.subscribe_to_all(
            filter_include=[r"providers-.*",],
            filter_by_stream_name=True,
        )
        for event in catchup_subscription:
            try:
                handlers[event.type](event)
            except KeyError:
                pass
