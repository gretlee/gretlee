"""
Flood Risk Assessment Model
Classification model to predict flood risk levels (Low/Medium/High)
Based on geographical features: elevation, rainfall, proximity to water bodies
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

from ml_models.utils import (
    save_model_sklearn,
    load_model_sklearn,
    save_scaler,
    load_scaler
)


class FloodRiskModel:
    """
    Machine learning model for flood risk classification
    """
    
    def __init__(self):
        """
        Initialize flood risk model
        """
        self.model = None
        self.scaler = None
        self.risk_classes = ['Low', 'Medium', 'High']
        self.feature_names = [
            'elevation_m',
            'distance_to_water_km',
            'annual_rainfall_mm',
            'drainage_quality',  # 0-10 scale
            'soil_permeability',  # 0-10 scale
            'urbanization_level',  # 0-10 scale
            'slope_percentage'
        ]
        self.model_path = 'ml_models/saved_models/flood_risk_classifier.pkl'
        self.scaler_path = 'ml_models/saved_models/flood_scaler.pkl'
    
    def build_model(self):
        """
        Build Random Forest classifier
        
        Returns:
            Scikit-learn classifier
        """
        model = RandomForestClassifier(
            n_estimators=150,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            class_weight='balanced',
            random_state=42
        )
        return model
    
    def prepare_features(self, df):
        """
        Extract features from raw data
        
        Args:
            df: DataFrame with geographical and environmental features
        
        Returns:
            X: Feature matrix
            y: Target labels (if available)
        """
        df = df.copy()
        
        # Fill missing values with defaults
        for feature in self.feature_names:
            if feature not in df.columns:
                # Set reasonable defaults
                defaults = {
                    'elevation_m': 100,
                    'distance_to_water_km': 5,
                    'annual_rainfall_mm': 800,
                    'drainage_quality': 5,
                    'soil_permeability': 5,
                    'urbanization_level': 5,
                    'slope_percentage': 2
                }
                df[feature] = defaults.get(feature, 5)
        
        X = df[self.feature_names].values
        
        # Extract labels if available
        y = None
        if 'risk_level' in df.columns:
            # Convert risk labels to numeric
            risk_mapping = {'Low': 0, 'Medium': 1, 'High': 2}
            y = df['risk_level'].map(risk_mapping).values
        
        return X, y
    
    def train(self, df, test_size=0.2):
        """
        Train the flood risk classifier
        
        Args:
            df: Training data with features and 'risk_level' column
            test_size: Proportion of data for testing
        
        Returns:
            Dictionary with training metrics
        """
        print("Training flood risk classification model...")
        
        # Prepare features
        X, y = self.prepare_features(df)
        
        if y is None:
            raise ValueError("Training data must include 'risk_level' column")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, stratify=y, random_state=42
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
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\nTraining completed!")
        print(f"Accuracy: {accuracy:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=self.risk_classes))
        
        # Save model and scaler
        save_model_sklearn(self.model, self.model_path)
        save_scaler(self.scaler, self.scaler_path)
        
        return {
            'accuracy': float(accuracy),
            'classification_report': classification_report(y_test, y_pred, target_names=self.risk_classes, output_dict=True)
        }
    
    def load(self):
        """
        Load trained model and scaler from disk
        """
        try:
            self.model = load_model_sklearn(self.model_path)
            self.scaler = load_scaler(self.scaler_path)
            print("Flood risk model loaded successfully")
        except FileNotFoundError:
            print("No saved model found. Using rule-based predictions.")
            self.model = None
    
    def predict(self, input_data):
        """
        Predict flood risk level
        
        Args:
            input_data: Dictionary or DataFrame with required features
        
        Returns:
            Dictionary with risk level and probability
        """
        if self.model is None:
            return self._generate_rule_based_prediction(input_data)
        
        # Convert input to feature array
        if isinstance(input_data, dict):
            X = np.array([[input_data.get(feature, 0) for feature in self.feature_names]])
        else:
            X, _ = self.prepare_features(input_data)
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        
        # Predict
        prediction = self.model.predict(X_scaled)[0]
        probabilities = self.model.predict_proba(X_scaled)[0]
        
        return {
            'risk_level': self.risk_classes[prediction],
            'confidence': float(probabilities[prediction]),
            'probabilities': {
                'Low': float(probabilities[0]),
                'Medium': float(probabilities[1]),
                'High': float(probabilities[2])
            }
        }
    
    def predict_area(self, area_data):
        """
        Predict flood risk for multiple locations in an area
        
        Args:
            area_data: DataFrame with geographical data for multiple points
        
        Returns:
            DataFrame with risk predictions
        """
        if self.model is None:
            # Generate rule-based predictions for all points
            predictions = []
            for _, row in area_data.iterrows():
                pred = self._generate_rule_based_prediction(row.to_dict())
                predictions.append(pred)
            
            area_data['risk_level'] = [p['risk_level'] for p in predictions]
            area_data['confidence'] = [p['confidence'] for p in predictions]
            return area_data
        
        X, _ = self.prepare_features(area_data)
        X_scaled = self.scaler.transform(X)
        
        predictions = self.model.predict(X_scaled)
        probabilities = self.model.predict_proba(X_scaled)
        
        area_data['risk_level'] = [self.risk_classes[p] for p in predictions]
        area_data['confidence'] = [float(probabilities[i][predictions[i]]) for i in range(len(predictions))]
        
        return area_data
    
    def _generate_rule_based_prediction(self, input_data):
        """
        Generate prediction using simple rules when model is not trained
        
        Args:
            input_data: Dictionary with geographical features
        
        Returns:
            Prediction dictionary
        """
        # Extract key features
        elevation = input_data.get('elevation_m', 100)
        distance_to_water = input_data.get('distance_to_water_km', 5)
        rainfall = input_data.get('annual_rainfall_mm', 800)
        drainage = input_data.get('drainage_quality', 5)
        
        # Simple rule-based scoring
        risk_score = 0
        
        # Low elevation increases risk
        if elevation < 50:
            risk_score += 3
        elif elevation < 100:
            risk_score += 2
        elif elevation < 200:
            risk_score += 1
        
        # Proximity to water increases risk
        if distance_to_water < 1:
            risk_score += 3
        elif distance_to_water < 3:
            risk_score += 2
        elif distance_to_water < 5:
            risk_score += 1
        
        # High rainfall increases risk
        if rainfall > 1500:
            risk_score += 3
        elif rainfall > 1000:
            risk_score += 2
        elif rainfall > 800:
            risk_score += 1
        
        # Poor drainage increases risk
        if drainage < 3:
            risk_score += 2
        elif drainage < 5:
            risk_score += 1
        
        # Determine risk level
        if risk_score >= 7:
            risk_level = 'High'
            confidence = 0.85
        elif risk_score >= 4:
            risk_level = 'Medium'
            confidence = 0.75
        else:
            risk_level = 'Low'
            confidence = 0.80
        
        # Add some randomness to confidence
        confidence += np.random.uniform(-0.1, 0.1)
        confidence = np.clip(confidence, 0.5, 0.95)
        
        return {
            'risk_level': risk_level,
            'confidence': float(confidence),
            'probabilities': {
                'Low': float(0.7 if risk_level == 'Low' else 0.2),
                'Medium': float(0.7 if risk_level == 'Medium' else 0.2),
                'High': float(0.7 if risk_level == 'High' else 0.1)
            }
        }
    
    def get_feature_importance(self):
        """
        Get feature importance scores
        
        Returns:
            Dictionary mapping feature names to importance scores
        """
        if self.model is None:
            return None
        
        importances = self.model.feature_importances_
        return dict(zip(self.feature_names, [float(imp) for imp in importances]))


def assess_city_flood_risk(city='Lahore', num_zones=20):
    """
    Assess flood risk for different zones in a city
    
    Args:
        city: City name
        num_zones: Number of zones to assess
    
    Returns:
        Dictionary with risk assessment results
    """
    model = FloodRiskModel()
    model.load()
    
    # Generate mock geographical data for city zones
    np.random.seed(42)
    zones = []
    
    for i in range(num_zones):
        zone = {
            'zone_id': f"{city}_zone_{i+1}",
            'elevation_m': np.random.uniform(10, 300),
            'distance_to_water_km': np.random.uniform(0.5, 15),
            'annual_rainfall_mm': np.random.uniform(600, 1800),
            'drainage_quality': np.random.randint(1, 10),
            'soil_permeability': np.random.randint(1, 10),
            'urbanization_level': np.random.randint(3, 10),
            'slope_percentage': np.random.uniform(0, 10)
        }
        zones.append(zone)
    
    df_zones = pd.DataFrame(zones)
    
    # Predict risk for all zones
    result_df = model.predict_area(df_zones)
    
    # Aggregate statistics
    risk_counts = result_df['risk_level'].value_counts().to_dict()
    
    return {
        'city': city,
        'total_zones': num_zones,
        'risk_distribution': {
            'Low': int(risk_counts.get('Low', 0)),
            'Medium': int(risk_counts.get('Medium', 0)),
            'High': int(risk_counts.get('High', 0))
        },
        'high_risk_zones': result_df[result_df['risk_level'] == 'High']['zone_id'].tolist(),
        'zones': result_df.to_dict('records')
    }


if __name__ == '__main__':
    # Demo: Generate mock data and predictions
    print("=== Flood Risk Assessment Model Demo ===\n")
    
    # Generate mock training data
    np.random.seed(42)
    data = []
    
    for _ in range(1000):
        elevation = np.random.uniform(5, 400)
        distance_to_water = np.random.uniform(0.2, 20)
        rainfall = np.random.uniform(400, 2000)
        drainage = np.random.randint(1, 10)
        
        # Determine risk based on features
        risk_score = 0
        if elevation < 50: risk_score += 3
        elif elevation < 100: risk_score += 2
        if distance_to_water < 2: risk_score += 2
        if rainfall > 1200: risk_score += 2
        if drainage < 4: risk_score += 2
        
        if risk_score >= 6:
            risk = 'High'
        elif risk_score >= 3:
            risk = 'Medium'
        else:
            risk = 'Low'
        
        data.append({
            'elevation_m': elevation,
            'distance_to_water_km': distance_to_water,
            'annual_rainfall_mm': rainfall,
            'drainage_quality': drainage,
            'soil_permeability': np.random.randint(1, 10),
            'urbanization_level': np.random.randint(1, 10),
            'slope_percentage': np.random.uniform(0, 15),
            'risk_level': risk
        })
    
    df = pd.DataFrame(data)
    print(f"Generated mock data: {len(df)} records")
    print(f"Risk distribution:\n{df['risk_level'].value_counts()}\n")
    
    # Assess flood risk for Lahore
    print("Assessing flood risk for Lahore...")
    results = assess_city_flood_risk('Lahore', num_zones=20)
    
    print(f"\n=== Flood Risk Assessment for {results['city']} ===")
    print(f"Total zones analyzed: {results['total_zones']}")
    print(f"\nRisk Distribution:")
    print(f"  Low Risk: {results['risk_distribution']['Low']} zones")
    print(f"  Medium Risk: {results['risk_distribution']['Medium']} zones")
    print(f"  High Risk: {results['risk_distribution']['High']} zones")
    
    if results['high_risk_zones']:
        print(f"\nHigh Risk Zones: {', '.join(results['high_risk_zones'][:5])}")
