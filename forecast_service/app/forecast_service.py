from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

HISTORICAL_WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/forecast"
WEATHER_API_KEY = "b92ee1d9f0faa2f02a4d512e5d027fd3"

@app.route("/historical-weather", methods=["GET"])
def historical_weather():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    dt = request.args.get("dt")
    params = {
        "lat": lat,
        "lon": lon,
        "dt": dt,
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }
    response = requests.get(HISTORICAL_WEATHER_API_URL, params=params)
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
