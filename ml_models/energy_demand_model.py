"""
Energy Demand Prediction Model
Uses regression to forecast electricity demand based on various factors
Considers population, temperature, time of year, and infrastructure
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from ml_models.utils import (
    save_model_sklearn,
    load_model_sklearn,
    save_scaler,
    load_scaler,
    calculate_metrics,
    prepare_features_for_prediction
)


class EnergyDemandModel:
    """
    Machine learning model for predicting urban energy demand
    """
    
    def __init__(self, model_type='random_forest'):
        """
        Initialize energy demand model
        
        Args:
            model_type: 'random_forest' or 'gradient_boosting'
        """
        self.model_type = model_type
        self.model = None
        self.scaler = None
        self.feature_names = [
            'population',
            'temperature',
            'month',
            'day_of_week',
            'is_weekend',
            'industrial_zones',
            'residential_areas',
            'commercial_areas'
        ]
        self.model_path = f'ml_models/saved_models/energy_demand_{model_type}.pkl'
        self.scaler_path = 'ml_models/saved_models/energy_scaler.pkl'
    
    def build_model(self):
        """
        Build regression model
        
        Returns:
            Scikit-learn regression model
        """
        if self.model_type == 'random_forest':
            model = RandomForestRegressor(
                n_estimators=100,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42
            )
        else:  # gradient_boosting
            model = GradientBoostingRegressor(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=42
            )
        
        return model
    
    def prepare_features(self, df):
        """
        Extract and engineer features from raw data
        
        Args:
            df: DataFrame with columns [date, city, consumption_kwh, temperature, population, ...]
        
        Returns:
            X: Feature matrix
            y: Target variable (energy consumption)
        """
        df = df.copy()
        
        # Convert date to datetime if needed
        if not pd.api.types.is_datetime64_any_dtype(df['date']):
            df['date'] = pd.to_datetime(df['date'])
        
        # Extract temporal features
        df['month'] = df['date'].dt.month
        df['day_of_week'] = df['date'].dt.dayofweek
        df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
        
        # Fill missing values with defaults if not present
        if 'industrial_zones' not in df.columns:
            df['industrial_zones'] = 5  # Default value
        if 'residential_areas' not in df.columns:
            df['residential_areas'] = 20  # Default value
        if 'commercial_areas' not in df.columns:
            df['commercial_areas'] = 10  # Default value
        
        # Select features
        X = df[self.feature_names].values
        y = df['consumption_kwh'].values if 'consumption_kwh' in df.columns else None
        
        return X, y
    
    def train(self, df, test_size=0.2):
        """
        Train the energy demand model
        
        Args:
            df: Training data DataFrame
            test_size: Proportion of data for testing
        
        Returns:
            Dictionary with training metrics
        """
        print("Training energy demand prediction model...")
        
        # Prepare features
        X, y = self.prepare_features(df)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Build and train model
        self.model = self.build_model()
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        metrics = calculate_metrics(y_test, y_pred)
        
        print(f"Training completed!")
        print(f"Model: {self.model_type}")
        print(f"R² Score: {metrics['r2']:.4f}")
        print(f"RMSE: {metrics['rmse']:.2f} kWh")
        
        # Save model and scaler
        save_model_sklearn(self.model, self.model_path)
        save_scaler(self.scaler, self.scaler_path)
        
        return metrics
    
    def load(self):
        """
        Load trained model and scaler from disk
        """
        try:
            self.model = load_model_sklearn(self.model_path)
            self.scaler = load_scaler(self.scaler_path)
            print("Energy demand model loaded successfully")
        except FileNotFoundError:
            print("No saved model found. Using mock predictions.")
            self.model = None
    
    def predict(self, input_data):
        """
        Predict energy demand
        
        Args:
            input_data: Dictionary or DataFrame with required features
        
        Returns:
            Predicted energy consumption (kWh)
        """
        if self.model is None:
            return self._generate_mock_prediction(input_data)
        
        # Convert input to feature array
        if isinstance(input_data, dict):
            X = prepare_features_for_prediction(input_data, self.feature_names)
        else:
            X, _ = self.prepare_features(input_data)
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        
        # Predict
        prediction = self.model.predict(X_scaled)
        
        return float(prediction[0]) if len(prediction) == 1 else prediction.tolist()
    
    def predict_scenario(self, city_data, scenario_adjustments):
        """
        Predict energy demand with scenario adjustments
        
        Args:
            city_data: Base city data dictionary
            scenario_adjustments: Dictionary with adjustments (e.g., {'solar_percentage': 30})
        
        Returns:
            Dictionary with predictions and impact analysis
        """
        # Baseline prediction
        baseline_demand = self.predict(city_data)
        
        # Apply scenario adjustments
        adjusted_data = city_data.copy()
        
        # Solar energy reduces demand from grid
        if 'solar_percentage' in scenario_adjustments:
            solar_reduction = scenario_adjustments['solar_percentage'] / 100.0
            adjusted_demand = baseline_demand * (1 - solar_reduction)
        else:
            adjusted_demand = baseline_demand
        
        # Green spaces can reduce cooling demand
        if 'green_spaces_increase' in scenario_adjustments:
            green_reduction = scenario_adjustments['green_spaces_increase'] / 100.0 * 0.05  # 5% max reduction
            adjusted_demand *= (1 - green_reduction)
        
        # Electric transport increases demand but cleaner
        if 'electric_transport_percentage' in scenario_adjustments:
            transport_increase = scenario_adjustments['electric_transport_percentage'] / 100.0 * 0.15  # 15% increase
            adjusted_demand *= (1 + transport_increase)
        
        return {
            'baseline_demand_kwh': float(baseline_demand),
            'adjusted_demand_kwh': float(adjusted_demand),
            'change_kwh': float(adjusted_demand - baseline_demand),
            'change_percentage': float((adjusted_demand - baseline_demand) / baseline_demand * 100),
            'scenario': scenario_adjustments
        }
    
    def _generate_mock_prediction(self, input_data):
        """
        Generate mock prediction when model is not trained
        
        Args:
            input_data: Input features
        
        Returns:
            Mock energy consumption value
        """
        # Simple heuristic based on population and temperature
        population = input_data.get('population', 1000000)
        temperature = input_data.get('temperature', 30)
        
        # Base demand: ~500 kWh per 1000 people
        base_demand = (population / 1000) * 500
        
        # Temperature effect: higher temp = more cooling demand
        temp_factor = 1 + (temperature - 25) * 0.02
        
        # Add some randomness
        noise = np.random.normal(0, base_demand * 0.05)
        
        demand = base_demand * temp_factor + noise
        return max(0, float(demand))
    
    def get_feature_importance(self):
        """
        Get feature importance scores
        
        Returns:
            Dictionary mapping feature names to importance scores
        """
        if self.model is None or not hasattr(self.model, 'feature_importances_'):
            return None
        
        importances = self.model.feature_importances_
        return dict(zip(self.feature_names, [float(imp) for imp in importances]))


def predict_city_energy_demand(city='Lahore', scenario=None):
    """
    Convenience function to predict energy demand for a city
    
    Args:
        city: City name
        scenario: Optional scenario adjustments dictionary
    
    Returns:
        Prediction dictionary
    """
    # City baseline data (mock)
    city_data = {
        'Lahore': {'population': 11126285, 'temperature': 32, 'industrial_zones': 15, 'residential_areas': 45, 'commercial_areas': 25},
        'Karachi': {'population': 14910352, 'temperature': 30, 'industrial_zones': 20, 'residential_areas': 50, 'commercial_areas': 30},
        'Faisalabad': {'population': 3203846, 'temperature': 33, 'industrial_zones': 25, 'residential_areas': 35, 'commercial_areas': 15},
        'Sargodha': {'population': 659862, 'temperature': 31, 'industrial_zones': 8, 'residential_areas': 25, 'commercial_areas': 10}
    }
    
    base_data = city_data.get(city, city_data['Lahore'])
    base_data['month'] = datetime.now().month
    base_data['day_of_week'] = datetime.now().weekday()
    base_data['is_weekend'] = 1 if base_data['day_of_week'] >= 5 else 0
    
    model = EnergyDemandModel()
    model.load()
    
    if scenario:
        result = model.predict_scenario(base_data, scenario)
    else:
        demand = model.predict(base_data)
        result = {
            'city': city,
            'demand_kwh': demand,
            'demand_mwh': demand / 1000,
            'per_capita_kwh': demand / base_data['population']
        }
    
    result['city'] = city
    return result


if __name__ == '__main__':
    # Demo: Generate mock data and predictions
    print("=== Energy Demand Model Demo ===\n")
    
    # Generate mock training data
    dates = pd.date_range(end=datetime.now(), periods=365, freq='D')
    cities = ['Lahore', 'Karachi', 'Faisalabad', 'Sargodha']
    
    data = []
    for city in cities:
        for date in dates:
            population = {'Lahore': 11000000, 'Karachi': 15000000, 'Faisalabad': 3200000, 'Sargodha': 660000}[city]
            temp = 25 + 10 * np.sin(2 * np.pi * date.dayofyear / 365) + np.random.randn() * 3
            consumption = (population / 1000) * 500 * (1 + (temp - 25) * 0.02) + np.random.randn() * 50000
            
            data.append({
                'date': date,
                'city': city,
                'population': population,
                'temperature': temp,
                'consumption_kwh': max(0, consumption),
                'industrial_zones': np.random.randint(5, 25),
                'residential_areas': np.random.randint(20, 50),
                'commercial_areas': np.random.randint(10, 30)
            })
    
    df = pd.DataFrame(data)
    print(f"Generated mock data: {len(df)} records\n")
    
    # Predict for Lahore
    print("Predicting energy demand for Lahore...")
    result = predict_city_energy_demand('Lahore')
    print(f"\nBaseline Demand:")
    print(f"  Total: {result['demand_kwh']:,.0f} kWh ({result['demand_mwh']:,.2f} MWh)")
    print(f"  Per Capita: {result['per_capita_kwh']:.2f} kWh")
    
    # Scenario analysis
    print("\n\nScenario: 30% solar energy + 20% more green spaces")
    scenario_result = predict_city_energy_demand('Lahore', {
        'solar_percentage': 30,
        'green_spaces_increase': 20
    })
    print(f"  Baseline: {scenario_result['baseline_demand_kwh']:,.0f} kWh")
    print(f"  Adjusted: {scenario_result['adjusted_demand_kwh']:,.0f} kWh")
    print(f"  Change: {scenario_result['change_kwh']:,.0f} kWh ({scenario_result['change_percentage']:.1f}%)")
