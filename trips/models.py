from django.db import models

class FuelType(models.TextChoices):
  
  GASOLINE = "gasoline", "Gasolina"
  ETHANOL = "ethanol", "Etanol"
  DIESEL = "diesel", "Diesel"
  FLEX = "flex", "Flex"

class Vehicle(models.Model):
  
  name = models.CharField(max_length=150)
  
  fuel_type = models.CharField(
        max_length=20,
        choices=FuelType.choices,
    )
  
  consumption_km_per_liter = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )
  
  active = models.BooleanField(default=True)
  
  created_at = models.DateTimeField(auto_now_add=True)
  
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
        return self.name
      
class TripSimulation(models.Model):
  
  origin = models.CharField(max_length=255)
  
  destination = models.CharField(max_length=255)
  
  origin_latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True,
    )
  
  origin_longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True,
    )
  
  destination_latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True,
    )
  
  destination_longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True,
    )
  
  fuel_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )
  
  average_speed_kmh = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )
  
  round_trip = models.BooleanField(default=False)
  
  distance_km = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )
  
  duration_minutes = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )
  
  fuel_liters = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )
  
  fuel_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )
  
  toll_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )
  
  total_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )
  
  route_geometry = models.JSONField(
        null=True,
        blank=True,
    )
  
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
        return f"{self.origin} → {self.destination}"
      
class Toll(models.Model):
  
  name = models.CharField(
        max_length=150,
    )
  
  latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
    )
  
  longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
    )
  
  price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )
  
  active = models.BooleanField(
        default=True,
    )
  
  created_at = models.DateTimeField(
        auto_now_add=True,
    )
  
  def __str__(self):
        return self.name



