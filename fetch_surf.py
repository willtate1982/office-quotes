import urllib.request
import urllib.parse
import json
import os
import sys

SPOT_ID = "584204204e65fad6a77099d5" # Fonte da Telha
API_KEY = os.environ.get("SCRAPER_API_KEY")

if not API_KEY:
    print("Error: SCRAPER_API_KEY environment variable is missing.")
    sys.exit(1)

def fetch_data(target_url):
    # Package the Surfline URL to be routed through ScraperAPI
    encoded_url = urllib.parse.quote(target_url)
    scraper_url = f"http://api.scraperapi.com?api_key={API_KEY}&url={encoded_url}"
    
    req = urllib.request.Request(scraper_url)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

try:
    wave_url = f"https://services.surfline.com/kbyg/spots/forecasts/wave?spotId={SPOT_ID}&days=5&intervalHours=24"
    wind_url = f"https://services.surfline.com/kbyg/spots/forecasts/wind?spotId={SPOT_ID}&days=5&intervalHours=24"
    
    print("Fetching wave data through proxy...")
    wave_data = fetch_data(wave_url)["data"]["wave"]
    
    print("Fetching wind data through proxy...")
    wind_data = fetch_data(wind_url)["data"]["wind"]
    
    forecast_list = []
    for i in range(min(5, len(wave_data))):
        speed_knots = wind_data[i].get("speed", 0)
        forecast_list.append({
            "timestamp": wave_data[i]["timestamp"],
            "wave": wave_data[i]["surf"]["max"],
            "period": wave_data[i]["swells"][0]["period"],
            "wind": round(speed_knots * 1.852, 1)
        })
        
    output = {"forecast": forecast_list}
    
    with open("surf.json", "w") as f:
        json.dump(output, f, indent=2)
        
    print("Successfully generated surf.json")
    
except Exception as e:
    print(f"Error fetching data: {e}")
    sys.exit(1)
