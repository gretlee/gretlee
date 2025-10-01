"""
Model Inference Service
Handles loading ML models and running predictions
"""

import sys
import os

# Add parent directory to path for importing ml_models
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from ml_models.air_quality_forecast import get_aqi_forecast
from ml_models.energy_demand_model import predict_city_energy_demand
from ml_models.flood_risk_model import assess_city_flood_risk
from backend.services.data_loader import data_loader


class ModelInferenceService:
    """
    Service for running ML model predictions
    """
    
    def __init__(self):
        """
        Initialize inference service
        """
        self.models_loaded = False
    
    def predict_aqi(self, city, days=7):
        """
        Predict AQI for a city
        
        Args:
            city: City name
            days: Number of days to forecast
        
        Returns:
            Dictionary with AQI predictions
        """
        try:
            # Get recent data for the city
            recent_data = data_loader.get_recent_aqi(city, days=7)
            
            # Get forecast
            forecast = get_aqi_forecast(city=city, days=days)
            
            return {
                'status': 'success',
                'city': city,
                'forecast_days': days,
                'data': forecast
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                'city': city
            }
    
    def predict_energy_demand(self, city, scenario=None):
        """
        Predict energy demand for a city
        
        Args:
            city: City name
            scenario: Optional scenario adjustments
        
        Returns:
            Dictionary with energy predictions
        """
        try:
            prediction = predict_city_energy_demand(city=city, scenario=scenario)
            
            return {
                'status': 'success',
                'city': city,
                'data': prediction
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                'city': city
            }
    
    def assess_flood_risk(self, city, num_zones=20):
        """
        Assess flood risk for a city
        
        Args:
            city: City name
            num_zones: Number of zones to analyze
        
        Returns:
            Dictionary with flood risk assessment
        """
        try:
            assessment = assess_city_flood_risk(city=city, num_zones=num_zones)
            
            return {
                'status': 'success',
                'city': city,
                'data': assessment
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                'city': city
            }
    
    def get_city_overview(self, city):
        """
        Get comprehensive overview for a city
        
        Args:
            city: City name
        
        Returns:
            Dictionary with all metrics
        """
        try:
            # Get city metadata
            metadata = data_loader.get_city_metadata(city)
            
            # Get AQI forecast
            aqi_forecast = self.predict_aqi(city, days=7)
            
            # Get energy demand
            energy_prediction = self.predict_energy_demand(city)
            
            # Get flood risk
            flood_assessment = self.assess_flood_risk(city, num_zones=10)
            
            return {
                'status': 'success',
                'city': city,
                'metadata': metadata,
                'aqi': aqi_forecast.get('data'),
                'energy': energy_prediction.get('data'),
                'flood_risk': flood_assessment.get('data')
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                'city': city
            }


# Singleton instance
model_inference_service = ModelInferenceService()
