from esdbclient import RecordedEvent

from tanda_backend.common.eventstore import deserialize
from tanda_backend.merchant.models import Merchant, Provider


def _provider_created_event(event: RecordedEvent) -> None:
    data = deserialize(event.data)

    provider, _ = Provider.objects.update_or_create(
        public_id=data["public_id"],
        defaults={
            "name": data["name"],
            "is_active": data["is_active"],
        },
    )

    if data.get("merchant_id"):
        merchant = Merchant.objects.get(
            public_id=data["merchant_id"],
        )
        merchant.provider = provider
        merchant.save()


event_handler_map = {
    "ProviderCreated": _provider_created_event,
    "ProviderUpdated": _provider_created_event,
}
