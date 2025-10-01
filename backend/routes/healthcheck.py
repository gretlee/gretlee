"""
Health Check Routes
Simple endpoint to check if API is running
"""

from flask import Blueprint, jsonify
from datetime import datetime

healthcheck_bp = Blueprint('healthcheck', __name__)


@healthcheck_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    
    Returns:
        JSON response with API status
    """
    return jsonify({
        'status': 'healthy',
        'message': 'Urban Sustainability Simulator API is running',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    }), 200


@healthcheck_bp.route('/status', methods=['GET'])
def status():
    """
    Detailed status endpoint
    
    Returns:
        JSON response with detailed API status
    """
    return jsonify({
        'status': 'operational',
        'services': {
            'aqi_forecast': 'available',
            'energy_demand': 'available',
            'flood_risk': 'available',
            'simulation_engine': 'available'
        },
        'supported_cities': ['Lahore', 'Karachi', 'Faisalabad', 'Sargodha'],
        'timestamp': datetime.now().isoformat()
    }), 200
