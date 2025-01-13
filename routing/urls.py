from django.urls import path
from .views import RoutingViews

urlpatterns=[
    path('routes/',RoutingViews.as_view(),name='route'),
    path('map/', RoutingViews.as_view(), name='map_view')
]