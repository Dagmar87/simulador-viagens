import requests

from django.conf import settings

from decimal import Decimal


class GeocodingService:

    def __init__(self):
        self.base_url = settings.NOMINATIM_URL

    def search(self, address: str) -> dict:
        response = requests.get(
            self.base_url,
            params={
                "q": address,
                "format": "json",
                "limit": 1,
                "countrycodes": "br",
            },
            headers={
                "User-Agent": "simulador-viagens/1.0",
            },
            timeout=15,
        )

        response.raise_for_status()

        results = response.json()

        if not results:
            raise ValueError(f"Endereço não encontrado: {address}")

        result = results[0]

        return {
            "latitude": float(result["lat"]),
            "longitude": float(result["lon"]),
            "display_name": result["display_name"],
        }


class RoutingService:

    def __init__(self):
        self.base_url = settings.OSRM_URL

    def calculate_route(
        self,
        origin_latitude: float,
        origin_longitude: float,
        destination_latitude: float,
        destination_longitude: float,
    ) -> dict:

        coordinates = (
            f"{origin_longitude},{origin_latitude};"
            f"{destination_longitude},{destination_latitude}"
        )

        url = f"{self.base_url}/route/v1/driving/" f"{coordinates}"

        response = requests.get(
            url,
            params={
                "overview": "full",
                "geometries": "geojson",
                "steps": "true",
            },
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        if data.get("code") != "Ok":
            raise ValueError(
                f"Não foi possível calcular a rota: " f"{data.get('code')}"
            )

        if not data.get("routes"):
            raise ValueError("Nenhuma rota encontrada.")

        route = data["routes"][0]

        return {
            "distance_meters": route["distance"],
            "duration_seconds": route["duration"],
            "geometry": route.get("geometry"),
            "legs": route.get("legs", []),
        }


class TripCalculator:

    @staticmethod
    def calculate(
        distance_km,
        consumption_km_per_liter,
        fuel_price,
        average_speed_kmh,
        toll_cost=Decimal("0"),
        round_trip=False,
    ):

        distance_km = Decimal(str(distance_km))

        consumption = Decimal(str(consumption_km_per_liter))

        fuel_price = Decimal(str(fuel_price))

        average_speed = Decimal(str(average_speed_kmh))

        toll_cost = Decimal(str(toll_cost))

        multiplier = Decimal("2") if round_trip else Decimal("1")

        total_distance = distance_km * multiplier

        fuel_liters = total_distance / consumption

        fuel_cost = fuel_liters * fuel_price

        duration_minutes = total_distance / average_speed * Decimal("60")

        total_toll = toll_cost * multiplier

        total_cost = fuel_cost + total_toll

        return {
            "distance_km": total_distance.quantize(Decimal("0.01")),
            "fuel_liters": fuel_liters.quantize(Decimal("0.01")),
            "fuel_cost": fuel_cost.quantize(Decimal("0.01")),
            "duration_minutes": duration_minutes.quantize(Decimal("0.01")),
            "toll_cost": total_toll.quantize(Decimal("0.01")),
            "total_cost": total_cost.quantize(Decimal("0.01")),
        }
