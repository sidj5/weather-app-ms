from flask import Flask, render_template, request
import requests
import time

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.template_filter('datetimeformat')
def datetimeformat(value, format='%Y-%m-%d'):
    return time.strftime(format, time.localtime(value))

CURRENT_WEATHER_SERVICE_URL = "http://current_weather_service:5001/current-weather"
HISTORICAL_WEATHER_SERVICE_URL = "http://forecast_weather_service:5002/historical-weather"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/weather", methods=["POST"])
def weather():
    start_time = time.time()
    city = request.form["city"]

    # Fetch current weather data
    current_weather_response = requests.get(CURRENT_WEATHER_SERVICE_URL, params={"city": city})
    data = current_weather_response.json()

     # Calculate server latency
    server_latency = time.time() - start_time  # Calculate the server processing time

    if "main" in data and "temp" in data["main"] and "weather" in data and len(data["weather"]) > 0:
        weather_info = {
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "server_latency": server_latency  # Include server latency in the response
        }

        # Extract latitude and longitude for historical data
        lat = data["coord"]["lat"]
        lon = data["coord"]["lon"]

        # Fetch historical weather data
        historical_data = []
        for i in range(1, 2):
            timestamp = int(time.time()) - i * 86400
            historical_response = requests.get(HISTORICAL_WEATHER_SERVICE_URL, params={
                "lat": lat,
                "lon": lon,
                "dt": timestamp
            })
            historical_data.extend(historical_response.json().get("list", []))

        return render_template("index.html", weather=weather_info, historical_data=historical_data)
    else:
        error_message = "Failed to retrieve weather information for the specified city."
        return render_template("index.html", error=error_message, server_latency=server_latency)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
