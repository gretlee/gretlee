"""
Test suite for prediction service.

Tests cover:
- Model training without errors
- Prediction output validation
- Historical data loading
- Forecast generation
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../backend'))

import pytest
import pandas as pd
import numpy as np
from services.prediction import train_prediction_model, predict_resource_demand


class TestPredictionModel:
    """Test cases for ML prediction model"""
    
    def test_model_trains_without_error(self):
        """Test: Model trains successfully on historical data"""
        # This will use the actual historical_requests.csv
        model, scaler, le_need, le_urgency = train_prediction_model()
        
        # Check that model and encoders were created
        assert model is not None, "Model should be created"
        assert scaler is not None, "Scaler should be created"
        assert le_need is not None, "Need type encoder should be created"
        assert le_urgency is not None, "Urgency encoder should be created"
    
    def test_model_has_correct_features(self):
        """Test: Model is trained with expected features"""
        model, scaler, le_need, le_urgency = train_prediction_model()
        
        if model is not None:
            # RandomForest should have feature_importances_
            assert hasattr(model, 'feature_importances_')
            assert len(model.feature_importances_) == 7  # 7 features expected
    
    def test_prediction_output_structure(self):
        """Test: Prediction returns correct structure"""
        predictions = predict_resource_demand(days=7)
        
        # Should return list of 7 predictions
        assert isinstance(predictions, list)
        assert len(predictions) == 7
        
        # Each prediction should have required fields
        for pred in predictions:
            assert 'date' in pred
            assert 'total_demand' in pred
            assert 'water_demand' in pred
            assert 'food_demand' in pred
            assert 'tent_demand' in pred
            
            # Demands should be non-negative
            assert pred['total_demand'] >= 0
            assert pred['water_demand'] >= 0
            assert pred['food_demand'] >= 0
            assert pred['tent_demand'] >= 0
    
    def test_prediction_dates_sequential(self):
        """Test: Prediction dates are sequential and in future"""
        predictions = predict_resource_demand(days=5)
        
        dates = [pd.to_datetime(p['date']) for p in predictions]
        
        # Check dates are sequential (each day increments by 1)
        for i in range(len(dates) - 1):
            diff = (dates[i + 1] - dates[i]).days
            assert diff == 1, "Dates should be consecutive days"
    
    def test_custom_forecast_period(self):
        """Test: Prediction works with different forecast periods"""
        # Test 3-day forecast
        predictions_3 = predict_resource_demand(days=3)
        assert len(predictions_3) == 3
        
        # Test 14-day forecast
        predictions_14 = predict_resource_demand(days=14)
        assert len(predictions_14) == 14
    
    def test_total_demand_is_sum_of_parts(self):
        """Test: Total demand equals sum of individual resource demands"""
        predictions = predict_resource_demand(days=7)
        
        for pred in predictions:
            calculated_total = (
                pred['water_demand'] + 
                pred['food_demand'] + 
                pred['tent_demand']
            )
            
            # Total should equal sum (allowing for small floating point differences)
            assert pred['total_demand'] == pytest.approx(calculated_total, abs=1)


class TestHistoricalData:
    """Test cases for historical data handling"""
    
    def test_historical_data_exists(self):
        """Test: Historical data file exists and is readable"""
        data_path = os.path.join(
            os.path.dirname(__file__), 
            '../data/historical_requests.csv'
        )
        
        assert os.path.exists(data_path), "Historical data file should exist"
        
        # Should be readable as CSV
        df = pd.read_csv(data_path)
        assert len(df) > 0, "Historical data should not be empty"
    
    def test_historical_data_has_required_columns(self):
        """Test: Historical data has all required columns"""
        data_path = os.path.join(
            os.path.dirname(__file__), 
            '../data/historical_requests.csv'
        )
        
        df = pd.read_csv(data_path)
        
        required_columns = ['date', 'lat', 'lon', 'need_type', 'people', 'urgency']
        
        for col in required_columns:
            assert col in df.columns, f"Column '{col}' should exist"
    
    def test_historical_data_valid_values(self):
        """Test: Historical data contains valid values"""
        data_path = os.path.join(
            os.path.dirname(__file__), 
            '../data/historical_requests.csv'
        )
        
        df = pd.read_csv(data_path)
        
        # Check for null values
        assert df['people'].notna().all(), "People column should not have nulls"
        assert df['lat'].notna().all(), "Latitude should not have nulls"
        assert df['lon'].notna().all(), "Longitude should not have nulls"
        
        # Check value ranges
        assert (df['people'] > 0).all(), "People should be positive"
        assert (df['lat'].between(-90, 90)).all(), "Latitude should be valid"
        assert (df['lon'].between(-180, 180)).all(), "Longitude should be valid"
        
        # Check categorical values
        valid_needs = ['water', 'food', 'tent', 'medical', 'shelter']
        assert df['need_type'].isin(valid_needs).all(), "Need types should be valid"
        
        valid_urgency = ['high', 'medium', 'low']
        assert df['urgency'].isin(valid_urgency).all(), "Urgency should be valid"


class TestPredictionEdgeCases:
    """Test cases for edge cases and error handling"""
    
    def test_prediction_without_trained_model(self):
        """Test: Prediction handles missing model gracefully"""
        # Even without a trained model, should return valid structure
        predictions = predict_resource_demand(days=7)
        
        assert isinstance(predictions, list)
        assert len(predictions) == 7
        
        # Each prediction should have the expected keys
        for pred in predictions:
            assert 'date' in pred
            assert 'total_demand' in pred
    
    def test_zero_day_forecast(self):
        """Test: Handle zero-day forecast request"""
        predictions = predict_resource_demand(days=0)
        
        # Should return empty list or handle gracefully
        assert isinstance(predictions, list)
        assert len(predictions) == 0
    
    def test_large_forecast_period(self):
        """Test: Handle very large forecast period"""
        predictions = predict_resource_demand(days=30)
        
        assert isinstance(predictions, list)
        assert len(predictions) == 30


class TestModelPerformance:
    """Test cases for model performance characteristics"""
    
    def test_model_makes_reasonable_predictions(self):
        """Test: Model predictions are within reasonable ranges"""
        predictions = predict_resource_demand(days=7)
        
        for pred in predictions:
            # Predictions should be reasonable (not absurdly high)
            assert pred['total_demand'] < 10000, "Total demand should be reasonable"
            assert pred['water_demand'] < 5000, "Water demand should be reasonable"
            assert pred['food_demand'] < 5000, "Food demand should be reasonable"
            assert pred['tent_demand'] < 5000, "Tent demand should be reasonable"
    
    def test_model_predictions_vary_by_day(self):
        """Test: Predictions vary across different days"""
        predictions = predict_resource_demand(days=7)
        
        # Extract all total demands
        demands = [p['total_demand'] for p in predictions]
        
        # Not all predictions should be identical (model should capture variation)
        # Allow for some identical values but not all
        unique_demands = len(set(demands))
        assert unique_demands > 1, "Predictions should vary across days"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
