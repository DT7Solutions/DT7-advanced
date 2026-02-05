import math

# ----------------------------- Andhra Pradesh Major Cities ----------------------------- #
ANDHRA_PRADESH_CITIES = [
    {"name": "visakhapatnam", "lat": 17.6868, "lng": 83.2185},
    {"name": "vijayawada", "lat": 16.5062, "lng": 80.6480},
    {"name": "guntur", "lat": 16.3067, "lng": 80.4365},
    {"name": "nellore", "lat": 14.4426, "lng": 79.9865},
    {"name": "tirupati", "lat": 13.6288, "lng": 79.4192},
    {"name": "kurnool", "lat": 15.8281, "lng": 78.0373},
    {"name": "rajahmundry", "lat": 17.0005, "lng": 81.8040},
    {"name": "kakinada", "lat": 16.9891, "lng": 82.2475},
    {"name": "eluru", "lat": 16.7107, "lng": 81.0952},
    {"name": "ongole", "lat": 15.5057, "lng": 80.0499},
]

# ----------------------------- Telangana Major Cities ----------------------------- #
TELANGANA_CITIES = [
    {"name": "hyderabad", "lat": 17.3850, "lng": 78.4867},
    {"name": "secunderabad", "lat": 17.4399, "lng": 78.4983},
    {"name": "warangal", "lat": 17.9689, "lng": 79.5941},
    {"name": "nizamabad", "lat": 18.6725, "lng": 78.0941},
    {"name": "karimnagar", "lat": 18.4386, "lng": 79.1288},
    {"name": "khammam", "lat": 17.2473, "lng": 80.1514},
    {"name": "mahbubnagar", "lat": 16.7488, "lng": 78.0035},
]

MAJOR_CITIES = ANDHRA_PRADESH_CITIES + TELANGANA_CITIES

def haversine(lat1, lon1, lat2, lon2):
    """Calculate distance between two geo points (KM)."""
    R = 6371  # Earth radius in KM
    lat1, lon1 = float(lat1), float(lon1)
    lat2, lon2 = float(lat2), float(lon2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def get_nearest_city(lat, lng):
    """
    Returns nearest city slug based on latitude & longitude.
    Used only for redirect logic.
    """
    nearest_city = "guntur"  # safe fallback
    min_distance = float("inf")

    for city in MAJOR_CITIES:
        try:
            dist = haversine(lat, lng, city["lat"], city["lng"])
            if dist < min_distance:
                min_distance = dist
                nearest_city = city["name"]
        except (TypeError, ValueError):
            continue
    return nearest_city
