from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserLogoutView, UserProfileView, PasswordResetView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('password_reset/', PasswordResetView.as_view(), name='password-reset'),
]
