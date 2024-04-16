from geopy.geocoders import Nominatim
from geopy.distance import geodesic

class GeoDistance:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="city_distance_calculator")

    def get_coordinates(self, city_name):
        location = self.geolocator.geocode(city_name)
        if location:
            return location.latitude, location.longitude
        else:
            print(f"Coordinates for {city_name} not found.")
            return None

    def calculate_distance(self, city1, city2):
        """Retorna a distância entre duas cidades em quilômetros. Caso haja um erro com o nome das cidades, retorna None."""
        coords1 = self.get_coordinates(city1)
        coords2 = self.get_coordinates(city2)

        if coords1 and coords2:
            distance = geodesic(coords1, coords2).kilometers
            distance = round(distance, 2)
        else:
            print(f"ERROR:({city1}-{city2}) Cannot calculate distance due to missing coordinates from one city.")
            distance = None
        return distance
    
    def ponto_progresso_caminho(self, cidade_A, cidade_B, progresso: float):
        # Obter as coordenadas geográficas das cidades A e B
        coordenadas_A = self.geolocator.geocode(cidade_A)
        coordenadas_B = self.geolocator.geocode(cidade_B)

        # Verificar se as coordenadas foram encontradas
        if coordenadas_A is None or coordenadas_B is None:
            return "Não foi possível encontrar as coordenadas para uma ou ambas as cidades fornecidas."

        # Extrair as coordenadas das cidades A e B
        coordenadas_A = (coordenadas_A.latitude, coordenadas_A.longitude)
        coordenadas_B = (coordenadas_B.latitude, coordenadas_B.longitude)

        # Calcular a distância total entre A e B
        distancia_total = geodesic(coordenadas_A, coordenadas_B).kilometers

        # Calcular a distância correspondente a 80% do caminho
        distancia_80_percento = progresso * distancia_total

        # Calcular a proporção do caminho em relação à distância total
        proporcao = distancia_80_percento / distancia_total

        # Calcular as coordenadas do ponto 80% do caminho
        latitude_80_percento = coordenadas_A[0] + proporcao * (coordenadas_B[0] - coordenadas_A[0])
        longitude_80_percento = coordenadas_A[1] + proporcao * (coordenadas_B[1] - coordenadas_A[1])

        # Retornar as coordenadas do ponto 80% do caminho
        return latitude_80_percento, longitude_80_percento

    def get_name_by_coords(self, latitude, longitude):
        # Tentar obter o nome da cidade com base nas coordenadas fornecidas
        try:
            localizacao = self.geolocator.reverse((latitude, longitude), language="pt") 
            cidade = localizacao.raw['address']['city']
            if cidade:
                return cidade
            else:
                return localizacao.raw['address']['town']
        except Exception as e:
            print("Erro ao obter o nome da cidade:", e)
            return None

if __name__ == "__main__":
    gd = GeoDistance()
    city1 = "Cabeceiras de Basto"
    city2 = "Nova Zelândia"
    distance = gd.calculate_distance(city1, city2)
    print(f"The distance between {city1} and {city2} is approximately {distance} kilometers.")
