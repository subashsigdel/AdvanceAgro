import requests

def get_weather(api_key, city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'  # You can change this to 'imperial' for Fahrenheit
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            print(data['dt_txt'])
            # Extract relevant weather information
            main_info = data['main']
            weather_info = data['weather'][0]
            temperature = main_info['temp']
            humidity = main_info['humidity']
            description = weather_info['description']

            print(f"Weather in {city}:")
            print(f"Temperature: {temperature}°C")
            print(f"Description: {description}")
            print(f"humidity: {humidity}")

        else:
            print(f"Failed to retrieve weather information. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key
api_key = '10d4dbd822bc129fa5dfaa9dac1bf2e0'

# Get user input for the city name
user_city = input("Enter the name of a city: ")

# Get and print weather information for the city
get_weather(api_key, user_city)




