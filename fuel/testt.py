import os
import django

# Set up Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task.settings")  # Replace 'task' with your project name
django.setup()

# Now you can import your views
from fuel.views import FuelViews

# Create an instance of FuelViews and call the update method
fuel_view_instance = FuelViews()
fuel_view_instance.update_fuel_lat_lon()
