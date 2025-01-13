from django.conf import settings
import requests
from math import radians, cos, sin, asin, sqrt
from fuel.models import Fuel
from fuel.serializers import FuelSerializer

class RouteService:
    def calculate_route_and_fuel_stops(self, waypoints):
        total_route_distance = 0
        fuel_stations = []
        total_fuel_cost = 0  
        start_point = waypoints[0]
        fuel_stations_list = self.fuel_service(start_point[0], start_point[1])
        fuel_stations.extend(fuel_stations_list)

        for station in fuel_stations_list:
            fuel_price = float(station.get("RetailPrice", 0))  
            fuel_needed = 500 / 10  
            total_fuel_cost += fuel_needed * fuel_price  

        for i in range(1, len(waypoints)):
            start_point = waypoints[i - 1]
            end_point = waypoints[i]
            segment_distance = self.calculate_distance_haversine(start_point[1], start_point[0], end_point[1], end_point[0])

            if total_route_distance + segment_distance >= 500:
                fuel_stations_list = self.fuel_service(start_point[0], start_point[1])
                fuel_stations.extend(fuel_stations_list)

                for station in fuel_stations_list:
                    fuel_price = float(station.get("RetailPrice", 0))  
                    fuel_needed = total_route_distance / 10  
                    total_fuel_cost += fuel_needed * fuel_price  

                total_route_distance = 0  

            total_route_distance += segment_distance

        return {
            "fuel_stations": fuel_stations,
            "total_fuel_cost": total_fuel_cost,  
        }

    def fuel_service(self, lat, lng, radius=5000):
        places_url = (f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
                      f"?location={lat},{lng}"
                      f"&radius={radius}"
                      f"&type=gas_station"
                      f"&key={settings.GOOGLE_API_KEY}")

        response = requests.get(places_url)
        data = response.json()
        api_gas_stations = []
        if data['status'] == "OK":
            api_gas_stations = [{
                "name": place['name'],
                "address": place['vicinity'],
                "latitude": place['geometry']['location']['lat'],
                "longitude": place['geometry']['location']['lng']
            } for place in data['results']]

        if not api_gas_stations:
            return {"error": "No gas stations found in the area"}

        db_fuel_stations = Fuel.objects.filter(
            TruckstopName__in=[station['name'] for station in api_gas_stations]
        )

        if db_fuel_stations.exists():
            for station in db_fuel_stations:
                corresponding_station = next(
                    (api_station for api_station in api_gas_stations if api_station['name'] == station.TruckstopName),
                    None
                )
                if corresponding_station:
                    station.latitude = corresponding_station['latitude']
                    station.longitude = corresponding_station['longitude']

            sorted_stations = sorted(db_fuel_stations, key=lambda x: float(x.RetailPrice))
            cheapest_station = sorted_stations[0]  
            serializer = FuelSerializer([cheapest_station], many=True)
            return serializer.data

        return {"error": "No matching fuel stations found in the database"}

    def find_route(self, start_location, finish_location):
        directions_url = f"https://maps.googleapis.com/maps/api/directions/json?origin={start_location}&destination={finish_location}&key={settings.GOOGLE_API_KEY}"
        response = requests.get(directions_url)
        data = response.json()

        if data['status'] == 'OK':
            route = data['routes'][0]['legs'][0]  # first route is the most optimal one
            total_distance = route['distance']['text']
            steps = route['steps']

            waypoints = [
                (step['end_location']['lat'], step['end_location']['lng'])
                for step in steps
            ]

            fuel_stations_data = self.calculate_route_and_fuel_stops(waypoints)
            fuel_stations = fuel_stations_data.get('fuel_stations', [])
            total_fuel_cost = fuel_stations_data.get('total_fuel_cost', 0)
            map_url = self.generate_map_url(start_location, finish_location, waypoints, fuel_stations)

            return {
                "total_distance": total_distance,
                "total_fuel_cost": total_fuel_cost,
                "fuel_stations": fuel_stations,
                "map": map_url,
            }
        
    def generate_map_url(self, start_location, finish_location, waypoints, fuel_stations):
        map_url = f"https://maps.googleapis.com/maps/api/staticmap?origin={start_location}&destination={finish_location}&size=800x600&key={settings.GOOGLE_API_KEY}"
        
        path_points = [start_location] + [f"{lat},{lng}" for lat, lng in waypoints] + [finish_location]
        path = "|".join(path_points)
        map_url += f"&path=color:0x0000ff|weight:5|{path}"  
        finish_lat, finish_lng = finish_location.split(",")
        label = 'Finish'  
        map_url += f"&markers=label:{label}|{finish_lat},{finish_lng}"

        if isinstance(fuel_stations, list) and all(isinstance(station, dict) for station in fuel_stations):
            for station in fuel_stations:
                try:
                    lat = station['latitude']
                    lng = station['longitude']
                    label = 'G'  
                    map_url += f"&markers=label:{label}|{lat},{lng}"
                except KeyError as e:
                    print(f"Error: Missing key {e} in fuel station data: {station}")
        else:
            print("Fuel Stations Data:", fuel_stations)
            print("Error: fuel_stations data is not in the expected format. Expected a list of dictionaries.")
        
        return map_url
    
    def calculate_distance_haversine(self, lng1, lat1, lng2, lat2):
        lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])

        dlng = lng2 - lng1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 3956 
        return c * r
    

    



