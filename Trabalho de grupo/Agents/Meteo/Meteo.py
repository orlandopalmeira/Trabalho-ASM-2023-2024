from spade.agent import Agent

from Agents.Meteo.Behaviors.SendMeteo import SendMeteo
from Agents.Meteo.Behaviors.SendMeteoFromFile import SendMeteoFromFile
from Agents.Meteo.MeteoAPI import date_to_ts, ts_to_date

from Config import Config as cfg
from Utils.Prints import print_c
from interface import logs_color

import json
import time

class Meteo(Agent):
    MODE_PAST = "past"
    MODE_CURRENT = "current"
    MODE_MANUAL = "manual"
    
    def __init__(self, jid, password, cities, mode, datetime = None, period = 30): # Timestamp indica a partir de que altura se quer a meteorologia, se corrido em "past" mode
        super().__init__(jid, password)
        self.cities = cities
        self.mode = mode

        self.cur_datetime = datetime
        self.period = period # Frequência de envio de informação em segundos

    def print(self, msg, color = "black"):
        unix_ts = time.time()
        ts = time.strftime('%H:%M:%S', time.localtime(unix_ts))
        print_c(f"({ts}) {self.name}: {msg}", color)
        logs_color(f"({ts}) {self.name}: {msg}", color)

    async def setup(self):
        self.print(f'starting...', "dark blue")
        if self.get_mode() == Meteo.MODE_MANUAL:
            # Escrever ficheiro
            cities_weather = {}
            for city in self.cities:
                weather = "Clear"
                cities_weather[city] = weather
            meteo_file_name = cfg.meteo_file_name()
            with open(meteo_file_name, 'w') as meteo_file:
                json.dump(cities_weather, meteo_file, indent=4)
            # Começar behaviour de leitura de ficheiro para obtenção de weathers
            self.add_behaviour(SendMeteoFromFile(1))
        else:
            self.add_behaviour(SendMeteo(self.period))

    def get_mode(self):
        return self.mode
    
    def next_datetime(self, hours = 1):
        """Avança 1 hora na datetime corrente"""
        seconds = hours * 3600
        ts = date_to_ts(self.cur_datetime) + seconds
        self.cur_datetime = ts_to_date(ts).strftime("%Y-%m-%d %H:%M:%S")
