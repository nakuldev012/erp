from django.urls import path
from .views import EmployeeTypeUserAPIView, BasicEmployeeAPIView, PersonalEmployeeAPIView, AccountEmployeeAPIView, AddressEmployeeAPIView

urlpatterns = [
    path("v1/get-employee-type-user/", EmployeeTypeUserAPIView.as_view()),
    path("v1/basic-employee/", BasicEmployeeAPIView.as_view()),
    path("v1/basic-employee/<int:pk>/", BasicEmployeeAPIView.as_view()),
    path("v1/employee-personal-details/", PersonalEmployeeAPIView.as_view()),
    path("v1/employee-personal-details/<int:pk>/", PersonalEmployeeAPIView.as_view()),
    path("v1/employee-account-details/", AccountEmployeeAPIView.as_view()),
    path("v1/employee-account-details/<int:pk>/", AccountEmployeeAPIView.as_view()),
    path("v1/employee-address-details/", AddressEmployeeAPIView.as_view()),
    path("v1/employee-address-details/<int:pk>/", AddressEmployeeAPIView.as_view()),  
    ]
