from .serializers import RoutingSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from routing.services import RouteService  

class RoutingViews(APIView):
    def post(self, request):
        serializer = RoutingSerializer(data=request.data)     
        if serializer.is_valid():                        
            serializer.save()                             
            return Response(serializer.data, status=201)      
        return Response(serializer.errors, status=400)       

    def get(self, request):
        start_location = request.query_params.get('startLocation', None)
        finish_location = request.query_params.get('finishLocation', None)

        if not start_location or not finish_location:
            return Response({"error": "Start and finish locations are required."}, status=400)

        route_service = RouteService()
        route_data = route_service.find_route(start_location, finish_location)
        return Response(route_data, status=200)
    




    


    


