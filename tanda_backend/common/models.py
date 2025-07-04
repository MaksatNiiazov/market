import uuid

from django.db import models


class PublicModel(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, unique=True)

    class Meta:
        abstract = True
