import requests
from datetime import datetime

API = "https://apidatos.ree.es/es/datos/mercados/precios-mercados-tiempo-real"
HEADERS = {"Accept": "application/json"}

def fetch_prices():
    hoy = datetime.now().date()
    start = hoy.isoformat() + "T00:00"
    end = hoy.isoformat() + "T23:59"
    params = {"start_date": start, "end_date": end, "time_trunc": "hour"}
    r = requests.get(API, params=params, headers=HEADERS)
    data = r.json()
    for item in data.get("included", []):
        if item.get("type") == "PVPC":
            values = item["attributes"]["values"]
            now = datetime.now()
            current = min(values, key=lambda v: abs(datetime.fromisoformat(v["datetime"][:-6])-now))
            sorted_vals = sorted(values, key=lambda v: v["value"])
            return {
                "values": values,
                "current": current,
                "min": sorted_vals[0],
                "max": sorted_vals[-1]
            }
    return {}
