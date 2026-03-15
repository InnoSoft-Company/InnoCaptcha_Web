from django.urls import path
from . import views as v

urlpatterns = [
  path("analytics/ReposVisitorsCountShield/", v.analytics.Shields.ReposVisitorsCountShield.as_view(), name="api-analytics-ReposVisitorsCountShieldAPI"),
  path("analytics/install/", v.analytics.Shields.InstallPingAPIView.as_view(), name="api-analytics-InstallPingAPIView"),

]
