from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json
import math

app = Flask(__name__)
CORS(app)

# Load museum data from museums.json
with open('museums.json', 'r') as f:
    museums = json.load(f)

# Load restaurant data from restaurants.json (assumed to be loaded already)
with open('restaurants.json', 'r') as f:
    restaurants = json.load(f)


# Haversine formula to calculate distance between two points on Earth's surface
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Radius of Earth in kilometers

    lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
    lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

# Find the nearest restaurant based on Haversine distance
def find_nearest_restaurant(latitude, longitude):
    nearest_restaurant = None
    min_distance = float('inf')

    for restaurant in restaurants:
        rest_lat = restaurant['location']['latitude']
        rest_lon = restaurant['location']['longitude']

        distance = haversine(latitude, longitude, rest_lat, rest_lon)

        if distance < min_distance:
            min_distance = distance
            nearest_restaurant = restaurant

    return nearest_restaurant


# Find the nearest museum based on the user's location
def find_nearest_museum(latitude, longitude):
    nearest_museum = None
    min_distance = float('inf')

    for museum in museums:
        museum_lat = museum['location']['latitude']
        museum_lon = museum['location']['longitude']
        distance = haversine(latitude, longitude, museum_lat, museum_lon)
        
        if distance < min_distance:
            min_distance = distance
            nearest_museum = museum

    return nearest_museum

# Determine the appropriate menu based on the time
def get_menu_by_time(time_str):
    time = datetime.strptime(time_str, "%H:%M").time()
    if time < datetime.strptime("11:00", "%H:%M").time():
        return "breakfast"
    elif time < datetime.strptime("16:00", "%H:%M").time():
        return "lunch"
    else:
        return "dinner"

# Check if the museum is open at the given time
def is_museum_open(museum, current_time):
    opening_time = datetime.strptime(museum['opening_time'], "%H:%M").time()
    closing_time = datetime.strptime(museum['closing_time'], "%H:%M").time()
    
    return opening_time <= current_time <= closing_time

# API endpoint to get the menu based on location and time
@app.route('/qrapi/get_menu', methods=['GET'])
def get_menu():
    latitude = request.args.get('latitude', type=float)
    longitude = request.args.get('longitude', type=float)
    time_str = request.args.get('time')

    if not latitude or not longitude or not time_str:
        return jsonify({"error": "latitude, longitude, and time are required"}), 400

    restaurant = find_nearest_restaurant(latitude, longitude)
    menu_type = get_menu_by_time(time_str)
    menu = restaurant["menus"].get(menu_type, [])

    api_response = {
        "restaurant": restaurant["name"],
        "location": restaurant["location"],
        "menu_type": menu_type,
        "menu": menu
    }

    response = {
        "private": {
            "Time": time_str,
            "Location": {
                "Latitude": latitude,
                "Longitude": longitude,
            }
        },
        "public": {
            "qr": "https://dynamic-qr-blue.vercel.app/qrapi/get_menu",
        },
        "response": api_response,
    }

    return jsonify(response)

# API endpoint to find the nearest museum and its opening status
@app.route('/qrapi/nearest_museum', methods=['GET'])
def get_nearest_museum():
    latitude = request.args.get('latitude', type=float)
    longitude = request.args.get('longitude', type=float)
    time_str = request.args.get('time')


    if not latitude or not longitude or not time_str:
        return jsonify({"error": "latitude, longitude, and time are required"}), 400
    
    current_time = datetime.strptime(time_str, "%H:%M").time()
    # Find the nearest museum
    nearest_museum = find_nearest_museum(latitude, longitude)
    
    # Check if the museum is open
    is_open = is_museum_open(nearest_museum, current_time)
    status = "Open" if is_open else "Closed"

    api_response = {
        "museum": nearest_museum['name'],
        "address": nearest_museum['address'],
        "description": nearest_museum['description'],
        "currently_open": status,
        "opening_time": nearest_museum['opening_time'],
        "closing_time": nearest_museum['closing_time'],
        "entrance_fee": nearest_museum['entrance_fee']
    }

    response = {
        "private": {
            "Time": time_str,
            "Location": {
                "Latitude": latitude,
                "Longitude": longitude,
            }
        },
        "public": {
            "qr": "https://dynamic-qr-blue.vercel.app/qrapi/nearest_museum",
        },
        "response": api_response,
    }

    return jsonify(response)

