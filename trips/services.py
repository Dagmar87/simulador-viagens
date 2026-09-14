import requests

from django.conf import settings


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
