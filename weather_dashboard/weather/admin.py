from django.contrib import admin
from .models import City, WeatherData, AirPollutionData
# Register your models here.

admin.site.register(City)
admin.site.register(WeatherData)
admin.site.register(AirPollutionData)