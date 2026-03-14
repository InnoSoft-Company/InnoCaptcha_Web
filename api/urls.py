from django.urls import path
from . import views as v

urlpatterns = [
  path("analytics/ReposVisitorsCountShield", v.ReposVisitorsCountShield.as_view(), name="api-analytics-ReposVisitorsCountShieldAPI"),

]
