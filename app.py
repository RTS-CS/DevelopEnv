import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# Load API key and URLs from environment
API_KEY = os.getenv("CLEVER_API_KEY")
GET_ROUTES_URL = "https://riderts.app/bustime/api/v3/getroutes"
GET_STOPS_URL = "https://riderts.app/bustime/api/v3/getstops"

@app.route("/", methods=["GET", "POST"])
def index():
    routes = []
    stops = []
    error = None

    # Load all routes
    try:
        route_res = requests.get(GET_ROUTES_URL, params={"key": API_KEY, "format": "json"})
        routes = route_res.json().get("bustime-response", {}).get("routes", [])
    except Exception as e:
        error = f"Error loading routes: {e}"
        return render_template("index.html", routes=routes, stops=stops, error=error)

    # If user submitted the form
    if request.method == "POST":
        route_id = request.form.get("route_id")
        print("🟢 Route selected:", route_id)

        try:
            params = {"key": API_KEY, "rt": route_id, "format": "json"}
            print("🔐 Using API key:", API_KEY)
            print("🔗 Calling GET_STOPS_URL:", GET_STOPS_URL)
            print("📦 Params:", params)

            stop_res = requests.get(GET_STOPS_URL, params=params)

            print("📡 Full request URL:", stop_res.url)
            print("📨 API response:", stop_res.text)

            stops = stop_res.json().get("bustime-response", {}).get("stops", [])
            if not stops:
                error = stop_res.json().get("bustime-response", {}).get("error", [{"msg": "No stops found"}])[0]["msg"]

        except Exception as e:
            error = f"Error fetching stops: {e}"

    return render_template("index.html", routes=routes, stops=stops, error=error)

# Optional health check endpoint
@app.route("/healthz")
def health_check():
    return "OK", 200
