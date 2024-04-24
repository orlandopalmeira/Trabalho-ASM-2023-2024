from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy.exc import GeocoderTimedOut

from Utils.Prints import *

#! Talvez estas funcionalidades pudessem ir para dentro da classe Trip


def geocode_city(city_name):
    """Alternativa a geolocator.geocode(city_name) com retries para tentar resolver problema dos timeouts."""
    geocoder = Nominatim(user_agent="my_geocoder")
    max_retries = 3
    retry_count = 0
    while retry_count < max_retries:
        try:
            location = geocoder.geocode(city_name)
            return location
        except GeocoderTimedOut:
            retry_count += 1
            print_warning("Geocoder service timed out. Retrying...")
    print_error("Unable to geocode the location after multiple attempts.")
    return None

def get_coordinates(city_name):
    location = geocode_city(city_name)
    if location:
        return location.latitude, location.longitude
    else:
        print_error(f"Coordinates for {city_name} not found.")
        return None

def calculate_distance(city1, city2):
    """Retorna a distância entre duas cidades em quilômetros. Caso haja um erro com o nome das cidades, retorna None."""
    coords1 = get_coordinates(city1)
    coords2 = get_coordinates(city2)

    if coords1 and coords2:
        distance = geodesic(coords1, coords2).kilometers
        distance = round(distance, 2)
    else:
        print_error(f"ERROR:({city1}-{city2}) Cannot calculate distance due to missing coordinates from one city.")
        distance = None
    return distance

def ponto_progresso_caminho(cidade_A, cidade_B, progresso: float):
    # Obter as coordenadas geográficas das cidades A e B
    coordenadas_A = geocode_city(cidade_A)
    coordenadas_B = geocode_city(cidade_B)

    # Verificar se as coordenadas foram encontradas
    if coordenadas_A is None or coordenadas_B is None:
        print_error("Não foi possível encontrar as coordenadas para uma ou ambas as cidades fornecidas.")
        return None

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

def get_name_by_coords(latitude, longitude):
    # Tentar obter o nome da cidade com base nas coordenadas fornecidas
    geolocator = Nominatim(user_agent="GeoDistance")
    try:
        localizacao = geolocator.reverse((latitude, longitude), language="pt") 
        cidade = localizacao.raw['address']['city']
        if cidade:
            return cidade
        else:
            return localizacao.raw['address']['town']
    except Exception as e:
        print_error("Erro ao obter o nome da cidade:", e)
        return None

if __name__ == "__main__":
    geolocator = Nominatim(user_agent="GeoDistance")
    city1 = "Cabeceiras de Basto"
    city2 = "Nova Zelândia"
    distance = geolocator.calculate_distance(city1, city2)
    print(f"The distance between {city1} and {city2} is approximately {distance} kilometers.")
