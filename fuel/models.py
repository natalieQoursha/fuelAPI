from django.db import models
import uuid

class Fuel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    OPISTruckstopID = models.IntegerField()
    TruckstopName = models.CharField(max_length=255)
    Address = models.CharField(max_length=255)
    City = models.CharField(max_length=255)
    State = models.CharField(max_length=255)
    RackID = models.IntegerField()
    RetailPrice = models.DecimalField(max_digits=10, decimal_places=5)

    latitude = models.FloatField(null=True, blank=True)  
    longitude = models.FloatField(null=True, blank=True)  
