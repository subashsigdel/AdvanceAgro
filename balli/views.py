import os
from django.conf import settings
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.utils import timezone
from . models import *
from django.db.models import Subquery, OuterRef, F
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
import requests
from django.http import JsonResponse
from django.shortcuts import render
from datetime import datetime
import json
import requests
from bs4 import BeautifulSoup
import json

# Create your views here.


# user login
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully login.!")
            return redirect('dashboard')
        else:
            messages.error(request, "Sorry, You are not Register Yet.")
            return redirect('login')
    else:
        return render(request, 'login.html')


def dashboard(request):
    # Replace YOUR_CHANNEL_ID and YOUR_READ_API_KEY with your ThingSpeak channel ID and read API key
    channel_id = '2406931'
    read_api_key = 'WOR1D01GPESM0159'

    # ThingSpeak API endpoint for channel feeds
    api_url = f'https://api.thingspeak.com/channels/{channel_id}/feeds.json?api_key={read_api_key}'

    # for weather
    # api_key = '10d4dbd822bc129fa5dfaa9dac1bf2e0'
    # lat = '26.79'  # Replace with the latitude of your location
    # lon = '87.29'  # Replace with the longitude of your location
    # exclude = ''  # Replace with the parts you want to exclude (e.g., 'minutely,hourly,daily,alerts')
    
    # OpenWeatherMap One Call API endpoint
    api_url_w = f'http://api.openweathermap.org/data/2.5/forecast?id=524901&lat=31.1939&lon=75.9456&exclude=minutely,%20hourly,%20daily,%20alerts&appid=10d4dbd822bc129fa5dfaa9dac1bf2e0'

    try:
        humidity = None
        temperature = None

        # Make a GET request to OpenWeatherMap
        response_w = requests.get(api_url_w)
        data_w = json.loads(response_w.text)

        # Extract relevant weather information
        if 'list' in data_w and data_w['list']:
            first_entry = data_w['list'][0]
            
            main_info = first_entry.get('main', {})
            humidity = int(main_info.get('humidity'))
            temperature_kelvin = main_info.get('temp')

            # Convert Kelvin to Celsius
            temperature = int(temperature_kelvin - 273.15)

            weather_info = first_entry.get('weather', [])[0]
            weather_main = weather_info.get('main')
            weather_description = weather_info.get('description')
        else:
            
            print("Humidity and temperature not found in current weather data.")

        # Make a GET request to ThingSpeak
        response = requests.get(api_url)
        data = response.json()
        # Extract the last entry from the feed
        if 'feeds' in data and data['feeds']:
            last_entry = data['feeds'][-10:]
            
            context = {'latest_entry': last_entry,
                       'humidity': humidity,
                       'temperature': temperature,
                       'weather_main': weather_main,
                       'weather_description': weather_description,
                       }
            return render(request, 'index.html', context)
        else:
            return render(request, 'index.html', {'error': 'No data available from ThingSpeak'})

    except requests.RequestException as e:
        return render(request, 'index.html', {'error': f'Request failed: {str(e)}'})


def user_logout(request):
    logout(request)
    return redirect(reverse('login'))


def report(request):
    all_crops = CropTimeline.objects.all()
    crops_info = []
    current_time = timezone.now()

    for crop in all_crops:
        created_date = crop.created_date
        harvesting_time = crop.harvesting_time

        time_difference = harvesting_time - created_date
        time_difference_days = time_difference.days

        if time_difference_days > (current_time - created_date).days / 2:
            status = "ready"
        elif 1 <= time_difference_days < (current_time - created_date).days:
            status = "in progress"
        else:
            status = "done"

        crop_info = {
            'crop_type': crop.crop_type,
            'field_name': crop.field_name,
            'status': status,
        }

        crops_info.append(crop_info)

    context = {
        'crops_info': crops_info,
    }

    return render(request, 'report.html', context)


def user_input(request):
    crop_types = CropTimeline.CROP_TYPES
    if request.method == 'POST':
        crop_type = request.POST.get('crop_type')
        ideal_starting_temperature = request.POST.get('ideal_starting_temperature')
        ideal_starting_moisture = request.POST.get('ideal_starting_moisture')

        # Validate input as needed

        # Create a new crop instance
        crop_instance = CropTimeline.objects.create(
            crop_type=crop_type,
            ideal_starting_temperature=ideal_starting_temperature,
            ideal_starting_moisture=ideal_starting_moisture,
            initial_moisture=ideal_starting_moisture,  # Assuming you want to set initial values
            initial_temperature=ideal_starting_temperature,  # Assuming you want to set initial values
            pesticide_time=timezone.now() + timedelta(days=get_random_days()),
            migration_time=timezone.now() + timedelta(days=get_random_days()),
            harvesting_time=timezone.now() + timedelta(days=get_random_days())
        )

        # Redirect to a success page or display a confirmation message
        return render(request, 'report.html', {'message': 'Crop created successfully'})

    return render(request, 'userinput.html', {'crop_types': crop_types})

def get_random_days():
    # You can adjust the range and logic for generating random days as needed
    import random
    return random.randint(10, 30)


def timeline(request):
    # Retrieve all instances of the Crop model
    all_crops = CropTimeline.objects.all()

    # Get the current month in digit
    current_month_digit = int(datetime.now().month) + 3

    # Calculate month digits for each crop
    crops_info = []
    for crop in all_crops:
        created_month_digit = int(crop.created_date.month) + 3
        harvesting_month_digit = int(crop.harvesting_time.month) + 3
        field_name = crop.field_name

        if created_month_digit > 13:
            created_month_digit = created_month_digit - 12
        if harvesting_month_digit > 13:
            harvesting_month_digit - 12
        crop_info = {
            'crop_type': crop.crop_type,  # Include any other information you need
            'created_month_digit': created_month_digit,
            'harvesting_month_digit': harvesting_month_digit,
            'field_name': field_name,
        }

        crops_info.append(crop_info)

    context = {
        'crops_info': crops_info,
        'current_month_digit': current_month_digit,
    }
    return render(request, 'timeline.html', context)



def notice(request):
    URL = "https://kalimatimarket.gov.np/"
    r = requests.get(URL)

    soup = BeautifulSoup(r.content, 'lxml')

    # Check if the 'commodityDailyPrice' div exists on the page
    table = soup.find('table', attrs={'id': 'commodityDailyPrice'})
    if table:
        rows = table.find_all('tr')
        
        vegetables_data = []

        # Iterate through rows and extract data
        for row in rows:
            columns = row.find_all('td')
            
            if columns:  # Check if the row has columns
              
                vegetable_name = columns[0].text.strip()
                min_price = columns[1].text.strip()
                max_price = columns[2].text.strip()
                avg_price = columns[3].text.strip()

                # Add the data to the vegetables_data list
                vegetables_data.append({
                    'name': vegetable_name,
                    'min_price': min_price,
                    'max_price': max_price,
                    'avg_price': avg_price,
                })

        return render(request, 'notice.html', {'vegetables_data': vegetables_data})
    else:
        return render(request, 'notice.html', {'error_message': "Table with id 'commodityDailyPrice' not found on the page."})
