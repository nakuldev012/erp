from django.urls import path
from .views import EmployeeTypeUserAPIView, BasicEmployeeAPIView, PersonalEmployeeAPIView

urlpatterns = [
    path("v1/get-employee-type-user/", EmployeeTypeUserAPIView.as_view()),
    path("v1/basic-employee/", BasicEmployeeAPIView.as_view()),
    path("v1/basic-employee/<int:pk>/", BasicEmployeeAPIView.as_view()),
    path("v1/employee-personal-details/", PersonalEmployeeAPIView.as_view()),

    
    ]
