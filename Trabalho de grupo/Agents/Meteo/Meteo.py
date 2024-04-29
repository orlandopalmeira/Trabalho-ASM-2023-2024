from spade.agent import Agent

from Agents.Meteo.Behaviors.SendMeteo import SendMeteo

from Config import Config as cfg
from Utils.Prints import *

from random import random
import requests, os
from datetime import datetime

# API_KEY = "c5edae66c459cb80a6c09d9aacea3e2c" # OpenWeatherMap API key - base
API_KEY=os.getenv("API_KEY")


class Meteo(Agent):
    
    def __init__(self, jid, password, cities, timestamp = None): # Timestamp indica periodo de tempo que quer simular
        super().__init__(jid, password)
        self.cities = cities
        self.timestamp = timestamp

    def print(self, msg):
        print(f"{self.name}: {msg}")

    async def setup(self):
        print(f'{self.name} starting...')
        self.add_behaviour(SendMeteo())

#* Obtem info das APIs
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
    if data["cod"] in ["404", "400", "401", "429", "500", "503", "504"]:
        print(f"ERROR {data['cod']}: Asking for weather in {city_name} at {full_url}")
    weathers = data["list"]
    return weathers

def get_weathers(city_name, start_time, count): # 8760 hours num ano
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


#* Interpreta info das APIs
def weathers_to_bool(weathers):
    """Transforms the weather data to a boolean value. If True it means that the weather is good. Else should be bad."""
    res = []
    for weather_instance in weathers:
        veredict = True
        weathers_list = weather_instance["weather"]
        for w in weathers_list:
            actual_weather = w["main"]
            if is_bad_weather_ow(actual_weather):
                veredict = False
                print(weathers_list)
                break
        res.append(veredict)
    return res

def weathers_to_weathers(weathers):
    res = []
    for weather_instance in weathers:
        weathers_list = weather_instance["weather"]
        final_weather = weathers_list[0]["main"]
        for w in weathers_list:
            weather_i = w["main"]
            if is_bad_weather_ow(weather_i):
                final_weather = weather_i
                break
        res.append(final_weather)
    return res

#* Conversores de data
def date_to_ts(d):
    return int(datetime.strptime(d, "%Y-%m-%d %H:%M:%S").timestamp())

def ts_to_date(ts):
    return datetime.fromtimestamp(ts)


#* Weather qualifiers
def is_bad_weather_ow(weather):
    bad_conditions = ["Thunderstorm", "Snow", "Fog", "Haze", "Mist", "Smoke", "Dust", "Ash", "Squall", "Tornado"]
    return weather in bad_conditions
    
def is_very_bad_weather_ow(weather):
    very_bad_conditions = ["Thunderstorm", "Snow", "Squall", "Tornado", "Smoke"]
    return weather in very_bad_conditions


#* Print functions
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
    cities = ["braga", "porto", "lisboa", "faro"]
    meteo = Meteo("meteo@localhost", "1234", cities)
    for city in meteo.cities:
        print(f"City: {city}")
        print(f"Weather: {meteo.get_weather(city)}")
        print()
    # print(meteo.get_weather("braga"))