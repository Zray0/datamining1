# accounts/views.py
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import FancyAuthenticationForm, CustomerSignupForm

class UnifiedLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = FancyAuthenticationForm
    redirect_authenticated_user = True
    def form_valid(self, form):
        resp = super().form_valid(form)
        messages.success(self.request, "Signed in successfully.")
        return resp
    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)
    def get_success_url(self):
        u = self.request.user
        if u.is_staff or u.is_superuser:
            return reverse_lazy("admin:index")
        nxt = self.get_redirect_url()
        return nxt or reverse_lazy("dashboards:dashboard_home")

class CustomerSignupView(FormView):
    template_name = "accounts/signup.html"
    form_class = CustomerSignupForm
    success_url = reverse_lazy("dashboards:dashboard_home")
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_staff = False
        user.is_superuser = False
        user.save()
        login(self.request, user)
        messages.success(self.request, "Account created successfully.")
        return super().form_valid(form)

class MyLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:login")
