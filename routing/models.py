from django.db import models
import uuid

class Routing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    startLocation=models.CharField(max_length=255)
    finishLocation=models.CharField(max_length=255)


