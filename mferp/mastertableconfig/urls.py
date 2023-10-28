from django.urls import path
from .views import CreateCategoryOrSubcategoryView, OrganizationView, TestView

urlpatterns = [
    path("v1/category/", CreateCategoryOrSubcategoryView.as_view()),
    path("v1/category/<int:pk>/", CreateCategoryOrSubcategoryView.as_view()),
    path("v1/organization/", OrganizationView.as_view()),
    path("v1/test/", TestView.as_view()),
    # path("v1/organization/<int:pk>/", OrganizationView.as_view()),
    ]

    