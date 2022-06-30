from django.urls import path
from .views import RegisterAPIView, LoginAPIView, PasswordResetAPIView

urlpatterns = [
    path('register', RegisterAPIView.as_view(), name="register"),
    path('login', LoginAPIView.as_view(), name="login"),
    path('reset-password', PasswordResetAPIView.as_view(), name="reset-password")
]
