import uuid
from django.db import models

class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)

    class Meta:
        abstract = True