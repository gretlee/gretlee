"""
Air Quality Index (AQI) Forecasting Model
Uses LSTM neural network for time series prediction of air quality metrics
Predicts PM2.5, PM10, NO2, SO2 levels for Pakistani cities
"""

import numpy as np
import pandas as pd
from datetime import datetime
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler

from ml_models.utils import (
    save_model_keras, 
    load_model_keras, 
    save_scaler, 
    load_scaler,
    create_sequences,
    generate_future_dates,
    calculate_aqi_category,
    create_mock_time_series
)


class AQIForecastModel:
    """
    LSTM-based Air Quality Index forecasting model
    """
    
    def __init__(self, seq_length=7, features=['pm25', 'pm10', 'no2', 'so2']):
        """
        Initialize AQI forecast model
        
        Args:
            seq_length: Number of past days to use for prediction
            features: List of pollutant features to predict
        """
        self.seq_length = seq_length
        self.features = features
        self.model = None
        self.scalers = {}
        self.model_path = 'ml_models/saved_models/aqi_lstm_model.h5'
        self.scaler_path = 'ml_models/saved_models/aqi_scaler.pkl'
    
    def build_model(self, input_shape):
        """
        Build LSTM neural network architecture
        
        Args:
            input_shape: Shape of input data (seq_length, n_features)
        
        Returns:
            Compiled Keras model
        """
        model = Sequential([
            LSTM(64, activation='relu', return_sequences=True, input_shape=input_shape),
            Dropout(0.2),
            LSTM(32, activation='relu', return_sequences=False),
            Dropout(0.2),
            Dense(16, activation='relu'),
            Dense(len(self.features))  # Output layer for each feature
        ])
        
        model.compile(
            optimizer='adam',
            loss='mse',
            metrics=['mae']
        )
        
        return model
    
    def prepare_data(self, df, city=None):
        """
        Prepare and scale data for training
        
        Args:
            df: DataFrame with columns [date, city, pm25, pm10, no2, so2]
            city: Filter by specific city (optional)
        
        Returns:
            X_train, y_train, X_test, y_test
        """
        # Filter by city if specified
        if city:
            df = df[df['city'] == city].copy()
        
        # Sort by date
        df = df.sort_values('date')
        
        # Extract feature values
        feature_data = df[self.features].values
        
        # Scale each feature
        scaled_data = np.zeros_like(feature_data, dtype=float)
        for i, feature in enumerate(self.features):
            scaler = MinMaxScaler(feature_range=(0, 1))
            scaled_data[:, i] = scaler.fit_transform(feature_data[:, i].reshape(-1, 1)).flatten()
            self.scalers[feature] = scaler
        
        # Create sequences
        X, y = create_sequences(scaled_data, self.seq_length)
        
        # Split train/test (80/20)
        train_size = int(len(X) * 0.8)
        X_train = X[:train_size]
        y_train = y[:train_size]
        X_test = X[train_size:]
        y_test = y[train_size:]
        
        return X_train, y_train, X_test, y_test
    
    def train(self, df, city=None, epochs=50, batch_size=32):
        """
        Train the LSTM model
        
        Args:
            df: Training data DataFrame
            city: City to train on (optional)
            epochs: Number of training epochs
            batch_size: Batch size for training
        
        Returns:
            Training history
        """
        print(f"Training AQI forecast model for {city if city else 'all cities'}...")
        
        # Prepare data
        X_train, y_train, X_test, y_test = self.prepare_data(df, city)
        
        print(f"Training data shape: {X_train.shape}")
        print(f"Test data shape: {X_test.shape}")
        
        # Build model
        input_shape = (X_train.shape[1], X_train.shape[2])
        self.model = self.build_model(input_shape)
        
        # Train model
        history = self.model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_data=(X_test, y_test),
            verbose=1
        )
        
        # Save model and scalers
        save_model_keras(self.model, self.model_path)
        save_scaler(self.scalers, self.scaler_path)
        
        print("Training completed!")
        return history
    
    def load(self):
        """
        Load trained model and scalers from disk
        """
        try:
            self.model = load_model_keras(self.model_path)
            self.scalers = load_scaler(self.scaler_path)
            print("Model loaded successfully")
        except FileNotFoundError:
            print("No saved model found. Using mock predictions.")
            self.model = None
    
    def predict(self, recent_data, days=7):
        """
        Predict AQI for future days
        
        Args:
            recent_data: Recent pollutant data (last seq_length days)
                        Shape: (seq_length, n_features)
            days: Number of days to forecast
        
        Returns:
            predictions: Dictionary with predicted values for each day
        """
        if self.model is None:
            print("Warning: Using mock predictions (model not trained)")
            return self._generate_mock_predictions(days)
        
        predictions = []
        current_sequence = recent_data.copy()
        
        # Scale input data
        scaled_sequence = np.zeros_like(current_sequence, dtype=float)
        for i, feature in enumerate(self.features):
            scaled_sequence[:, i] = self.scalers[feature].transform(
                current_sequence[:, i].reshape(-1, 1)
            ).flatten()
        
        # Predict iteratively
        for _ in range(days):
            # Reshape for model input
            X_input = scaled_sequence[-self.seq_length:].reshape(1, self.seq_length, len(self.features))
            
            # Predict next day
            y_pred_scaled = self.model.predict(X_input, verbose=0)[0]
            
            # Inverse transform predictions
            y_pred = np.zeros_like(y_pred_scaled)
            for i, feature in enumerate(self.features):
                y_pred[i] = self.scalers[feature].inverse_transform(
                    y_pred_scaled[i].reshape(-1, 1)
                )[0, 0]
            
            predictions.append(y_pred)
            
            # Update sequence
            scaled_sequence = np.vstack([scaled_sequence, y_pred_scaled])
        
        return self._format_predictions(predictions, days)
    
    def _format_predictions(self, predictions, days):
        """
        Format predictions into readable dictionary
        
        Args:
            predictions: List of prediction arrays
            days: Number of days predicted
        
        Returns:
            Formatted prediction dictionary
        """
        future_dates = generate_future_dates(datetime.now(), days)
        
        formatted = {
            'dates': future_dates,
            'predictions': {}
        }
        
        for i, feature in enumerate(self.features):
            feature_predictions = [pred[i] for pred in predictions]
            formatted['predictions'][feature] = [float(val) for val in feature_predictions]
        
        # Calculate overall AQI (simplified - using PM2.5 as primary indicator)
        pm25_values = formatted['predictions']['pm25']
        formatted['predictions']['aqi'] = [float(val * 2) for val in pm25_values]  # Simplified AQI calculation
        formatted['predictions']['category'] = [calculate_aqi_category(aqi) for aqi in formatted['predictions']['aqi']]
        
        return formatted
    
    def _generate_mock_predictions(self, days=7):
        """
        Generate mock predictions for demonstration when model is not trained
        
        Args:
            days: Number of days to forecast
        
        Returns:
            Mock prediction dictionary
        """
        future_dates = generate_future_dates(datetime.now(), days)
        
        # Generate realistic mock values with some variation
        np.random.seed(42)
        base_values = {
            'pm25': 75 + np.random.randn(days) * 10,
            'pm10': 120 + np.random.randn(days) * 15,
            'no2': 45 + np.random.randn(days) * 8,
            'so2': 25 + np.random.randn(days) * 5
        }
        
        # Calculate AQI from PM2.5 (simplified)
        aqi_values = base_values['pm25'] * 2
        
        return {
            'dates': future_dates,
            'predictions': {
                'pm25': [max(0, float(val)) for val in base_values['pm25']],
                'pm10': [max(0, float(val)) for val in base_values['pm10']],
                'no2': [max(0, float(val)) for val in base_values['no2']],
                'so2': [max(0, float(val)) for val in base_values['so2']],
                'aqi': [max(0, float(val)) for val in aqi_values],
                'category': [calculate_aqi_category(aqi) for aqi in aqi_values]
            }
        }


def get_aqi_forecast(city='Lahore', days=7):
    """
    Convenience function to get AQI forecast for a city
    
    Args:
        city: City name (Lahore, Karachi, Faisalabad, Sargodha)
        days: Number of days to forecast
    
    Returns:
        Forecast dictionary
    """
    model = AQIForecastModel()
    model.load()
    
    # Generate mock recent data (in real scenario, this would come from database)
    recent_data = np.array([
        [70, 110, 40, 22],  # 7 days ago
        [73, 115, 42, 24],
        [75, 118, 44, 25],
        [72, 112, 41, 23],
        [76, 120, 45, 26],
        [74, 116, 43, 24],
        [75, 118, 44, 25]   # Yesterday
    ])
    
    predictions = model.predict(recent_data, days=days)
    predictions['city'] = city
    
    return predictions


if __name__ == '__main__':
    # Demo: Generate mock data and train model
    print("=== AQI Forecast Model Demo ===\n")
    
    # Create mock historical data
    dates = pd.date_range(end=datetime.now(), periods=365, freq='D')
    cities = ['Lahore', 'Karachi', 'Faisalabad', 'Sargodha']
    
    data = []
    for city in cities:
        for date in dates:
            data.append({
                'date': date,
                'city': city,
                'pm25': np.random.normal(75, 15),
                'pm10': np.random.normal(120, 20),
                'no2': np.random.normal(45, 10),
                'so2': np.random.normal(25, 5)
            })
    
    df = pd.DataFrame(data)
    print(f"Generated mock data: {len(df)} records")
    print(df.head())
    
    # Get forecast
    print("\nGenerating forecast for Lahore (7 days)...")
    forecast = get_aqi_forecast('Lahore', days=7)
    
    print("\n=== Forecast Results ===")
    print(f"City: {forecast['city']}")
    for i, date in enumerate(forecast['dates']):
        print(f"\n{date}:")
        print(f"  PM2.5: {forecast['predictions']['pm25'][i]:.1f} µg/m³")
        print(f"  PM10: {forecast['predictions']['pm10'][i]:.1f} µg/m³")
        print(f"  AQI: {forecast['predictions']['aqi'][i]:.0f} ({forecast['predictions']['category'][i]})")
