import requests

def get_travel_options(start, destination, travel_mode):
    # API calls to Google Maps, etc.
    response = requests.get(f"https://maps.googleapis.com/maps/api/directions/json?origin={start}&destination={destination}&mode={travel_mode}")
    return response.json()

def get_nearest_bus_stop(location):
    # Mockup API to fetch nearest bus stops
    return {"stop_name": "Example Bus Stop", "arrival_times": ["5 mins", "10 mins"]}
