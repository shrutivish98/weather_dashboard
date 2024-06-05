from django.db import models
from django.utils import timezone

# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()



class WeatherData(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    temperature = models.FloatField()
    humidity = models.FloatField()
    pressure = models.FloatField()
    weather_description = models.CharField(max_length=255)
    timestamp = models.DateTimeField()

class AirPollutionData(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    pm25 = models.FloatField()
    pm10 = models.FloatField()
    o3 = models.FloatField()
    no2 = models.FloatField()
    so2 = models.FloatField()
    co = models.FloatField()
    timestamp = models.DateTimeField()
