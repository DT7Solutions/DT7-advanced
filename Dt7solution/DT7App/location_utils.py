import math

# ----------------------------- Andhra Pradesh Major Cities ----------------------------- #
ANDHRA_PRADESH_CITIES = [
    {"name": "visakhapatnam", "lat": 17.6868, "lng": 83.2185},   # Visakhapatnam district
    {"name": "vizianagaram", "lat": 18.1149, "lng": 83.4160},   # Vizianagaram
    {"name": "srikakulam", "lat": 18.2966, "lng": 83.8956},     # Srikakulam
    {"name": "vijayawada", "lat": 16.5062, "lng": 80.6480},     # Krishna
    {"name": "guntur", "lat": 16.3067, "lng": 80.4365},        # Guntur
    {"name": "amaravathi", "lat": 16.5723, "lng": 80.3568},     # Guntur/Amaravathi region
    {"name": "nellore", "lat": 14.4426, "lng": 79.9865},       # Nellore
    {"name": "tirupati", "lat": 13.6288, "lng": 79.4192},      # Chittoor/Tirupati
    {"name": "kurnool", "lat": 15.8281, "lng": 78.0373},       # Kurnool
    {"name": "anantapur", "lat": 14.6814, "lng": 77.6000},     # Anantapur
    {"name": "rajahmundry", "lat": 17.0005, "lng": 81.8040},   # East Godavari
    {"name": "kakinada", "lat": 16.9891, "lng": 82.2475},      # East Godavari
    {"name": "eluru", "lat": 16.7107, "lng": 81.0952},         # West Godavari
    {"name": "ongole", "lat": 15.5057, "lng": 80.0499},        # Prakasam
    {"name": "kadapa", "lat": 14.4670, "lng": 78.8242},        # Kadapa
    {"name": "chittoor", "lat": 13.2170, "lng": 79.1000},      # Chittoor district
]

# ----------------------------- Telangana Major Cities ----------------------------- #
TELANGANA_CITIES = [
    {"name": "hyderabad", "lat": 17.3850, "lng": 78.4867},     # Hyderabad district
    {"name": "secunderabad", "lat": 17.4399, "lng": 78.4983},  # Hyderabad region
    {"name": "warangal", "lat": 17.9689, "lng": 79.5941},      # Warangal
    {"name": "nizamabad", "lat": 18.6725, "lng": 78.0941},     # Nizamabad
    {"name": "karimnagar", "lat": 18.4386, "lng": 79.1288},   # Karimnagar
    {"name": "khammam", "lat": 17.2473, "lng": 80.1514},      # Khammam
    {"name": "mahbubnagar", "lat": 16.7488, "lng": 78.0035},  # Mahbubnagar
    {"name": "ramagundam", "lat": 18.8165, "lng": 79.3646},    # Peddapalli
    {"name": "medak", "lat": 17.7970, "lng": 78.2700},        # Medak
    {"name": "nalgonda", "lat": 17.0588, "lng": 79.2670},     # Nalgonda
    {"name": "adilabad", "lat": 19.6665, "lng": 78.5349},     # Adilabad
]

MAJOR_CITIES = ANDHRA_PRADESH_CITIES + TELANGANA_CITIES

# ----------------------------- Haversine Function ----------------------------- #
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

# ----------------------------- Get Nearest City within Radius ----------------------------- #
def get_nearest_city(lat, lng, radius_km=50):
    """
    Returns nearest city slug based on latitude & longitude.
    Only returns a city if within `radius_km`. Otherwise, returns default 'guntur'.
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

    # Check if nearest city is within the radius
    if min_distance <= radius_km:
        return nearest_city
    else:
        return "guntur"
