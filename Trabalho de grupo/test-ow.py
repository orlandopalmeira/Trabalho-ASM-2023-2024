import requests, os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

API_KEY=os.getenv("API_KEY")

def get_coordinates(city_name):
    api_key = API_KEY
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    full_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(full_url)
    data = response.json()
    if data["cod"] != "404":
        coordinates = data["coord"]
        lat = coordinates["lat"]
        lon = coordinates["lon"]
    else:
        print(f"ERROR 404: Asking for coordinates in {city_name} at {full_url}")
    return lat, lon

def get_weathers(city_name, start_time, end_time):
    """OpenWeatherMap API."""
    api_key = API_KEY
    lat, lon = get_coordinates(city_name)
    start_time = transform_date_to_ts(start_time)
    end_time = transform_date_to_ts(end_time)
    # count = 24
    # full_url = f"https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type=hour&start={start_time}&cnt={count}&appid={api_key}"
    full_url = f"https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type=hour&start={start_time}&end={end_time}&appid={api_key}"
    print(full_url)
    response = requests.get(full_url)
    data = response.json()
    if data["cod"] in ["404", "400", "401", "429", "500", "503", "504"]:
        print(f"ERROR {data["cod"]}: Asking for weather in {city_name} at {full_url}")
    weathers = data["list"]
    return weathers

def transform_weathers_to_bool(weathers):
    """Transforms the weather data to a boolean value. If True it means that the weather is good. Else should be bad."""
    for weather_tick in weathers:
        if len(weather_tick["weather"]) > 1:
            print(weather_tick["weather"])
        #! Check if given a list of weather, there is one bad weather
        weather = weather_tick["weather"][0]
        tempo = weather["main"]

def transform_date_to_ts(date):
    return int(datetime.strptime(date, "%Y-%m-%d %H:%M:%S").timestamp())

def transform_ts_to_date(ts):
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

if __name__ == "__main__":
    city_name = "Porto"
    start_time = "2024-01-06 12:00:00"
    end_time = "2024-02-06 12:00:00"
    weather = get_weathers(city_name, start_time, end_time)

    print("Weather:", weather)

