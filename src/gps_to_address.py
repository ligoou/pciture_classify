import requests

def gps_to_address_google(gps_data):
    api_key = "YOUR_GOOGLE_MAPS_API_KEY"
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "latlng": f"{gps_data['GPSLatitude']},{gps_data['GPSLongitude']}",
        "key": api_key
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    if data["status"] == "OK":
        address = data["results"][0]["formatted_address"]
        return address
    else:
        return None

def gps_to_address_openstreetmap(gps_data):
    base_url = "https://nominatim.openstreetmap.org/reverse"
    lat = float(gps_data['GPSLatitude'][0]) + float(gps_data['GPSLatitude'][1]) / 60 + float(
        gps_data['GPSLatitude'][2]) / 3600
    lon = float(gps_data['GPSLongitude'][0]) + float(gps_data['GPSLongitude'][1]) / 60 + float(
        gps_data['GPSLongitude'][2]) / 3600
    print(f"lat: {lat}, lon: {lon}")
    params = {
        "format": "geocodejson",
        "lat": lat,
        "lon": lon,
        "addressdetails": 1,
        "accept-language": "zh",
        "zoom": 8,
        "limit": 1
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Priority": "u=0, i",
        "Sec-CH-UA": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "Sec-CH-UA-Mobile": "?0",
        "Sec-CH-UA-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1"
    }
    response = requests.get(base_url, params=params, headers=headers)
    print(f"Response status code: {response}")
    data = response.json()
    if "features" in data and len(data["features"]) > 0:
        address = data['features'][0]['properties']['geocoding']['label']
        print(address)
    else:
        return None
