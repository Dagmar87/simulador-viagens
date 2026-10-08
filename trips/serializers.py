from rest_framework import serializers

from .models import TripSimulation, Vehicle, Toll


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

    def validate_origin(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("A origem é obrigatória.")

        if len(value) < 3:
            raise serializers.ValidationError("Informe uma origem válida.")

        if len(value) > 255:
            raise serializers.ValidationError(
                "A origem deve ter no máximo 255 caracteres."
            )

        return value

    def validate_destination(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("O destino é obrigatório.")

        if len(value) < 3:
            raise serializers.ValidationError("Informe um destino válido.")

        if len(value) > 255:
            raise serializers.ValidationError(
                "O destino deve ter no máximo 255 caracteres."
            )

        return value

    def validate_fuel_price(self, value):
        """
        Valida o preço do combustível.

        Valores aceitáveis:
        - maior que R$ 0,00
        - no máximo R$ 20,00 por litro
        """

        if value <= 0:
            raise serializers.ValidationError(
                "O preço do combustível deve ser maior que zero."
            )

        if value > 20:
            raise serializers.ValidationError(
                "O preço do combustível não pode ser maior que R$ 20,00 por litro."
            )

        return value

    def validate_average_speed_kmh(self, value):
        """
        Valida a velocidade média utilizada no cálculo.

        Valores aceitáveis:
        - maior que 0 km/h
        - no máximo 200 km/h
        """

        if value <= 0:
            raise serializers.ValidationError(
                "A velocidade média deve ser maior que zero."
            )

        if value > 200:
            raise serializers.ValidationError(
                "A velocidade média não pode ser maior que 200 km/h."
            )

        return value


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle

        fields = [
            "id",
            "name",
            "fuel_type",
            "consumption_km_per_liter",
            "active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("O nome do veículo é obrigatório.")

        if len(value) < 2:
            raise serializers.ValidationError(
                "O nome do veículo deve ter pelo menos 2 caracteres."
            )

        if len(value) > 150:
            raise serializers.ValidationError(
                "O nome do veículo deve ter no máximo 150 caracteres."
            )

        return value

    def validate_consumption_km_per_liter(self, value):
        """
        Valida o consumo do veículo.

        Exemplos razoáveis:
        - 5 km/L
        - 8 km/L
        - 12 km/L
        - 15 km/L

        Valores abaixo de 1 km/L ou acima de 30 km/L
        são considerados fora da faixa esperada para
        este simulador.
        """

        if value <= 0:
            raise serializers.ValidationError("O consumo deve ser maior que zero.")

        if value < 1:
            raise serializers.ValidationError(
                "O consumo não pode ser menor que 1 km/L."
            )

        if value > 30:
            raise serializers.ValidationError(
                "O consumo não pode ser maior que 30 km/L."
            )

        return value


class TollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Toll

        fields = [
            "id",
            "name",
            "latitude",
            "longitude",
            "price",
            "active",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
        ]

    def validate_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("O nome do pedágio é obrigatório.")

        if len(value) < 2:
            raise serializers.ValidationError(
                "O nome do pedágio deve ter pelo menos 2 caracteres."
            )

        return value

    def validate_latitude(self, value):
        if value < -90 or value > 90:
            raise serializers.ValidationError("A latitude deve estar entre -90 e 90.")

        return value

    def validate_longitude(self, value):
        if value < -180 or value > 180:
            raise serializers.ValidationError(
                "A longitude deve estar entre -180 e 180."
            )

        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "O preço do pedágio não pode ser negativo."
            )

        if value > 500:
            raise serializers.ValidationError(
                "O preço do pedágio não pode ser maior que R$ 500,00."
            )

        return value
