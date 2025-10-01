"""
Utility functions for ML models
Includes data preprocessing, model saving/loading, and common operations
"""

import os
import pickle
import joblib
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf


def save_model_sklearn(model, filepath):
    """
    Save scikit-learn model to disk
    
    Args:
        model: Trained scikit-learn model
        filepath: Path to save the model (e.g., 'models/saved_models/model.pkl')
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    joblib.dump(model, filepath)
    print(f"Model saved to {filepath}")


def load_model_sklearn(filepath):
    """
    Load scikit-learn model from disk
    
    Args:
        filepath: Path to the saved model
    
    Returns:
        Loaded model
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Model file not found: {filepath}")
    return joblib.load(filepath)


def save_model_keras(model, filepath):
    """
    Save Keras/TensorFlow model to disk
    
    Args:
        model: Trained Keras model
        filepath: Path to save the model (e.g., 'models/saved_models/model.h5')
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    model.save(filepath)
    print(f"Model saved to {filepath}")


def load_model_keras(filepath):
    """
    Load Keras/TensorFlow model from disk
    
    Args:
        filepath: Path to the saved model
    
    Returns:
        Loaded Keras model
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Model file not found: {filepath}")
    return tf.keras.models.load_model(filepath)


def save_scaler(scaler, filepath):
    """
    Save preprocessing scaler
    
    Args:
        scaler: Fitted scaler object
        filepath: Path to save the scaler
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    joblib.dump(scaler, filepath)
    print(f"Scaler saved to {filepath}")


def load_scaler(filepath):
    """
    Load preprocessing scaler
    
    Args:
        filepath: Path to the saved scaler
    
    Returns:
        Loaded scaler
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Scaler file not found: {filepath}")
    return joblib.load(filepath)


def create_sequences(data, seq_length):
    """
    Create sequences for time series forecasting
    
    Args:
        data: Time series data (numpy array or list)
        seq_length: Length of input sequences
    
    Returns:
        X: Input sequences
        y: Target values
    """
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i + seq_length])
        y.append(data[i + seq_length])
    return np.array(X), np.array(y)


def preprocess_time_series(df, column, seq_length=7, train_split=0.8):
    """
    Preprocess time series data for LSTM models
    
    Args:
        df: DataFrame with time series data
        column: Column name to use for prediction
        seq_length: Length of input sequences
        train_split: Ratio of training data
    
    Returns:
        X_train, y_train, X_test, y_test, scaler
    """
    # Extract values
    values = df[column].values.reshape(-1, 1)
    
    # Scale data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_values = scaler.fit_transform(values)
    
    # Create sequences
    X, y = create_sequences(scaled_values, seq_length)
    
    # Split into train/test
    train_size = int(len(X) * train_split)
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]
    
    return X_train, y_train, X_test, y_test, scaler


def generate_future_dates(start_date, days):
    """
    Generate future dates for forecasting
    
    Args:
        start_date: Starting date (datetime or string)
        days: Number of days to forecast
    
    Returns:
        List of date strings
    """
    if isinstance(start_date, str):
        start_date = pd.to_datetime(start_date)
    
    future_dates = []
    for i in range(1, days + 1):
        future_date = start_date + timedelta(days=i)
        future_dates.append(future_date.strftime('%Y-%m-%d'))
    
    return future_dates


def calculate_aqi_category(aqi_value):
    """
    Categorize AQI value into health categories
    
    Args:
        aqi_value: AQI numeric value
    
    Returns:
        Category string
    """
    if aqi_value <= 50:
        return "Good"
    elif aqi_value <= 100:
        return "Moderate"
    elif aqi_value <= 150:
        return "Unhealthy for Sensitive Groups"
    elif aqi_value <= 200:
        return "Unhealthy"
    elif aqi_value <= 300:
        return "Very Unhealthy"
    else:
        return "Hazardous"


def create_mock_time_series(days=365, start_value=100, noise_level=10):
    """
    Create mock time series data for demonstration
    
    Args:
        days: Number of days
        start_value: Starting value
        noise_level: Amount of random noise
    
    Returns:
        DataFrame with date and value columns
    """
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    
    # Create synthetic trend with seasonality
    t = np.arange(days)
    trend = start_value + 0.05 * t
    seasonality = 20 * np.sin(2 * np.pi * t / 365)
    noise = np.random.normal(0, noise_level, days)
    
    values = trend + seasonality + noise
    values = np.clip(values, 0, None)  # Ensure non-negative
    
    df = pd.DataFrame({
        'date': dates,
        'value': values
    })
    
    return df


def prepare_features_for_prediction(input_data, feature_names):
    """
    Prepare input features for model prediction
    
    Args:
        input_data: Dictionary of feature values
        feature_names: List of expected feature names in order
    
    Returns:
        numpy array ready for prediction
    """
    features = []
    for feature in feature_names:
        if feature in input_data:
            features.append(input_data[feature])
        else:
            features.append(0)  # Default value for missing features
    
    return np.array([features])


def calculate_metrics(y_true, y_pred):
    """
    Calculate evaluation metrics
    
    Args:
        y_true: True values
        y_pred: Predicted values
    
    Returns:
        Dictionary of metrics
    """
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)
    
    return {
        'mae': float(mae),
        'mse': float(mse),
        'rmse': float(rmse),
        'r2': float(r2)
    }
