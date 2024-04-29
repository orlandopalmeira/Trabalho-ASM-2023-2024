from random import random
from spade.agent import Agent

from Agents.Meteo.Behaviors.SendMeteo import SendMeteo

from Config import Config as cfg
from Utils.Prints import *

import requests, os



class Meteo(Agent):
    # API_KEY = "c5edae66c459cb80a6c09d9aacea3e2c" # OpenWeatherMap API key - base
    API_KEY=os.getenv("API_KEY")

    
    def __init__(self, jid, password, cities, timestamp = None): # Timestamp indica periodo de tempo que quer simular
        super().__init__(jid, password)
        self.cities = cities
        self.timestamp = timestamp

    def print(self, msg):
        print(f"{self.name}: {msg}")

    async def setup(self):
        print(f'{self.name} starting...')
        self.add_behaviour(SendMeteo())

    def get_coordinates(self, city_name):
        api_key = self.API_KEY
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        full_url = base_url + "appid=" + api_key + "&q=" + city_name
        response = requests.get(full_url)
        data = response.json()
        if data["cod"] != "404":
            coordinates = data["coord"]
            lat = coordinates["lat"]
            lon = coordinates["lon"]
        else:
            print_error(f"ERROR 404: Asking for coordinates in {city_name} at {full_url}")
        return lat, lon

    def get_weather(self, city_name, start = "2024-03-06", end = "2024-03-08"):
        """Open-meteo API."""
        api_key = self.API_KEY
        lat, lon = self.get_coordinates(city_name)
        # url_example = f"https://history.openweathermap.org/data/3.0/history/timemachine?lat=51.51&lon=-0.13&dt=606348800&appid={api_key}"
        full_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=weather_code&start_date={start}&end_date={end}"
        response = requests.get(full_url)
        data = response.json()
        if data["cod"] == "404":
            print_error(f"ERROR 404: Asking for weather in {city_name} at {full_url}")
            return None
        weather = data["hourly"]["weather_code"]
        return weather
    
    def get_weather_ow(self, city_name, datetime = None):
        """OpenWeatherMap API."""
        api_key = self.API_KEY
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        graus = "&units=metric"
        full_url = base_url + "appid=" + api_key + "&q=" + city_name + graus
        response = requests.get(full_url)
        data = response.json()
        if data["cod"] == "404":
            print_error(f"ERROR 404: Asking for weather in {city_name} at {full_url}")
            return None
        weather = data["weather"][0]
        tempo = weather["main"]

        return tempo
    
    def get_current_weather(self, city_name):
        api_key = self.API_KEY
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        graus = "&units=metric"
        full_url = base_url + "appid=" + api_key + "&q=" + city_name + graus
        response = requests.get(full_url)
        data = response.json()
        if data["cod"] == "404":
            print(f"ERROR 404: Asking for weather in {city_name} at {full_url}")
        weather = data["weather"][0]
        tempo = weather["main"]

        return tempo
    
    
    def is_bad_weather_ow(weather):
        """For OpenWeatherMap API."""
        bad_conditions = ["Thunderstorm", "Snow", "Fog", "Haze", "Mist", "Smoke", "Dust", "Ash", "Squall", "Tornado"]

        return weather in bad_conditions
    
    def is_bad_weather(wmo_code):
        """For open-meteo API. Returns True if the weather is bad for plane takeoffs, False otherwise."""
        # WMO codes indicating bad weather for plane takeoffs
        bad_weather_codes = [45, 48, 51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 71, 73, 75, 77, 80, 81, 82, 85, 86, 95, 96, 99]

        return wmo_code in bad_weather_codes

    def interpret_weather(wmo_code):
        weather_dict = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Fog",
            48: "Depositing rime fog",
            51: "Drizzle (light)",
            53: "Drizzle (moderate)",
            55: "Drizzle (dense)",
            56: "Freezing drizzle (light)",
            57: "Freezing drizzle (dense)",
            61: "Rain (slight)",
            63: "Rain (moderate)",
            65: "Rain (heavy)",
            66: "Freezing rain (light)",
            67: "Freezing rain (heavy)",
            71: "Snow fall (slight)",
            73: "Snow fall (moderate)",
            75: "Snow fall (heavy)",
            77: "Snow grains",
            80: "Rain showers (slight)",
            81: "Rain showers (moderate)",
            82: "Rain showers (violent)",
            85: "Snow showers (slight)",
            86: "Snow showers (heavy)",
            95: "Thunderstorm (slight or moderate)",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail"
        }

        return weather_dict[wmo_code]

        

if __name__ == "__main__":
    cities = ["braga", "porto", "lisboa", "faro"]
    meteo = Meteo("meteo@localhost", "1234", cities)
    for city in meteo.cities:
        print(f"City: {city}")
        print(f"Weather: {meteo.get_weather(city)}")
        print()
    # print(meteo.get_weather("braga"))