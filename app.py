from flask import Flask, render_template, request
import requests
from geopy.geocoders import Nominatim

app = Flask(__name__)

def get_lat_lon(city_name):
    """Convert city name to latitude and longitude using Geopy."""
    geolocator = Nominatim(user_agent="weather_app")
    location = geolocator.geocode(city_name)
    if location:
        return location.latitude, location.longitude
    return None, None

def get_weather(lat, lon):
    """Fetch weather data from Open-Meteo API."""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json().get("current_weather", {})
        return {
            "temperature": f"{data.get('temperature', 'N/A')}°C",
            "windspeed": f"{data.get('windspeed', 'N/A')} km/h",
            "condition": data.get("weathercode", "Unknown")
        }
    return None

@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    city = ""

    if request.method == "POST":
        city = request.form["city"]
        lat, lon = get_lat_lon(city)

        if lat is not None and lon is not None:
            weather = get_weather(lat, lon)

    return render_template("index.html", city=city, weather=weather)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
