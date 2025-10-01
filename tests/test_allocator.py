"""
Test suite for resource allocation algorithm.

Tests cover various scenarios:
- Single request with sufficient stock
- Request larger than available stock
- Multiple requests with urgency prioritization
- Distance-based allocation
- Stock depletion
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../backend'))

import pytest
from services.allocator import allocate_resources, calculate_allocation_metrics
from utils.geo import haversine


class TestAllocator:
    """Test cases for resource allocation algorithm"""
    
    def test_single_request_sufficient_stock(self):
        """Test: Single request with single center having enough stock"""
        centers = [
            {
                'center_id': 'CTR001',
                'lat': 33.6844,
                'lon': 73.0479,
                'water_stock': 1000,
                'food_stock': 800,
                'tent_stock': 200
            }
        ]
        
        requests = [
            {
                'request_id': 'REQ001',
                'lat': 33.7077,
                'lon': 73.0478,
                'people': 50,
                'need_type': 'water',
                'urgency': 'high'
            }
        ]
        
        allocations, updated_centers = allocate_resources(centers, requests)
        
        # Assertions
        assert len(allocations) == 1
        assert allocations[0]['request_id'] == 'REQ001'
        assert allocations[0]['center_id'] == 'CTR001'
        assert allocations[0]['resources_sent'] == 50
        assert allocations[0]['distance'] > 0
        
        # Check stock deduction
        assert updated_centers[0]['water_stock'] == 950
        assert updated_centers[0]['food_stock'] == 800  # unchanged
        assert updated_centers[0]['tent_stock'] == 200  # unchanged
    
    def test_request_larger_than_stock(self):
        """Test: Request with demand exceeding available stock"""
        centers = [
            {
                'center_id': 'CTR001',
                'lat': 33.6844,
                'lon': 73.0479,
                'water_stock': 30,
                'food_stock': 800,
                'tent_stock': 200
            }
        ]
        
        requests = [
            {
                'request_id': 'REQ001',
                'lat': 33.7077,
                'lon': 73.0478,
                'people': 100,
                'need_type': 'water',
                'urgency': 'high'
            }
        ]
        
        allocations, updated_centers = allocate_resources(centers, requests)
        
        # Should allocate partial resources
        assert len(allocations) == 1
        assert allocations[0]['resources_sent'] == 30  # Only what's available
        assert updated_centers[0]['water_stock'] == 0
    
    def test_multiple_requests_urgency_respected(self):
        """Test: Multiple requests are processed by urgency priority"""
        centers = [
            {
                'center_id': 'CTR001',
                'lat': 33.6844,
                'lon': 73.0479,
                'water_stock': 1000,
                'food_stock': 1000,
                'tent_stock': 1000
            }
        ]
        
        requests = [
            {
                'request_id': 'REQ001',
                'lat': 33.7077,
                'lon': 73.0478,
                'people': 50,
                'need_type': 'water',
                'urgency': 'low'
            },
            {
                'request_id': 'REQ002',
                'lat': 33.6500,
                'lon': 73.1600,
                'people': 75,
                'need_type': 'food',
                'urgency': 'high'
            },
            {
                'request_id': 'REQ003',
                'lat': 33.6900,
                'lon': 73.0600,
                'people': 60,
                'need_type': 'tent',
                'urgency': 'medium'
            }
        ]
        
        allocations, updated_centers = allocate_resources(centers, requests)
        
        # All requests should be allocated
        assert len(allocations) == 3
        
        # Check that high urgency was processed (should be first in allocations)
        assert allocations[0]['request_id'] == 'REQ002'
        assert allocations[0]['resources_sent'] == 75
        
        # Medium urgency second
        assert allocations[1]['request_id'] == 'REQ003'
        assert allocations[1]['resources_sent'] == 60
        
        # Low urgency last
        assert allocations[2]['request_id'] == 'REQ001'
        assert allocations[2]['resources_sent'] == 50
    
    def test_no_stock_available(self):
        """Test: Request when no stock is available"""
        centers = [
            {
                'center_id': 'CTR001',
                'lat': 33.6844,
                'lon': 73.0479,
                'water_stock': 0,
                'food_stock': 0,
                'tent_stock': 0
            }
        ]
        
        requests = [
            {
                'request_id': 'REQ001',
                'lat': 33.7077,
                'lon': 73.0478,
                'people': 50,
                'need_type': 'water',
                'urgency': 'high'
            }
        ]
        
        allocations, updated_centers = allocate_resources(centers, requests)
        
        # No allocation should be made
        assert len(allocations) == 0
    
    def test_nearest_center_selection(self):
        """Test: Multiple centers - should select nearest one"""
        centers = [
            {
                'center_id': 'CTR001',
                'lat': 33.6844,
                'lon': 73.0479,
                'water_stock': 1000,
                'food_stock': 800,
                'tent_stock': 200
            },
            {
                'center_id': 'CTR002',
                'lat': 31.5204,
                'lon': 74.3587,
                'water_stock': 1500,
                'food_stock': 1200,
                'tent_stock': 300
            },
            {
                'center_id': 'CTR003',
                'lat': 24.8607,
                'lon': 67.0011,
                'water_stock': 2000,
                'food_stock': 1500,
                'tent_stock': 400
            }
        ]
        
        # Request near CTR001
        requests = [
            {
                'request_id': 'REQ001',
                'lat': 33.7077,
                'lon': 73.0478,
                'people': 50,
                'need_type': 'water',
                'urgency': 'high'
            }
        ]
        
        allocations, updated_centers = allocate_resources(centers, requests)
        
        # Should allocate from CTR001 (nearest)
        assert len(allocations) == 1
        assert allocations[0]['center_id'] == 'CTR001'
        
        # Verify distance is reasonable (should be small)
        assert allocations[0]['distance'] < 10  # Less than 10km
    
    def test_different_need_types(self):
        """Test: Allocation handles different resource types correctly"""
        centers = [
            {
                'center_id': 'CTR001',
                'lat': 33.6844,
                'lon': 73.0479,
                'water_stock': 100,
                'food_stock': 200,
                'tent_stock': 50
            }
        ]
        
        requests = [
            {
                'request_id': 'REQ001',
                'lat': 33.7077,
                'lon': 73.0478,
                'people': 30,
                'need_type': 'water',
                'urgency': 'high'
            },
            {
                'request_id': 'REQ002',
                'lat': 33.6500,
                'lon': 73.1600,
                'people': 40,
                'need_type': 'food',
                'urgency': 'high'
            },
            {
                'request_id': 'REQ003',
                'lat': 33.6900,
                'lon': 73.0600,
                'people': 20,
                'need_type': 'tent',
                'urgency': 'high'
            }
        ]
        
        allocations, updated_centers = allocate_resources(centers, requests)
        
        # All should be allocated
        assert len(allocations) == 3
        
        # Check correct stock deductions
        assert updated_centers[0]['water_stock'] == 70
        assert updated_centers[0]['food_stock'] == 160
        assert updated_centers[0]['tent_stock'] == 30


class TestAllocationMetrics:
    """Test cases for allocation metrics calculation"""
    
    def test_full_allocation_metrics(self):
        """Test: Metrics when all requests are allocated"""
        requests = [
            {'request_id': 'REQ001'},
            {'request_id': 'REQ002'},
            {'request_id': 'REQ003'}
        ]
        
        allocations = [
            {'request_id': 'REQ001', 'distance': 10.5},
            {'request_id': 'REQ002', 'distance': 15.2},
            {'request_id': 'REQ003', 'distance': 8.3}
        ]
        
        metrics = calculate_allocation_metrics(allocations, requests)
        
        assert metrics['total_requests'] == 3
        assert metrics['allocated_requests'] == 3
        assert metrics['allocation_rate'] == 100.0
        assert metrics['avg_distance'] == pytest.approx(11.33, rel=0.01)
    
    def test_partial_allocation_metrics(self):
        """Test: Metrics when some requests are unallocated"""
        requests = [
            {'request_id': 'REQ001'},
            {'request_id': 'REQ002'},
            {'request_id': 'REQ003'},
            {'request_id': 'REQ004'}
        ]
        
        allocations = [
            {'request_id': 'REQ001', 'distance': 10.0},
            {'request_id': 'REQ002', 'distance': 20.0}
        ]
        
        metrics = calculate_allocation_metrics(allocations, requests)
        
        assert metrics['total_requests'] == 4
        assert metrics['allocated_requests'] == 2
        assert metrics['allocation_rate'] == 50.0
        assert metrics['avg_distance'] == 15.0
    
    def test_no_allocations_metrics(self):
        """Test: Metrics when no requests are allocated"""
        requests = [
            {'request_id': 'REQ001'},
            {'request_id': 'REQ002'}
        ]
        
        allocations = []
        
        metrics = calculate_allocation_metrics(allocations, requests)
        
        assert metrics['total_requests'] == 2
        assert metrics['allocated_requests'] == 0
        assert metrics['allocation_rate'] == 0.0
        assert metrics['avg_distance'] == 0.0


class TestHaversineDistance:
    """Test cases for Haversine distance calculation"""
    
    def test_same_location(self):
        """Test: Distance between same point should be 0"""
        distance = haversine(33.6844, 73.0479, 33.6844, 73.0479)
        assert distance == pytest.approx(0.0, abs=0.01)
    
    def test_known_distance(self):
        """Test: Distance between Islamabad and Lahore (approximately 280km)"""
        islamabad_lat, islamabad_lon = 33.6844, 73.0479
        lahore_lat, lahore_lon = 31.5204, 74.3587
        
        distance = haversine(islamabad_lat, islamabad_lon, lahore_lat, lahore_lon)
        
        # Actual distance is approximately 280km
        assert 270 < distance < 290
    
    def test_symmetry(self):
        """Test: Distance A->B should equal distance B->A"""
        lat1, lon1 = 33.6844, 73.0479
        lat2, lon2 = 31.5204, 74.3587
        
        distance_ab = haversine(lat1, lon1, lat2, lon2)
        distance_ba = haversine(lat2, lon2, lat1, lon1)
        
        assert distance_ab == pytest.approx(distance_ba, rel=0.001)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
