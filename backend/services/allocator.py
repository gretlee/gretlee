from utils.geo import haversine, find_nearest_center

def allocate_resources(centers, requests):
    """
    Allocate resources from centers to disaster requests.
    
    Algorithm:
    1. Sort requests by urgency (high > medium > low)
    2. For each request, assign nearest center with available stock
    3. Deduct stock after allocation
    
    Args:
        centers: List of center dictionaries with stock information
        requests: List of request dictionaries with needs
    
    Returns:
        Tuple of (allocations, updated_centers)
        allocations: List of allocation dictionaries
        updated_centers: List of updated center dictionaries with new stock levels
    """
    # Urgency priority mapping
    urgency_priority = {
        'high': 3,
        'medium': 2,
        'low': 1
    }
    
    # Sort requests by urgency (high to low)
    sorted_requests = sorted(
        requests, 
        key=lambda x: urgency_priority.get(x['urgency'], 0), 
        reverse=True
    )
    
    # Create working copies of centers
    working_centers = [center.copy() for center in centers]
    
    allocations = []
    
    for req in sorted_requests:
        request_lat = req['lat']
        request_lon = req['lon']
        need_type = req['need_type']
        people = req['people']
        
        # Determine stock field based on need type
        stock_field_map = {
            'water': 'water_stock',
            'food': 'food_stock',
            'tent': 'tent_stock',
            'tents': 'tent_stock',
            'medical': 'water_stock',  # Use water stock as proxy for medical
            'shelter': 'tent_stock'
        }
        
        stock_field = stock_field_map.get(need_type.lower(), 'water_stock')
        
        # Find suitable centers (with available stock)
        suitable_centers = [
            c for c in working_centers 
            if c.get(stock_field, 0) > 0
        ]
        
        if not suitable_centers:
            # No center has available stock
            continue
        
        # Find nearest center with stock
        nearest_center, distance = find_nearest_center(
            request_lat, 
            request_lon, 
            suitable_centers
        )
        
        if nearest_center:
            # Calculate resources to send (min of need and available stock)
            available_stock = nearest_center[stock_field]
            resources_to_send = min(people, available_stock)
            
            # Create allocation
            allocation = {
                'request_id': req['request_id'],
                'center_id': nearest_center['center_id'],
                'resources_sent': resources_to_send,
                'distance': round(distance, 2),
                'need_type': need_type
            }
            
            allocations.append(allocation)
            
            # Update center stock in working copy
            for center in working_centers:
                if center['center_id'] == nearest_center['center_id']:
                    center[stock_field] -= resources_to_send
                    break
    
    return allocations, working_centers

def calculate_allocation_metrics(allocations, requests):
    """
    Calculate performance metrics for allocations.
    
    Returns:
        Dictionary with metrics like % requests served, avg distance
    """
    if not requests:
        return {
            'total_requests': 0,
            'allocated_requests': 0,
            'allocation_rate': 0,
            'avg_distance': 0
        }
    
    total_requests = len(requests)
    allocated_requests = len(allocations)
    allocation_rate = (allocated_requests / total_requests) * 100 if total_requests > 0 else 0
    
    avg_distance = 0
    if allocations:
        total_distance = sum(a['distance'] for a in allocations)
        avg_distance = total_distance / len(allocations)
    
    return {
        'total_requests': total_requests,
        'allocated_requests': allocated_requests,
        'allocation_rate': round(allocation_rate, 2),
        'avg_distance': round(avg_distance, 2)
    }
