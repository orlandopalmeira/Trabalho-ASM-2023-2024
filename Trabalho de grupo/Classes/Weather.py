
class Weather:
    def __init__(self, weather):
        self.weather = weather

    def get_weather(self) -> str:
        return self.weather
    
    def set_weather(self, weather):
        self.weather = weather
    
    def __str__(self):
        return f"{self.weather}"
