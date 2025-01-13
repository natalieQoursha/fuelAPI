from .models import Fuel
from .serializers import FuelSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class FuelViews(APIView):
    
    def get(self, request):
        fuels = Fuel.objects.all()  # returns all data in fuel model, this is a queryset
        serializer = FuelSerializer(fuels, many=True)  # serialize the queryset into JSON
        return Response(serializer.data)  # return data as HTTP response 

    def post(self, request):
        serializer = FuelSerializer(data=request.data)  # accept incoming data as JSON format
        if serializer.is_valid():  # check if data is valid based on rules
            serializer.save()  # save the new data as a new object
            return Response(serializer.data, status=201)  # created 
        return Response(serializer.errors, status=400)  # bad request 


