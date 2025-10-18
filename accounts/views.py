# accounts/views.py
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import (
    LoginView, LogoutView,
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView,
)
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import CustomerSignupForm, FancyAuthenticationForm
from .models import Customer

class UnifiedLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = FancyAuthenticationForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.request.user
        if not form.cleaned_data.get("remember"):
            self.request.session.set_expiry(0)
        if not user.is_staff:
            profile = getattr(user, "customer", None)
            if profile:
                self.request.session["customer"] = {"full_name": profile.full_name, "phone": profile.phone}
        messages.success(self.request, "Signed in successfully.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)

    def get_success_url(self):
        nxt = self.get_redirect_url()
        if nxt:
            return nxt
        return reverse_lazy("dashboards:dashboard_home")

class CustomerSignupView(FormView):
    template_name = "accounts/signup.html"
    form_class = CustomerSignupForm
    success_url = reverse_lazy("dashboards:dashboard_home")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_staff = False
        user.is_superuser = False
        user.save()
        Customer.objects.create(
            user=user,
            full_name=form.cleaned_data.get("full_name", ""),
            phone=form.cleaned_data.get("phone", ""),
            address=form.cleaned_data.get("address", ""),
        )
        login(self.request, user)
        messages.success(self.request, "Account created successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)

class MyLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:login")

class MyPasswordResetView(PasswordResetView):
    template_name = "accounts/password_reset.html"
    email_template_name = "accounts/password_reset_email.txt"
    subject_template_name = "accounts/password_reset_subject.txt"
    success_url = reverse_lazy("accounts:password_reset_done")

class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = "accounts/password_reset_done.html"

class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"
    success_url = reverse_lazy("accounts:password_reset_complete")

class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "accounts/password_reset_complete.html"

# accounts/views.py
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView

class UnifiedLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True
    # ... form logic unchanged ...

    def get_success_url(self):
        user = self.request.user
        # Force staff/superusers to admin (or analytics) regardless of ?next
        if user.is_staff or user.is_superuser:
            return reverse_lazy("admin:index")   # or reverse_lazy("analytics:rules_page")
        # For customers, respect ?next if present and safe
        nxt = self.get_redirect_url()
        if nxt:
            return nxt
        return reverse_lazy("dashboards:dashboard_home")
