import requests
from .location_utils import get_nearest_city

def get_client_ip(request):
    """
    Get real client IP (proxy safe)
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")

def get_lat_lng_from_ip(ip):
    """
    Convert IP → lat/lng using ipapi
    Used ONLY as fallback when slug is missing
    """
    try:
        response = requests.get(f"https://ipapi.co/{ip}/json/", timeout=2)
        if response.status_code == 200:
            data = response.json()
            return data.get("latitude"), data.get("longitude")
    except Exception:
        pass
    return None, None

def location_data(request):
    """
    FINAL LOGIC:
    1. Cookie (PRIMARY)
    2. URL slug (SECONDARY)
    3. IP fallback
    4. guntur
    """
    # 1️⃣ Cookie first
    city = request.COOKIES.get("user_city")
    if city:
        return {"city": city}
    # 2️⃣ URL slug (ONLY if valid city)
    try:
        path_parts = request.path.strip("/").split("/")
        if path_parts and path_parts[0] in [
            "guntur", "hyderabad", "vijayawada",
            "visakhapatnam", "nellore", "tirupati",
            "kurnool", "rajahmundry", "kakinada",
            "eluru", "ongole", "secunderabad",
            "warangal", "nizamabad", "karimnagar",
            "khammam", "mahbubnagar"
        ]:
            return {"city": path_parts[0]}
    except Exception:
        pass
    # 3️⃣ IP fallback
    try:
        ip = get_client_ip(request)
        lat, lng = get_lat_lng_from_ip(ip)
        if lat and lng:
            return {"city": get_nearest_city(lat, lng)}
    except Exception:
        pass
    # 4️⃣ Final fallback
    return {"city": "guntur"}
