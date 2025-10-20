import math

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.asin(math.sqrt(a))

def simple_pool(shipments, radius_km=10):
    shipments = list(shipments)
    pools = []
    used = set()
    for i, s in enumerate(shipments):
        if s.id in used:
            continue
        group = [s]
        used.add(s.id)
        for t in shipments[i+1:]:
            if t.id in used:
                continue
            d = haversine_km(s.pickup_lat, s.pickup_lon, t.pickup_lat, t.pickup_lon)
            if d <= radius_km:
                group.append(t)
                used.add(t.id)
        pools.append(group)
    return pools
