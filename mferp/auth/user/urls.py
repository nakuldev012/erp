from .views import (
    UserLoginView,
    UserSignUpView,
    UserLogoutView,
    VerifyAccountView,
    ForgetPasswordEmailView,
    ResetPasswordView,
    ForgetPasswordVerifyView,
    ChangePasswordView, BulkUserSignUpView,CsvFileView
)
from django.urls import path


urlpatterns = [
    path("v1/signup/", UserSignUpView.as_view()),
    path("v1/login/", UserLoginView.as_view()),
    path("v1/logout/", UserLogoutView.as_view()),
    path("v1/verify-account/", VerifyAccountView.as_view()),
    path("v1/forget-password/", ForgetPasswordEmailView.as_view()),
    path("v1/reset-password/", ResetPasswordView.as_view()),
    path("v1/forget-password-verify/", ForgetPasswordVerifyView.as_view()),
    path("v1/change-password/", ChangePasswordView.as_view()),
    path("v1/bulk-user-signup/",BulkUserSignUpView.as_view()),
    path("v1/csvfile/", CsvFileView.as_view(), name='csv-file-api'),
    
]
