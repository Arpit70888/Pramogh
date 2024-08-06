from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import *

router = DefaultRouter()
router.register(r'profile', ProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegistrationAPI.as_view()),
    path('login/', UserLoginAPI.as_view()),
    path('delete/', AccountDeleteView.as_view()),
    path('password/change/', PasswordChangeAPI.as_view()),
    path('otp/', OTPView.as_view()),
    path('reset/password/', PasswordResetView.as_view()),
]
