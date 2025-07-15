import os
import json
import requests
from flask import Flask, render_template, send_file

app = Flask(__name__)

API_KEY = os.getenv("CLEVER_API_KEY", "7GqnDentpEHC9wjD7jeSvP7P6")
GET_ROUTES_URL = "https://riderts.app/bustime/api/v3/getroutes"
GET_VEHICLES_URL = "https://riderts.app/bustime/api/v3/getvehicles"

@app.route("/")
def index():
    data = collect_data()
    return render_template("index.html", data=data)

@app.route("/download")
def download_json():
    return send_file("stops_by_route.json", as_attachment=True)

def collect_data():
    output = {}
    try:
        route_res = requests.get(GET_ROUTES_URL, params={"key": API_KEY, "format": "json"})
        routes = route_res.json().get("bustime-response", {}).get("routes", [])
    except Exception as e:
        return {"error": f"Failed to fetch routes: {e}"}

    for route in routes:
        rt_id = route["rt"]
        try:
            vehicle_res = requests.get(GET_VEHICLES_URL, params={"key": API_KEY, "format": "json", "rt": rt_id})
            vehicles = vehicle_res.json().get("bustime-response", {}).get("vehicle", [])
            stops = {}
            for v in vehicles:
                stpid = v.get("stpid")
                stpnm = v.get("stpnm")
                if stpid and stpnm:
                    stops[stpid] = stpnm
            output[rt_id] = {"route_name": route["rtnm"], "stops": stops}
        except:
            continue

    with open("stops_by_route.json", "w") as f:
        json.dump(output, f, indent=2)

    return output
