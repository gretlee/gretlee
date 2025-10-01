"""
Forecast Routes
Endpoints for AQI, energy, and flood risk predictions
"""

from flask import Blueprint, request, jsonify
from backend.services.model_inference import model_inference_service

forecast_bp = Blueprint('forecast', __name__)


@forecast_bp.route('/forecast/aqi', methods=['GET'])
def get_aqi_forecast():
    """
    Get AQI forecast for a city
    
    Query Parameters:
        city (str): City name (required)
        days (int): Number of days to forecast (default: 7)
    
    Returns:
        JSON response with AQI predictions
    """
    city = request.args.get('city', 'Lahore')
    days = int(request.args.get('days', 7))
    
    if days < 1 or days > 30:
        return jsonify({
            'status': 'error',
            'message': 'Days parameter must be between 1 and 30'
        }), 400
    
    result = model_inference_service.predict_aqi(city, days)
    
    if result['status'] == 'error':
        return jsonify(result), 500
    
    return jsonify(result), 200


@forecast_bp.route('/forecast/energy', methods=['GET'])
def get_energy_forecast():
    """
    Get energy demand forecast for a city
    
    Query Parameters:
        city (str): City name (required)
    
    Returns:
        JSON response with energy demand predictions
    """
    city = request.args.get('city', 'Lahore')
    
    result = model_inference_service.predict_energy_demand(city)
    
    if result['status'] == 'error':
        return jsonify(result), 500
    
    return jsonify(result), 200


@forecast_bp.route('/forecast/flood-risk', methods=['GET'])
def get_flood_risk():
    """
    Get flood risk assessment for a city
    
    Query Parameters:
        city (str): City name (required)
        zones (int): Number of zones to analyze (default: 20)
    
    Returns:
        JSON response with flood risk assessment
    """
    city = request.args.get('city', 'Lahore')
    zones = int(request.args.get('zones', 20))
    
    if zones < 1 or zones > 100:
        return jsonify({
            'status': 'error',
            'message': 'Zones parameter must be between 1 and 100'
        }), 400
    
    result = model_inference_service.assess_flood_risk(city, zones)
    
    if result['status'] == 'error':
        return jsonify(result), 500
    
    return jsonify(result), 200


@forecast_bp.route('/forecast/overview', methods=['GET'])
def get_city_overview():
    """
    Get comprehensive overview for a city
    
    Query Parameters:
        city (str): City name (required)
    
    Returns:
        JSON response with all forecasts and metrics
    """
    city = request.args.get('city', 'Lahore')
    
    result = model_inference_service.get_city_overview(city)
    
    if result['status'] == 'error':
        return jsonify(result), 500
    
    return jsonify(result), 200
