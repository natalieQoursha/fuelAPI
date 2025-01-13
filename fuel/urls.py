from django.urls import path
from .views import FuelViews

urlpatterns=[
    path('fuels/',FuelViews.as_view(),name='fuel')
]