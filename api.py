# import required modules
import requests, json

# Enter your API key here
api_key = "5ce502e29c4663feda6eb895c482e492"

# base_url variable to store url
base_url = "http://api.openweathermap.org/data/2.5/weather?"

# Give city name
city_name = input("Enter city name : ")

# complete_url variable to store
# complete url address
complete_url = base_url + "appid=" + api_key + "&q=" + city_name

# get method of requests module
# return response object
response = requests.get(complete_url)

# json method of response object 
# convert json format data into
# python format data
x = response.json()

# Now x contains list of nested dictionaries
# Check the value of "cod" key is equal to
# "404", means city is found otherwise,
# city is not foun

# Print the entire API response
print(json.dumps(x, indent=2))

# Check for City Existence:
if x["cod"] != "404":
    try:
        y = x["main"]
        current_temperature = y["temp"]
        current_pressure = y["pressure"]
        current_humidity = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        
        # Print Results
        print(" Temperature (in kelvin unit) = " + str(current_temperature) +
              "\n atmospheric pressure (in hPa unit) = " + str(current_pressure) +
              "\n humidity (in percentage) = " + str(current_humidity) +
              "\n description = " + str(weather_description))
    except KeyError as e:
        print(f"Error accessing key: {e}")
else:
    print(" City Not Found ")
