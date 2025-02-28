import requests
import math
import os
from dotenv import load_dotenv

# Load API keys
load_dotenv()
OPENCELL_API_KEY = os.getenv("OPENCELL_API_KEY")

def fetch_network_towers(lat, lon):
    """Fetch network towers data from OpenCell API."""
    lat_diff = 0.0045
    lon_diff = 0.0045 / math.cos(math.radians(lat))

    latmin, latmax = lat - lat_diff, lat + lat_diff
    lonmin, lonmax = lon - lon_diff, lon + lon_diff

    url = f"https://www.opencellid.org/cell/getInArea?key={OPENCELL_API_KEY}&BBOX={latmin},{lonmin},{latmax},{lonmax}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return {}

def summarize_tower_data(tower_data):
    """Summarizes network tower data."""
    if "cells" in tower_data:
        num_towers = len(tower_data["cells"])
        radio_types = set(cell["radio"] for cell in tower_data["cells"])
        avg_range = sum(cell["range"] for cell in tower_data["cells"]) / num_towers if num_towers > 0 else 0
        summary = (
            f"📡 **Towers Found:** {num_towers}  \n"
            f"📶 **Network Types:** {', '.join(radio_types)}  \n"
            f"📏 **Avg Tower Range:** {int(avg_range)} meters"
        )
    else:
        summary = "⚠️ No tower data available."
    return summary
