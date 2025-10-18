# accounts/urls.py
from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.UnifiedLoginView.as_view(), name="login"),
    path("signup/", views.CustomerSignupView.as_view(), name="signup"),
    path("logout/", views.MyLogoutView.as_view(), name="logout"),
    path("password-reset/", views.MyPasswordResetView.as_view(), name="password_reset"),
    path("password-reset/done/", views.MyPasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", views.MyPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", views.MyPasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
