from django.contrib import admin

from .models import (
    Toll,
    TripSimulation,
    Vehicle,
)

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "fuel_type",
        "consumption_km_per_liter",
        "active",
    )

    list_filter = (
        "fuel_type",
        "active",
    )
    
@admin.register(Toll)
class TollAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "active",
    )

    list_filter = (
        "active",
    )
    
@admin.register(TripSimulation)
class TripSimulationAdmin(admin.ModelAdmin):
    list_display = (
        "origin",
        "destination",
        "distance_km",
        "fuel_cost",
        "toll_cost",
        "total_cost",
        "created_at",
    )

    list_filter = (
        "round_trip",
        "created_at",
    )

    search_fields = (
        "origin",
        "destination",
    )