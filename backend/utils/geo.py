import math

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees).
    
    Returns distance in kilometers.
    """
    # Convert decimal degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of earth in kilometers
    r = 6371
    
    return c * r

def find_nearest_center(request_lat, request_lon, centers):
    """
    Find the nearest center to a given request location.
    
    Args:
        request_lat: Latitude of the request
        request_lon: Longitude of the request
        centers: List of center dictionaries with 'lat', 'lon', and 'center_id'
    
    Returns:
        Tuple of (nearest_center, distance)
    """
    if not centers:
        return None, float('inf')
    
    nearest_center = None
    min_distance = float('inf')
    
    for center in centers:
        distance = haversine(request_lat, request_lon, center['lat'], center['lon'])
        if distance < min_distance:
            min_distance = distance
            nearest_center = center
    
    return nearest_center, min_distance
