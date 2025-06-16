import json

from django.conf import settings
from esdbclient import EventStoreDBClient, NewEvent, StreamState


def get_event_store_client(uri: str = settings.ESDB_URI) -> EventStoreDBClient:
    return EventStoreDBClient(
        uri=uri,
    )


def append_to_stream(events: NewEvent | list[NewEvent], stream_name: str):
    client = get_event_store_client()

    client.append_to_stream(
        stream_name,
        current_version=StreamState.ANY,
        events=events,
    )
    client.close()


def serialize(d):
    return json.dumps(d).encode("utf8")


def deserialize(s):
    return json.loads(s.decode("utf8"))
