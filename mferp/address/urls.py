from django.urls import path
from .views import CountryAPIView, GetStateAPIView, GetCityAPIView

urlpatterns = [
    path("v1/country/", CountryAPIView.as_view()),
    path("v1/get-state-via-country/", GetStateAPIView.as_view()),
    path("v1/get-city-via-state/", GetCityAPIView.as_view()),
    
    ]
