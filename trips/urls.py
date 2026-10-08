from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    TripSimulationViewSet,
    VehicleViewSet,
)

router = DefaultRouter()

router.register(
    "simulations",
    TripSimulationViewSet,
    basename="simulation",
)

router.register(
    "vehicles",
    VehicleViewSet,
    basename="vehicle",
)

urlpatterns = [
    path("", include(router.urls)),
]
