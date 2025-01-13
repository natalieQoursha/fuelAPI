from rest_framework import serializers
from .models import Routing

class RoutingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Routing
        fields='__all__'

        