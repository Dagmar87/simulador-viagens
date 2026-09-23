from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import TripSimulation, Vehicle
from .serializers import TripSimulationSerializer
from .services import GeocodingService, RoutingService, TripCalculator


class TripSimulationViewSet(viewsets.ModelViewSet):

    queryset = TripSimulation.objects.all().order_by("-created_at")

    serializer_class = TripSimulationSerializer

    def create(self, request, *args, **kwargs):

        origin = request.data.get("origin")
        destination = request.data.get("destination")

        vehicle_id = request.data.get("vehicle_id")

        fuel_price = request.data.get("fuel_price")
        average_speed = request.data.get("average_speed_kmh")

        round_trip = request.data.get("round_trip", False)

        if not origin:
            return Response(
                {"detail": "Origem é obrigatória."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not destination:
            return Response(
                {"detail": "Destino é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not vehicle_id:
            return Response(
                {"detail": "vehicle_id é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        vehicle = Vehicle.objects.filter(id=vehicle_id, active=True).first()

        if not vehicle:
            return Response(
                {"detail": "Veículo não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:

            fuel_price = float(fuel_price)

            average_speed = float(average_speed)

        except (TypeError, ValueError):

            return Response(
                {
                    "detail": (
                        "fuel_price e " "average_speed_kmh " "devem ser numéricos."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if fuel_price <= 0:

            return Response(
                {"detail": ("fuel_price deve ser " "maior que zero.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if average_speed <= 0:

            return Response(
                {"detail": ("average_speed_kmh deve " "ser maior que zero.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:

            geocoder = GeocodingService()

            origin_data = geocoder.search(origin)

            destination_data = geocoder.search(destination)

            router = RoutingService()

            route = router.calculate_route(
                origin_latitude=origin_data["latitude"],
                origin_longitude=origin_data["longitude"],
                destination_latitude=destination_data["latitude"],
                destination_longitude=destination_data["longitude"],
            )

            distance_km = route["distance_meters"] / 1000

            calculation = TripCalculator.calculate(
                distance_km=distance_km,
                consumption_km_per_liter=float(vehicle.consumption_km_per_liter),
                fuel_price=fuel_price,
                average_speed_kmh=average_speed,
                toll_cost=0,
                round_trip=round_trip,
            )

            simulation = TripSimulation.objects.create(
                origin=origin,
                destination=destination,
                origin_latitude=origin_data["latitude"],
                origin_longitude=origin_data["longitude"],
                destination_latitude=destination_data["latitude"],
                destination_longitude=destination_data["longitude"],
                fuel_price=fuel_price,
                average_speed_kmh=average_speed,
                round_trip=round_trip,
                distance_km=calculation["distance_km"],
                duration_minutes=calculation["duration_minutes"],
                fuel_liters=calculation["fuel_liters"],
                fuel_cost=calculation["fuel_cost"],
                toll_cost=calculation["toll_cost"],
                total_cost=calculation["total_cost"],
                route_geometry=route["geometry"],
            )

        except ValueError as exc:

            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(simulation)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )
