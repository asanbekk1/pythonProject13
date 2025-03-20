from django.urls import path
from .views import (
    UserRegistrationView,
    UserConfirmationView,
    UserLoginView,
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('confirm/', UserConfirmationView.as_view(), name='user-confirm'),
    path('login/', UserLoginView.as_view(), name='user-login'),
]