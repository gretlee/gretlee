"""
API Tests
Unit tests for backend API endpoints
"""

import pytest
import sys
import os

# Add parent directories to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.app import create_app


@pytest.fixture
def client():
    """Create test client"""
    app = create_app()
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        yield client


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/api/health')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'timestamp' in data


def test_status(client):
    """Test status endpoint"""
    response = client.get('/api/status')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['status'] == 'operational'
    assert 'services' in data
    assert 'supported_cities' in data


def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    
    data = response.get_json()
    assert 'name' in data
    assert 'endpoints' in data


def test_aqi_forecast(client):
    """Test AQI forecast endpoint"""
    response = client.get('/api/forecast/aqi?city=Lahore&days=7')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['city'] == 'Lahore'
    assert 'data' in data


def test_aqi_forecast_invalid_days(client):
    """Test AQI forecast with invalid days parameter"""
    response = client.get('/api/forecast/aqi?city=Lahore&days=50')
    assert response.status_code == 400
    
    data = response.get_json()
    assert data['status'] == 'error'


def test_energy_forecast(client):
    """Test energy demand forecast endpoint"""
    response = client.get('/api/forecast/energy?city=Karachi')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['city'] == 'Karachi'


def test_flood_risk(client):
    """Test flood risk assessment endpoint"""
    response = client.get('/api/forecast/flood-risk?city=Faisalabad&zones=10')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['city'] == 'Faisalabad'


def test_city_overview(client):
    """Test city overview endpoint"""
    response = client.get('/api/forecast/overview?city=Sargodha')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['city'] == 'Sargodha'
    assert 'metadata' in data


def test_scenario_simulation(client):
    """Test scenario simulation endpoint"""
    scenario_data = {
        'city': 'Lahore',
        'solar_percentage': 30,
        'green_spaces_increase': 20,
        'electric_transport_percentage': 40,
        'tree_planting': 100000
    }
    
    response = client.post(
        '/api/simulation/scenario',
        json=scenario_data,
        content_type='application/json'
    )
    
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['status'] == 'success'
    assert 'data' in data
    assert 'impacts' in data['data']


def test_scenario_simulation_invalid_solar(client):
    """Test scenario simulation with invalid solar percentage"""
    scenario_data = {
        'city': 'Lahore',
        'solar_percentage': 150  # Invalid: > 100
    }
    
    response = client.post(
        '/api/simulation/scenario',
        json=scenario_data,
        content_type='application/json'
    )
    
    assert response.status_code == 400


def test_scenario_simulation_missing_city(client):
    """Test scenario simulation without city"""
    scenario_data = {
        'solar_percentage': 30
    }
    
    response = client.post(
        '/api/simulation/scenario',
        json=scenario_data,
        content_type='application/json'
    )
    
    assert response.status_code == 400


def test_scenario_templates(client):
    """Test scenario templates endpoint"""
    response = client.get('/api/simulation/templates')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['status'] == 'success'
    assert 'templates' in data
    assert 'conservative' in data['templates']
    assert 'aggressive' in data['templates']


def test_compare_scenarios(client):
    """Test scenario comparison endpoint"""
    comparison_data = {
        'city': 'Lahore',
        'scenarios': [
            {
                'name': 'Scenario 1',
                'solar_percentage': 20,
                'green_spaces_increase': 10
            },
            {
                'name': 'Scenario 2',
                'solar_percentage': 50,
                'green_spaces_increase': 30
            }
        ]
    }
    
    response = client.post(
        '/api/simulation/compare',
        json=comparison_data,
        content_type='application/json'
    )
    
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['status'] == 'success'
    assert 'comparisons' in data
    assert len(data['comparisons']) == 2


def test_404_error(client):
    """Test 404 error handling"""
    response = client.get('/api/nonexistent')
    assert response.status_code == 404
    
    data = response.get_json()
    assert data['status'] == 'error'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
