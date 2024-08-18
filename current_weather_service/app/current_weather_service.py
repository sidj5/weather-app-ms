from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"
WEATHER_API_KEY = "b92ee1d9f0faa2f02a4d512e5d027fd3"

@app.route("/current-weather", methods=["GET"])
def current_weather():
    city = request.args.get("city")
    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }
    response = requests.get(WEATHER_API_URL, params=params)
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
