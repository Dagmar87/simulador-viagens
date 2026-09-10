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
