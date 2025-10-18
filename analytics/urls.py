
# analytics/urls.py
from django.urls import path
from .views import rules_page
from .views import rules_api
app_name = "analytics"
urlpatterns = [path("rules/", rules_api, name="rules_api"),
               path("rules-page/", rules_page, name="rules_page"),]
