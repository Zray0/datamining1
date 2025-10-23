from django.urls import path
from .views import clusters_overview, rules_page

app_name = "analytics"
urlpatterns = [
    path("clusters/", clusters_overview, name="clusters_overview"),
    path("rules-page/", rules_page, name="rules_page"),
]
