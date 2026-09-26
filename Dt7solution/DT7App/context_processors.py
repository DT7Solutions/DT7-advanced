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

from django.core.cache import cache

def get_lat_lng_from_ip(ip):
    """
    Convert IP -> lat/lng using ipapi (Cached for 24h to avoid blocking page load)
    """
    if not ip or ip in ("127.0.0.1", "localhost", "::1"):
        return None, None
        
    cache_key = f"ip_lat_lng_{ip}"
    cached_coords = cache.get(cache_key)
    if cached_coords is not None:
        return cached_coords

    try:
        response = requests.get(f"https://ipapi.co/{ip}/json/", timeout=0.5)
        if response.status_code == 200:
            data = response.json()
            coords = (data.get("latitude"), data.get("longitude"))
            cache.set(cache_key, coords, 86400)  # Cache for 24 hours
            return coords
    except Exception:
        pass
        
    # Store negative cache briefly (5 mins) to prevent spamming failed external API
    cache.set(cache_key, (None, None), 300)
    return None, None


# ----------------------------- Updated list of valid cities for URL slug ----------------------------- #
VALID_CITIES = [
    # Andhra Pradesh
    "visakhapatnam", "vizianagaram", "srikakulam", "vijayawada", "guntur",
    "amaravathi", "nellore", "tirupati", "kurnool", "anantapur",
    "rajahmundry", "kakinada", "eluru", "ongole", "kadapa", "chittoor",
    # Telangana
    "hyderabad", "secunderabad", "warangal", "nizamabad", "karimnagar",
    "khammam", "mahbubnagar", "ramagundam", "medak", "nalgonda", "adilabad"
]

def location_data(request):
    """
    FINAL LOGIC:
    1. Cookie (PRIMARY)
    2. URL slug (SECONDARY)
    3. IP fallback (with nearest city within 50 km)
    4. guntur (DEFAULT)
    """
    # 1️⃣ Cookie first
    city = request.COOKIES.get("user_city")
    if city:
        return {"city": city}

    # 2️⃣ URL slug (only if valid city)
    try:
        path_parts = request.path.strip("/").split("/")
        if path_parts and path_parts[0].lower() in VALID_CITIES:
            return {"city": path_parts[0].lower()}
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
