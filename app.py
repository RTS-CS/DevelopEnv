import os
import requests
from flask import Flask, request, render_template

app = Flask(__name__)

API_KEY = os.getenv("CLEVER_API_KEY", "your-default-api-key")
BASE_URL = os.getenv("CLEVER_API_URL", "https://rtstransit.com/bustime/api/v3/getstops")

@app.route("/", methods=["GET", "POST"])
def index():
    stops = []
    route_id = ""
    error = None

    if request.method == "POST":
        route_id = request.form.get("route_id")
        if route_id:
            params = {
                "key": API_KEY,
                "rt": route_id,
                "format": "json"
            }
            try:
                response = requests.get(BASE_URL, params=params)
                data = response.json()

                if "stops" in data:
                    stops = data["stops"]
                else:
                    error = data.get("error", [{"msg": "No stops found"}])[0]["msg"]
            except Exception as e:
                error = str(e)

    return render_template("index.html", stops=stops, route_id=route_id, error=error)

if __name__ == "__main__":
    app.run(debug=True)
