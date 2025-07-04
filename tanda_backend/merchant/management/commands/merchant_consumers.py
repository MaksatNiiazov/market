import logging

from django.core.management.base import BaseCommand
from django.db import transaction
from esdbclient.exceptions import AlreadyExists
from django.conf import settings

from tanda_backend.common.eventstore import get_event_store_client
from tanda_backend.merchant.services.event_handler import event_handler_map

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Run cutting service consumer."

    def handle(self, *args, **options) -> None:
        client = get_event_store_client(uri=settings.BOOSTER_ESDB_URI)
        group_name = "tanda-merchant-consumer"
        try:
            client.create_subscription_to_all(
                group_name=group_name,
                from_end=True,
            )
        except AlreadyExists:
            pass

        subscription = client.read_subscription_to_all(
            group_name=group_name,
        )
        for event in subscription:
            logger.info("Received event: %s", event.type)
            with transaction.atomic():
                sid = transaction.savepoint()
                try:
                    if event.type in event_handler_map:
                        event_handler_map[event.type](event)
                except Exception:
                    logger.exception("Error processing event: %s", event.type)
                    transaction.savepoint_rollback(sid)
                    if event.retry_count < 5:
                        action = "retry"
                    else:
                        action = "park"

                    subscription.nack(event, action)
                else:
                    logger.info("Successfully done: %s", event.type)
                    subscription.ack(event)
