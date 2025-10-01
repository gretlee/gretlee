"""
Simulation Routes
Endpoints for running what-if scenario simulations
"""

from flask import Blueprint, request, jsonify
from backend.services.simulation_engine import simulation_engine

simulation_bp = Blueprint('simulation', __name__)


@simulation_bp.route('/simulation/scenario', methods=['POST'])
def run_scenario():
    """
    Run a what-if scenario simulation
    
    Request Body (JSON):
        {
            "city": "Lahore",
            "solar_percentage": 30,
            "green_spaces_increase": 20,
            "electric_transport_percentage": 40,
            "tree_planting": 100000,
            "policy_changes": ["solar_incentives", "ev_subsidies"]
        }
    
    Returns:
        JSON response with simulation results
    """
    if not request.is_json:
        return jsonify({
            'status': 'error',
            'message': 'Content-Type must be application/json'
        }), 400
    
    data = request.get_json()
    
    # Validate required fields
    if 'city' not in data:
        return jsonify({
            'status': 'error',
            'message': 'City parameter is required'
        }), 400
    
    city = data['city']
    
    # Extract scenario parameters
    scenario_params = {}
    
    if 'solar_percentage' in data:
        solar = float(data['solar_percentage'])
        if solar < 0 or solar > 100:
            return jsonify({
                'status': 'error',
                'message': 'solar_percentage must be between 0 and 100'
            }), 400
        scenario_params['solar_percentage'] = solar
    
    if 'green_spaces_increase' in data:
        green = float(data['green_spaces_increase'])
        if green < 0 or green > 100:
            return jsonify({
                'status': 'error',
                'message': 'green_spaces_increase must be between 0 and 100'
            }), 400
        scenario_params['green_spaces_increase'] = green
    
    if 'electric_transport_percentage' in data:
        electric = float(data['electric_transport_percentage'])
        if electric < 0 or electric > 100:
            return jsonify({
                'status': 'error',
                'message': 'electric_transport_percentage must be between 0 and 100'
            }), 400
        scenario_params['electric_transport_percentage'] = electric
    
    if 'tree_planting' in data:
        trees = int(data['tree_planting'])
        if trees < 0:
            return jsonify({
                'status': 'error',
                'message': 'tree_planting must be non-negative'
            }), 400
        scenario_params['tree_planting'] = trees
    
    if 'policy_changes' in data:
        scenario_params['policy_changes'] = data['policy_changes']
    
    # Run simulation
    result = simulation_engine.run_scenario(city, scenario_params)
    
    if result['status'] == 'error':
        return jsonify(result), 500
    
    return jsonify(result), 200


@simulation_bp.route('/simulation/compare', methods=['POST'])
def compare_scenarios():
    """
    Compare multiple scenarios side by side
    
    Request Body (JSON):
        {
            "city": "Lahore",
            "scenarios": [
                {"name": "Conservative", "solar_percentage": 20, ...},
                {"name": "Aggressive", "solar_percentage": 50, ...}
            ]
        }
    
    Returns:
        JSON response with comparison results
    """
    if not request.is_json:
        return jsonify({
            'status': 'error',
            'message': 'Content-Type must be application/json'
        }), 400
    
    data = request.get_json()
    
    if 'city' not in data or 'scenarios' not in data:
        return jsonify({
            'status': 'error',
            'message': 'City and scenarios parameters are required'
        }), 400
    
    city = data['city']
    scenarios = data['scenarios']
    
    if not isinstance(scenarios, list) or len(scenarios) < 2:
        return jsonify({
            'status': 'error',
            'message': 'At least 2 scenarios required for comparison'
        }), 400
    
    # Run simulation for each scenario
    results = []
    for scenario in scenarios:
        scenario_name = scenario.pop('name', f'Scenario {len(results) + 1}')
        result = simulation_engine.run_scenario(city, scenario)
        
        if result['status'] == 'success':
            result['data']['scenario_name'] = scenario_name
            results.append(result['data'])
    
    return jsonify({
        'status': 'success',
        'city': city,
        'comparisons': results
    }), 200


@simulation_bp.route('/simulation/templates', methods=['GET'])
def get_scenario_templates():
    """
    Get predefined scenario templates
    
    Returns:
        JSON response with scenario templates
    """
    templates = {
        'conservative': {
            'name': 'Conservative Growth',
            'description': 'Modest sustainability improvements',
            'solar_percentage': 20,
            'green_spaces_increase': 10,
            'electric_transport_percentage': 15,
            'tree_planting': 50000
        },
        'moderate': {
            'name': 'Moderate Progress',
            'description': 'Balanced sustainability strategy',
            'solar_percentage': 40,
            'green_spaces_increase': 25,
            'electric_transport_percentage': 35,
            'tree_planting': 150000
        },
        'aggressive': {
            'name': 'Aggressive Transformation',
            'description': 'Ambitious sustainability goals',
            'solar_percentage': 70,
            'green_spaces_increase': 50,
            'electric_transport_percentage': 60,
            'tree_planting': 300000
        },
        'carbon_neutral': {
            'name': 'Carbon Neutral 2040',
            'description': 'Path to carbon neutrality',
            'solar_percentage': 85,
            'green_spaces_increase': 60,
            'electric_transport_percentage': 80,
            'tree_planting': 500000
        }
    }
    
    return jsonify({
        'status': 'success',
        'templates': templates
    }), 200
