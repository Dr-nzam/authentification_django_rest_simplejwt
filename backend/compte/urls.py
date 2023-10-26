from django.urls import path
from .views import RegisterView, reset_password_email,reset_password
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from dj_rest_auth.views import LogoutView
from dj_rest_auth.views import (
    PasswordResetConfirmView,
    PasswordResetView,
)
from compte.views import password_reset_confirm_redirect

urlpatterns = [
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("api/logout/", LogoutView.as_view(), name="rest_logout"),
    path('api/register/', RegisterView.as_view(), name="sign_up"),
    path('api/reset_password_email/', reset_password_email, name='reset_password_email'),
    path('api/reset_password/', reset_password, name='reset_password'),
    
    path("password/reset/", PasswordResetView.as_view(), name="rest_password_reset"),
    path(
        "password/reset/confirm/<str:uidb64>/<str:token>/",
        password_reset_confirm_redirect,
        name="password_reset_confirm",
    ),
    path("password/reset/confirm/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    
]