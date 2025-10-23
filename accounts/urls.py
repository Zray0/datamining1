# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import UnifiedLoginView, CustomerSignupView, MyLogoutView

app_name = "accounts"

urlpatterns = [
    path("login/", UnifiedLoginView.as_view(), name="login"),
    path("signup/", CustomerSignupView.as_view(), name="signup"),
    path("logout/", MyLogoutView.as_view(), name="logout"),

    # Password reset URLs with canonical names
    path("password-reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
