import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import joblib

def train_prediction_model():
    """
    Train a machine learning model to predict resource demand.
    Uses RandomForest to predict demand based on historical patterns.
    
    Returns:
        Trained model and feature scaler
    """
    try:
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.preprocessing import StandardScaler, LabelEncoder
        from sklearn.model_selection import train_test_split
        
        # Load historical data
        data_path = os.path.join(os.path.dirname(__file__), '../../data/historical_requests.csv')
        
        if not os.path.exists(data_path):
            print(f"Warning: Historical data not found at {data_path}")
            return None, None, None, None
        
        df = pd.read_csv(data_path)
        
        # Feature engineering
        df['date'] = pd.to_datetime(df['date'])
        df['day_of_week'] = df['date'].dt.dayofweek
        df['day_of_month'] = df['date'].dt.day
        df['month'] = df['date'].dt.month
        
        # Encode categorical variables
        le_need = LabelEncoder()
        le_urgency = LabelEncoder()
        
        df['need_type_encoded'] = le_need.fit_transform(df['need_type'])
        df['urgency_encoded'] = le_urgency.fit_transform(df['urgency'])
        
        # Features for prediction
        features = ['lat', 'lon', 'day_of_week', 'day_of_month', 'month', 
                   'need_type_encoded', 'urgency_encoded']
        X = df[features]
        y = df['people']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
        model.fit(X_train_scaled, y_train)
        
        # Evaluate
        train_score = model.score(X_train_scaled, y_train)
        test_score = model.score(X_test_scaled, y_test)
        
        print(f"Model trained successfully. Train R²: {train_score:.3f}, Test R²: {test_score:.3f}")
        
        # Save model
        model_dir = os.path.join(os.path.dirname(__file__), '../models')
        os.makedirs(model_dir, exist_ok=True)
        
        joblib.dump(model, os.path.join(model_dir, 'demand_model.pkl'))
        joblib.dump(scaler, os.path.join(model_dir, 'scaler.pkl'))
        joblib.dump(le_need, os.path.join(model_dir, 'le_need.pkl'))
        joblib.dump(le_urgency, os.path.join(model_dir, 'le_urgency.pkl'))
        
        return model, scaler, le_need, le_urgency
        
    except ImportError:
        print("Warning: scikit-learn not installed. Install with: pip install scikit-learn")
        return None, None, None, None
    except Exception as e:
        print(f"Error training model: {str(e)}")
        return None, None, None, None

def load_prediction_model():
    """
    Load trained prediction model from disk.
    
    Returns:
        Tuple of (model, scaler, le_need, le_urgency)
    """
    try:
        model_dir = os.path.join(os.path.dirname(__file__), '../models')
        
        model = joblib.load(os.path.join(model_dir, 'demand_model.pkl'))
        scaler = joblib.load(os.path.join(model_dir, 'scaler.pkl'))
        le_need = joblib.load(os.path.join(model_dir, 'le_need.pkl'))
        le_urgency = joblib.load(os.path.join(model_dir, 'le_urgency.pkl'))
        
        return model, scaler, le_need, le_urgency
        
    except FileNotFoundError:
        print("Model not found. Training new model...")
        return train_prediction_model()
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        return None, None, None, None

def predict_resource_demand(days=7):
    """
    Predict resource demand for next N days.
    
    Args:
        days: Number of days to predict (default 7)
    
    Returns:
        List of prediction dictionaries with date and estimated demand
    """
    try:
        # Load or train model
        model, scaler, le_need, le_urgency = load_prediction_model()
        
        if model is None:
            return [{
                'date': (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d'),
                'total_demand': 0,
                'water_demand': 0,
                'food_demand': 0,
                'tent_demand': 0,
                'note': 'Model not available'
            } for i in range(days)]
        
        predictions = []
        
        # Sample locations (in real scenario, use historical hotspots)
        sample_locations = [
            {'lat': 33.6844, 'lon': 73.0479},  # Islamabad region
            {'lat': 31.5204, 'lon': 74.3587},  # Lahore region
            {'lat': 24.8607, 'lon': 67.0011},  # Karachi region
        ]
        
        need_types = ['water', 'food', 'tent']
        urgency_levels = ['high', 'medium', 'low']
        
        for day in range(days):
            target_date = datetime.now() + timedelta(days=day)
            day_predictions = []
            
            for location in sample_locations:
                for need in need_types:
                    for urgency in urgency_levels:
                        # Prepare features
                        features = [
                            location['lat'],
                            location['lon'],
                            target_date.weekday(),
                            target_date.day,
                            target_date.month,
                            le_need.transform([need])[0],
                            le_urgency.transform([urgency])[0]
                        ]
                        
                        # Scale and predict
                        features_scaled = scaler.transform([features])
                        predicted_people = model.predict(features_scaled)[0]
                        
                        day_predictions.append({
                            'need_type': need,
                            'urgency': urgency,
                            'predicted_people': max(0, int(predicted_people))
                        })
            
            # Aggregate predictions
            total_demand = sum(p['predicted_people'] for p in day_predictions)
            water_demand = sum(p['predicted_people'] for p in day_predictions if p['need_type'] == 'water')
            food_demand = sum(p['predicted_people'] for p in day_predictions if p['need_type'] == 'food')
            tent_demand = sum(p['predicted_people'] for p in day_predictions if p['need_type'] == 'tent')
            
            predictions.append({
                'date': target_date.strftime('%Y-%m-%d'),
                'total_demand': total_demand,
                'water_demand': water_demand,
                'food_demand': food_demand,
                'tent_demand': tent_demand
            })
        
        return predictions
        
    except Exception as e:
        print(f"Error predicting demand: {str(e)}")
        return [{
            'date': (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d'),
            'total_demand': 0,
            'error': str(e)
        } for i in range(days)]
