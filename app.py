import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

API_KEY = os.getenv("CLEVER_API_KEY")
GET_ROUTES_URL = "https://riderts.app/bustime/api/v3/getroutes"
GET_STOPS_URL = "https://riderts.app/bustime/api/v3/getstops"

@app.route("/", methods=["GET", "POST"])
def index():
    routes = []
    stops = []
    error = None

    # Get available routes from API
    try:
        route_res = requests.get(GET_ROUTES_URL, params={"key": API_KEY, "format": "json"})
        routes = route_res.json().get("bustime-response", {}).get("routes", [])
    except Exception as e:
        error = f"Error loading routes: {e}"

    # Handle form submission to get stops
    if request.method == "POST":
        route_id = request.form.get("route_id")
        print("🟢 Route selected:", route_id)

        try:
            stop_res = requests.get(
                GET_STOPS_URL,
                params={"key": API_KEY, "rt": route_id, "format": "json"}
            )
            stops = stop_res.json().get("bustime-response", {}).get("stops", [])
            if not stops:
                error = stop_res.json().get("bustime-response", {}).get("error", [{"msg": "No stops found"}])[0]["msg"]
        except Exception as e:
            error = f"Error fetching stops: {e}"

    return render_template("index.html", routes=routes, stops=stops, error=error)
