from django.shortcuts import render
from django.conf import settings
import requests
from .models import City

def index(request):
    cities = City.objects.all()
    weather_data = []
    air_pollution_data = []
    error_message = None

    if request.method == 'POST':
        city_name = request.POST['city']
        weather_response = get_weather_data(city_name)
        air_pollution_response = get_air_pollution_data(city_name)

        if weather_response and air_pollution_response:
            weather_data.append({
                'city': {'name': city_name},
                'temperature': weather_response['main']['temp'],
                'humidity': weather_response['main']['humidity'],
                'pressure': weather_response['main']['pressure'],
                'weather_description': weather_response['weather'][0]['description'],
                'timestamp': weather_response['dt']
            })

            air_pollution_data.append({
                'city': {'name': city_name},
                'pm25': air_pollution_response['list'][0]['components']['pm2_5'],
                'pm10': air_pollution_response['list'][0]['components']['pm10'],
                'o3': air_pollution_response['list'][0]['components']['o3'],
                'no2': air_pollution_response['list'][0]['components']['no2'],
                'so2': air_pollution_response['list'][0]['components']['so2'],
                'co': air_pollution_response['list'][0]['components']['co'],
                'timestamp': air_pollution_response['list'][0]['dt']
            })
        else:
            error_message = "City not found or API request failed."

    context = {
        'cities': cities,
        'weather_data': weather_data,
        'air_pollution_data': air_pollution_data,
        'error_message': error_message
    }

    return render(request, 'weather/index.html', context)

def get_weather_data(city_name):
    api_key = settings.WEATHER_API_KEY
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_air_pollution_data(city_name):
    api_key = settings.WEATHER_API_KEY
    lat, lon = get_city_coordinates(city_name)
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_city_coordinates(city_name):
    # Dummy implementation; replace with actual method to get coordinates
    coordinates = {
        'New York': (40.7128, -74.0060),
        'Los Angeles': (34.0522, -118.2437),
        
    }
    return coordinates.get(city_name, (0, 0))





















# from django.shortcuts import render, get_object_or_404
# from .models import City, WeatherData, AirPollutionData
# from datetime import datetime
# from django.conf import settings
# import requests
# from django.http import JsonResponse

# def fetch_weather_data(city_name):
#     api_key = settings.OPENWEATHERMAP_API_KEY
#     weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'
    
#     weather_response = requests.get(weather_url).json()
    
#     if weather_response['cod'] == 200:
#         lat = weather_response['coord']['lat']
#         lon = weather_response['coord']['lon']
        
#         city, _ = City.objects.get_or_create(name=city_name, latitude=lat, longitude=lon)

#         WeatherData.objects.create(
#             city=city,
#             temperature=weather_response['main']['temp'],
#             humidity=weather_response['main']['humidity'],
#             pressure=weather_response['main']['pressure'],
#             weather_description=weather_response['weather'][0]['description'],
#             timestamp=datetime.now()
#         )

#         pollution_url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}'
#         pollution_response = requests.get(pollution_url).json()

#         if 'list' in pollution_response:
#             AirPollutionData.objects.create(
#                 city=city,
#                 pm25=pollution_response['list'][0]['components']['pm2_5'],
#                 pm10=pollution_response['list'][0]['components']['pm10'],
#                 o3=pollution_response['list'][0]['components']['o3'],
#                 no2=pollution_response['list'][0]['components']['no2'],
#                 so2=pollution_response['list'][0]['components']['so2'],
#                 co=pollution_response['list'][0]['components']['co'],
#                 timestamp=datetime.now()
#             )
#     else:
#         print("City not found or API request failed.")

# def index(request):
#     cities = City.objects.all()

#     if request.method == 'POST':
#         city_name = request.POST.get('city')
#         fetch_weather_data(city_name)
    
#     weather_data_list = []
#     air_pollution_data_list = []

#     for city in cities:
#         latest_weather = WeatherData.objects.filter(city=city).latest('timestamp')
#         latest_pollution = AirPollutionData.objects.filter(city=city).latest('timestamp')

#         weather_data_list.append(latest_weather)
#         air_pollution_data_list.append(latest_pollution)

#     return render(request, 'weather/index.html', {
#         'cities': cities,
#         'weather_data_list': weather_data_list,
#         'air_pollution_data_list': air_pollution_data_list
#     })




# # from django.shortcuts import render,get_object_or_404
# # from .models import City, WeatherData, AirPollutionData
# # from datetime import datetime
# # import requests
# # from django.http import JsonResponse
# # from .utils import fetch_weather_data
# # # Create your views here.

# # def fetch_weather_data(city_name):
# #     api_key = 'YOUR_API_KEY'
# #     weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'
# #     pollution_url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}'

# #     weather_response = requests.get(weather_url).json()
# #     pollution_response = requests.get(pollution_url).json()

# #     if weather_response['cod'] == 200:
# #         city, _ = City.objects.get_or_create(name=city_name)
        
# #         weather_data = WeatherData(
# #             city=city,
# #             temperature=weather_response['main']['temp'],
# #             humidity=weather_response['main']['humidity'],
# #             pressure=weather_response['main']['pressure'],
# #             weather_description=weather_response['weather'][0]['description'],
# #             timestamp=datetime.now()
# #         )
# #         weather_data.save()

# #         lat = weather_response['coord']['lat']
# #         lon = weather_response['coord']['lon']
# #         pollution_url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}'
# #         pollution_response = requests.get(pollution_url).json()

# #         if 'list' in pollution_response:
# #             pollution_data = AirPollutionData(
# #                 city=city,
# #                 pm25=pollution_response['list'][0]['components']['pm2_5'],
# #                 pm10=pollution_response['list'][0]['components']['pm10'],
# #                 o3=pollution_response['list'][0]['components']['o3'],
# #                 no2=pollution_response['list'][0]['components']['no2'],
# #                 so2=pollution_response['list'][0]['components']['so2'],
# #                 co=pollution_response['list'][0]['components']['co'],
# #                 timestamp=datetime.now()
# #             )
# #             pollution_data.save()

# #     else:
# #         print("City not found or API request failed.")

# # def index(request):
# #     cities = City.objects.all()

# #     if request.method == 'POST':
# #         city_name = request.POST.get('city')
# #         city = get_object_or_404(City, name=city_name)
# #         lat = city.latitude
# #         lon = city.longitude

# #         try:
# #             weather_response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=YOUR_API_KEY')
# #             weather_response.raise_for_status()  # Raise an error if the request was unsuccessful
# #             weather_json = weather_response.json()

# #             air_pollution_response = requests.get(f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid=YOUR_API_KEY')
# #             air_pollution_response.raise_for_status()  # Raise an error if the request was unsuccessful
# #             air_pollution_json = air_pollution_response.json()

# #             weather_data = {
# #                 'city': city,
# #                 'temperature': weather_json.get('main', {}).get('temp'),
# #                 'humidity': weather_json.get('main', {}).get('humidity'),
# #                 'pressure': weather_json.get('main', {}).get('pressure'),
# #                 'weather_description': weather_json['weather'][0].get('description'),
# #                 'timestamp': weather_json['dt']
# #             }

# #             air_pollution_data = {
# #                 'city': city,
# #                 'pm25': air_pollution_json['list'][0]['components']['pm2_5'],
# #                 'pm10': air_pollution_json['list'][0]['components']['pm10'],
# #                 'o3': air_pollution_json['list'][0]['components']['o3'],
# #                 'no2': air_pollution_json['list'][0]['components']['no2'],
# #                 'so2': air_pollution_json['list'][0]['components']['so2'],
# #                 'co': air_pollution_json['list'][0]['components']['co'],
# #                 'timestamp': air_pollution_json['list'][0]['dt']
# #             }

# #             return render(request, 'weather/index.html', {
# #                 'cities': cities,
# #                 'weather_data': weather_data,
# #                 'air_pollution_data': air_pollution_data
# #             })

# #         except requests.exceptions.RequestException as e:
# #             error_message = "Failed to fetch data from the weather API. Please try again later."
# #             return render(request, 'weather/index.html', {'cities': cities, 'error_message': error_message})

# #     return render(request, 'weather/index.html', {'cities': cities})


#     # if 'list' in pollution_response:
#     #     pollution_data = AirPollutionData(
#     #         city=city,
#     #         pm25=pollution_response['list'][0]['components']['pm2_5'],
#     #         pm10=pollution_response['list'][0]['components']['pm10'],
#     #         o3=pollution_response['list'][0]['components']['o3'],
#     #         no2=pollution_response['list'][0]['components']['no2'],
#     #         so2=pollution_response['list'][0]['components']['so2'],
#     #         co=pollution_response['list'][0]['components']['co'],
#     #         timestamp=datetime.now()
#     #     )
#     #     pollution_data.save()


# # def index(request):
# #     cities = City.objects.all()
# #     weather_data = []
# #     air_pollution_data = []

# #     if request.method == 'POST':
# #         city_name = request.POST.get('city')
# #         city = get_object_or_404(City, name=city_name)
# #         lat = city.latitude
# #         lon = city.longitude

# #         weather_response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=YOUR_API_KEY')
# #         weather_json = weather_response.json()

# #         air_pollution_response = requests.get(f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid=YOUR_API_KEY')
# #         air_pollution_json = air_pollution_response.json()

# #     if 'weather' in weather_json:
# #         weather_data.append({
# #              'city': city,
# #             'temperature': weather_json.get('main', {}).get('temp'),
# #             'humidity': weather_json.get('main', {}).get('humidity'),
# #             'pressure': weather_json.get('main', {}).get('pressure'),
# #             'weather_description': weather_json['weather'][0]['description'],
# #             'timestamp': weather_json['dt']

# #         })

# #     if 'list' in air_pollution_json:
# #         air_pollution_data.append({
# #             'city': city,
# #             'pm25': air_pollution_json['list'][0]['components']['pm2_5'],
# #             'pm10': air_pollution_json['list'][0]['components']['pm10'],
# #             'o3': air_pollution_json['list'][0]['components']['o3'],
# #             'no2': air_pollution_json['list'][0]['components']['no2'],
# #             'so2': air_pollution_json['list'][0]['components']['so2'],
# #             'co': air_pollution_json['list'][0]['components']['co'],
# #             'timestamp': air_pollution_json['list'][0]['dt']
# #         })

# #     return render(request, 'weather/index.html', {
# #         'cities': cities,
# #         'weather_data': weather_data,
# #         'air_pollution_data': air_pollution_data
# #     })