from rest_framework import serializers

from .models import TripSimulation


class TripSimulationSerializer(serializers.ModelSerializer):

    class Meta:
        model = TripSimulation

        fields = [
            "id",
            "origin",
            "destination",
            "fuel_price",
            "average_speed_kmh",
            "round_trip",
            "distance_km",
            "duration_minutes",
            "fuel_liters",
            "fuel_cost",
            "toll_cost",
            "total_cost",
            "route_geometry",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "distance_km",
            "duration_minutes",
            "fuel_liters",
            "fuel_cost",
            "toll_cost",
            "total_cost",
            "route_geometry",
            "created_at",
        ]

        def validate_fuel_price(self, value):

            if value <= 0:
                raise serializers.ValidationError(
                    "O preço do combustível deve ser maior que zero."
                )

            return value

        def validate_average_speed_kmh(self, value):

            if value <= 0:
                raise serializers.ValidationError(
                    "A velocidade média deve ser maior que zero."
                )

            return value
