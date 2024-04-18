import random

def generate_random_trip(locations):
    origin = random.choice(locations)
    destination = random.choice(locations)
    while destination == origin:
        destination = random.choice(locations)
    return (origin, destination)

def generate_random_trips(locations, num_trips):
    trips = []
    for _ in range(num_trips):
        trip = generate_random_trip(locations)
        trips.append(trip)
    return trips

if __name__ == "__main__":
    locations = ["New York", "Los Angeles", "Chicago", "San Francisco", "Seattle", "Boston"]

    random_trips = generate_random_trips(locations, 5)

    for trip in random_trips:
        print(trip)
