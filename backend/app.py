"""
Flask Backend Application
Main entry point for the Urban Sustainability Simulator API
"""

import sys
import os
from flask import Flask, jsonify
from flask_cors import CORS

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.routes.healthcheck import healthcheck_bp
from backend.routes.forecast_routes import forecast_bp
from backend.routes.simulation_routes import simulation_bp


def create_app():
    """
    Create and configure Flask application
    
    Returns:
        Flask app instance
    """
    app = Flask(__name__)
    
    # Configuration
    app.config['JSON_SORT_KEYS'] = False
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    
    # Enable CORS for frontend communication
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000", "http://localhost:5000"],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })
    
    # Register blueprints
    app.register_blueprint(healthcheck_bp, url_prefix='/api')
    app.register_blueprint(forecast_bp, url_prefix='/api')
    app.register_blueprint(simulation_bp, url_prefix='/api')
    
    # Root endpoint
    @app.route('/')
    def index():
        """Root endpoint with API information"""
        return jsonify({
            'name': 'Urban Sustainability Simulator API',
            'version': '1.0.0',
            'description': 'AI-driven platform for urban sustainability forecasting in Pakistani cities',
            'endpoints': {
                'health': '/api/health',
                'status': '/api/status',
                'aqi_forecast': '/api/forecast/aqi?city=Lahore&days=7',
                'energy_forecast': '/api/forecast/energy?city=Lahore',
                'flood_risk': '/api/forecast/flood-risk?city=Lahore&zones=20',
                'city_overview': '/api/forecast/overview?city=Lahore',
                'run_scenario': '/api/simulation/scenario (POST)',
                'compare_scenarios': '/api/simulation/compare (POST)',
                'scenario_templates': '/api/simulation/templates'
            },
            'supported_cities': ['Lahore', 'Karachi', 'Faisalabad', 'Sargodha'],
            'documentation': 'See README.md for detailed API documentation'
        }), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return jsonify({
            'status': 'error',
            'message': 'Endpoint not found',
            'code': 404
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        return jsonify({
            'status': 'error',
            'message': 'Internal server error',
            'code': 500
        }), 500
    
    return app


if __name__ == '__main__':
    app = create_app()
    
    print("=" * 60)
    print("🌍 Urban Sustainability Simulator API")
    print("=" * 60)
    print("Starting Flask development server...")
    print("API available at: http://localhost:5000")
    print("Health check: http://localhost:5000/api/health")
    print("=" * 60)
    
    # Run development server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
