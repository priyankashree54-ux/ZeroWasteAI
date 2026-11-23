"""Decides which NGO gets the leftover food. Closest NGO first, until its limit is full."""
import math

NGOS = [
    {"name": "Annapurna Community Kitchen", "lat": 28.6139, "lon": 77.2090, "capacity_kg": 60, "serves": "Shelter for homeless"},
    {"name": "Hope Children's Home",        "lat": 28.5355, "lon": 77.3910, "capacity_kg": 35, "serves": "Orphanage"},
    {"name": "Seva Old-Age Care",           "lat": 28.7041, "lon": 77.1025, "capacity_kg": 25, "serves": "Elderly care"},
    {"name": "Roti Bank Foundation",        "lat": 28.4595, "lon": 77.0266, "capacity_kg": 80, "serves": "Street hunger relief"},
    {"name": "Asha Night Shelter",          "lat": 28.6692, "lon": 77.4538, "capacity_kg": 40, "serves": "Night shelter"},
]

def haversine(a_lat, a_lon, b_lat, b_lon):
    R = 6371
    p1, p2 = math.radians(a_lat), math.radians(b_lat)
    dphi, dl = p2 - p1, math.radians(b_lon - a_lon)
    h = math.sin(dphi/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2 * R * math.asin(math.sqrt(h))

def allocate(surplus_kg, lat, lon, ngos=NGOS):
    """Give food to the nearest NGO, then the next nearest, until nothing is left."""
    ranked = sorted(ngos, key=lambda n: haversine(lat, lon, n["lat"], n["lon"]))
    left, plan = surplus_kg, []
    for n in ranked:
        if left <= 0:
            break
        give = min(left, n["capacity_kg"])
        plan.append({"ngo": n["name"], "serves": n["serves"], "kg": round(give, 1),
                     "distance_km": round(haversine(lat, lon, n["lat"], n["lon"]), 1),
                     "meals": int(give * 3)})   # rough guess: 1 kg = 3 meals
        left -= give
    return plan, round(max(left, 0), 1)
