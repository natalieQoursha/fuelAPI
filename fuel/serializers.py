from rest_framework import serializers
from .models import Fuel

class FuelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Fuel
        fields='__all__'

        