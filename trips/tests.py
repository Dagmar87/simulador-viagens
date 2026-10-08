from decimal import Decimal

from django.test import TestCase

from .services import TripCalculator


class TripCalculatorTest(TestCase):

    def test_calculate_trip(self):

        result = TripCalculator.calculate(
            distance_km=Decimal("600"),
            consumption_km_per_liter=Decimal("12"),
            fuel_price=Decimal("6"),
            average_speed_kmh=Decimal("80"),
            toll_cost=Decimal("50"),
            round_trip=False,
        )

        self.assertEqual(
            result["distance_km"],
            Decimal("600.00"),
        )

        self.assertEqual(
            result["fuel_liters"],
            Decimal("50.00"),
        )

        self.assertEqual(
            result["fuel_cost"],
            Decimal("300.00"),
        )

        self.assertEqual(
            result["duration_minutes"],
            Decimal("450.00"),
        )

        self.assertEqual(
            result["toll_cost"],
            Decimal("50.00"),
        )

        self.assertEqual(
            result["total_cost"],
            Decimal("350.00"),
        )

    def test_round_trip(self):
        result = TripCalculator.calculate(
            distance_km=500,
            consumption_km_per_liter=10,
            fuel_price=5,
            average_speed_kmh=100,
            toll_cost=20,
            round_trip=True,
        )

        self.assertEqual(
            result["distance_km"],
            Decimal("1000.00"),
        )

        self.assertEqual(
            result["fuel_liters"],
            Decimal("100.00"),
        )

        self.assertEqual(
            result["fuel_cost"],
            Decimal("500.00"),
        )

        self.assertEqual(
            result["toll_cost"],
            Decimal("40.00"),
        )

        self.assertEqual(
            result["total_cost"],
            Decimal("540.00"),
        )
