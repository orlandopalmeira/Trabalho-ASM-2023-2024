import requests, os
from datetime import datetime
# from Utils.Prints import *

# API_KEY = "c5edae66c459cb80a6c09d9aacea3e2c" # OpenWeatherMap API key - base
API_KEY=os.getenv("API_KEY")

# GOOD = cfg.get_good_weather() # "Clear"
# BAD = cfg.get_bad_weather() # "Thunderstorm"
GOOD = "Clear"
BAD = "Thunderstorm"


#> Obtem info das APIs
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
        # print(f"ERROR 404: Asking for coordinates in {city_name} at {full_url}")
        raise Exception(f"City {city_name} not found at {full_url}!")
    return lat, lon

def get_weathers_aux(city_name, start_time, end_or_count = 169):
    """Get the weather data from the OpenWeatherMap API. end_or_count can either be a string with datetype or an integer with the number of hours to get the weather data."""
    api_key = API_KEY
    lat, lon = get_coordinates(city_name)
    start_time = date_to_ts(start_time)
    if type(end_or_count) == int:
        count = end_or_count
        full_url = f"https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type=hour&start={start_time}&cnt={count}&appid={api_key}"
    else:
        end = date_to_ts(end_or_count)
        full_url = f"https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type=hour&start={start_time}&end={end}&appid={api_key}"
    # print(full_url)
    response = requests.get(full_url)
    data = response.json()
    if data["cod"] != "200":
        print(f"ERROR {data['cod']} - Asking for weather in {city_name} at {full_url}")
        return None
    weathers = data["list"]
    return weathers

def get_weathers(city_name, start_time, count = 50): # 8760 hours num ano
    if type(count) == str: # Se for uma datetime string
        count = date_to_ts(count) - date_to_ts(start_time)
        count /= 3600
        fixup = count / 24
        count += fixup # Adiciona 1 dia por cada dia, para garantir que a data final é incluida
        count = int(count)
    cur_count = 0
    maximo = 169
    full_array = []
    while cur_count < count:
        cur_count += min(count - cur_count, maximo)
        weathers = get_weathers_aux(city_name, start_time, cur_count)
        full_array += weathers
        start_time = ts_to_date(weathers[-1]["dt"] + 3600).strftime("%Y-%m-%d %H:%M:%S") # Busca a ultima timestamp e adiciona 1 hora
    return full_array


def get_current_weather(city_name: str):
    full_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
    # print(full_url)
    response = requests.get(full_url)
    data = response.json()
    if str(data["cod"]) != "200":
        print(f"ERROR {data['cod']}: Asking for current weather in {city_name} at {full_url}")
        return None
    
    main_weather = data["weather"][0]["main"]
    return main_weather

def get_exact_past_weather(city_name: str, datetime_str: str):
    """Get the weather data from the OpenWeatherMap API. end_or_count can either be a string with datetype or an integer with the number of hours to get the weather data."""
    api_key = API_KEY
    lat, lon = get_coordinates(city_name)
    start_time = date_to_ts(datetime_str)
    full_url = f"https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type=hour&start={start_time}&cnt=1&appid={api_key}"
    # print(full_url)
    response = requests.get(full_url)
    data = response.json()
    if data["cod"] != "200":
        print(f"ERROR {data['cod']} - Asking for weather in {city_name} at {full_url}")
        return None
    weathers = data["list"]
    # print(weathers)
    return weathers[0]



#> Interpreta info das APIs

def weatherinfo_to_weather(weather_instance):
    weathers_list = weather_instance["weather"]
    final_weather = weathers_list[0]["main"]
    for w in weathers_list:
        weather_i = w["main"]
        if is_very_bad_weather_ow(weather_i):
            final_weather = weather_i
            break
    return final_weather

def weather_datetime(weather_instance):
    return ts_to_date(weather_instance["dt"])

#> Weather qualifiers
def is_bad_weather_ow(weather):
    # bad_conditions = ["Thunderstorm", "Snow", "Fog", "Haze", "Mist", "Smoke", "Dust", "Ash", "Squall", "Tornado"]
    bad_conditions = ["Clouds", "Smoke", "Mist", "Haze", "Dust", "Drizzle", "Fog", "Sand", "Rain", "Ash", "Squalls", "Squall", "Snow"] # Condições que atrasam descolagens e aterragens
    return weather in bad_conditions
    
def is_very_bad_weather_ow(weather):
    # very_bad_conditions = ["Thunderstorm", "Snow", "Squall", "Tornado", "Smoke"]
    very_bad_conditions = ["Thunderstorm", "Tornado", "Volcanic Ash"]
    return weather in very_bad_conditions


#> Conversores de data
def date_to_ts(d):
    return int(datetime.strptime(d, "%Y-%m-%d %H:%M:%S").timestamp())

def ts_to_date(ts):
    return datetime.fromtimestamp(ts)

#> Print functions
def print_very_bad_weathers(weathers):
    for weather_instance in weathers:
        weathers_list = weather_instance["weather"]
        for w in weathers_list:
            actual_weather = w["main"]
            if is_very_bad_weather_ow(actual_weather):
                print("-"*50)
                print(f"Datetime: {ts_to_date(weather_instance['dt'])}")
                weathers_ = [w["main"] for w in weathers_list]
                print(f"Weathers: {weathers_}")
                print("-"*50)
                break


if __name__ == "__main__":
    city_name = "Keflavik"
    city_name = "Dubai"
    start_time = "2024-04-16 10:00:00"

    weathers = get_weathers(city_name, start_time, count=12)
    for w in weathers:
        wi = weatherinfo_to_weather(w)
        print(wi)
    # print(weathers)
    print_very_bad_weathers(weathers)