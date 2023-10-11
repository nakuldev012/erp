from django.urls import path
from .views import CountryAPIView, GetStateAPIView, GetCityAPIView

urlpatterns = [
    path("v1/country/", CountryAPIView.as_view()),
    path("v1/get-state-via-country/<int:pk>/", GetStateAPIView.as_view()),
    path("v1/get-city-via-state/<int:pk>/", GetCityAPIView.as_view()),
    
    ]
