import requests
from datetime import datetime
from .models import City, WeatherData, AirPollutionData
from django.conf import settings

def fetch_weather_data(city_name):
    api_key = settings.OPENWEATHERMAP_API_KEY
    if not api_key:
        print("API key not found in settings.")
        return
    
    weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'
    
    try:
        weather_response = requests.get(weather_url)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
    except requests.RequestException as e:
        print(f"Weather API request failed: {e}")
        return

    if weather_data.get('cod') == 200:
        city, created = City.objects.get_or_create(name=city_name)
        
        try:
            weather_record = WeatherData(
                city=city,
                temperature=weather_data['main']['temp'],
                humidity=weather_data['main']['humidity'],
                pressure=weather_data['main']['pressure'],
                weather_description=weather_data['weather'][0]['description'],
                timestamp=datetime.now()
            )
            weather_record.save()
        except Exception as e:
            print(f"Failed to save weather data: {e}")
            return

        # Fetch coordinates for air pollution data
        lat = weather_data['coord']['lat']
        lon = weather_data['coord']['lon']
        pollution_url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}'
        
        try:
            pollution_response = requests.get(pollution_url)
            pollution_response.raise_for_status()
            pollution_data = pollution_response.json()
        except requests.RequestException as e:
            print(f"Pollution API request failed: {e}")
            return

        if 'list' in pollution_data and pollution_data['list']:
            try:
                pollution_record = AirPollutionData(
                    city=city,
                    pm25=pollution_data['list'][0]['components']['pm2_5'],
                    pm10=pollution_data['list'][0]['components']['pm10'],
                    o3=pollution_data['list'][0]['components']['o3'],
                    no2=pollution_data['list'][0]['components']['no2'],
                    so2=pollution_data['list'][0]['components']['so2'],
                    co=pollution_data['list'][0]['components']['co'],
                    timestamp=datetime.now()
                )
                pollution_record.save()
            except Exception as e:
                print(f"Failed to save air pollution data: {e}")
        else:
            print("No air pollution data found.")
    else:
        print(f"City not found or weather API request failed with code: {weather_data.get('cod')}")

