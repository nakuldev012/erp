from django.urls import path
from .views import EmployeeTypeUserAPIView

urlpatterns = [
    
    path("v1/type_of_employment/", EmployeeTypeUserAPIView.as_view()),
   
    ]

    