import urllib.request
import json

SPOT_ID = "584204204e65fad6a77099d5" # Fonte da Telha

def fetch_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
        "Origin": "https://www.surfline.com",
        "Referer": "https://www.surfline.com/"
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

try:
    wave_url = f"https://services.surfline.com/kbyg/spots/forecasts/wave?spotId={SPOT_ID}&days=5&intervalHours=24"
    wind_url = f"https://services.surfline.com/kbyg/spots/forecasts/wind?spotId={SPOT_ID}&days=5&intervalHours=24"
    
    wave_data = fetch_data(wave_url)["data"]["wave"]
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
