# geo_validator.py
import math

def haversine(lat1, lon1, lat2, lon2):
    # returns distance in meters
    R = 6371000  # earth radius meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2.0)**2 + math.cos(phi1)*math.cos(phi2)*(math.sin(dlambda/2.0)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def distance_meters(p1, p2):
    if p1 is None or p2 is None:
        return None
    return haversine(p1[0], p1[1], p2[0], p2[1])
