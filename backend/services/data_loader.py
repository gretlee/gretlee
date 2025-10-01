"""
Data Loader Service
Handles loading and preprocessing of datasets from various sources
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class DataLoader:
    """
    Service for loading datasets used by ML models
    """
    
    def __init__(self, data_dir='data'):
        """
        Initialize data loader
        
        Args:
            data_dir: Base directory for data files
        """
        self.data_dir = data_dir
        self.raw_dir = os.path.join(data_dir, 'raw')
        self.processed_dir = os.path.join(data_dir, 'processed')
    
    def load_aqi_data(self, city=None, start_date=None, end_date=None):
        """
        Load air quality index data
        
        Args:
            city: Filter by city name (optional)
            start_date: Start date for filtering (optional)
            end_date: End date for filtering (optional)
        
        Returns:
            DataFrame with AQI data
        """
        aqi_file = os.path.join(self.raw_dir, 'aqi_data.csv')
        
        # If file doesn't exist, generate mock data
        if not os.path.exists(aqi_file):
            df = self._generate_mock_aqi_data()
        else:
            df = pd.read_csv(aqi_file)
            df['date'] = pd.to_datetime(df['date'])
        
        # Apply filters
        if city:
            df = df[df['city'] == city]
        
        if start_date:
            df = df[df['date'] >= pd.to_datetime(start_date)]
        
        if end_date:
            df = df[df['date'] <= pd.to_datetime(end_date)]
        
        return df
    
    def load_energy_data(self, city=None, start_date=None, end_date=None):
        """
        Load energy consumption data
        
        Args:
            city: Filter by city name (optional)
            start_date: Start date for filtering (optional)
            end_date: End date for filtering (optional)
        
        Returns:
            DataFrame with energy data
        """
        energy_file = os.path.join(self.raw_dir, 'energy_data.csv')
        
        # If file doesn't exist, generate mock data
        if not os.path.exists(energy_file):
            df = self._generate_mock_energy_data()
        else:
            df = pd.read_csv(energy_file)
            df['date'] = pd.to_datetime(df['date'])
        
        # Apply filters
        if city:
            df = df[df['city'] == city]
        
        if start_date:
            df = df[df['date'] >= pd.to_datetime(start_date)]
        
        if end_date:
            df = df[df['date'] <= pd.to_datetime(end_date)]
        
        return df
    
    def load_flood_risk_data(self, city=None):
        """
        Load flood risk geographical data
        
        Args:
            city: Filter by city name (optional)
        
        Returns:
            DataFrame with geographical features
        """
        flood_file = os.path.join(self.raw_dir, 'flood_risk_data.csv')
        
        # If file doesn't exist, generate mock data
        if not os.path.exists(flood_file):
            df = self._generate_mock_flood_data()
        else:
            df = pd.read_csv(flood_file)
        
        # Apply filters
        if city:
            df = df[df['city'] == city]
        
        return df
    
    def get_city_metadata(self, city):
        """
        Get metadata for a specific city
        
        Args:
            city: City name
        
        Returns:
            Dictionary with city information
        """
        # Mock city metadata
        cities = {
            'Lahore': {
                'population': 11126285,
                'area_km2': 1772,
                'coordinates': {'lat': 31.5497, 'lon': 74.3436},
                'province': 'Punjab',
                'industrial_zones': 15,
                'residential_areas': 45,
                'commercial_areas': 25
            },
            'Karachi': {
                'population': 14910352,
                'area_km2': 3527,
                'coordinates': {'lat': 24.8607, 'lon': 67.0011},
                'province': 'Sindh',
                'industrial_zones': 20,
                'residential_areas': 50,
                'commercial_areas': 30
            },
            'Faisalabad': {
                'population': 3203846,
                'area_km2': 1280,
                'coordinates': {'lat': 31.4504, 'lon': 73.1350},
                'province': 'Punjab',
                'industrial_zones': 25,
                'residential_areas': 35,
                'commercial_areas': 15
            },
            'Sargodha': {
                'population': 659862,
                'area_km2': 5854,
                'coordinates': {'lat': 32.0836, 'lon': 72.6711},
                'province': 'Punjab',
                'industrial_zones': 8,
                'residential_areas': 25,
                'commercial_areas': 10
            }
        }
        
        return cities.get(city, cities['Lahore'])
    
    def get_recent_aqi(self, city, days=7):
        """
        Get recent AQI data for a city
        
        Args:
            city: City name
            days: Number of recent days
        
        Returns:
            Recent AQI data as numpy array
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        df = self.load_aqi_data(city, start_date, end_date)
        
        if len(df) == 0:
            # Return mock data if no data available
            return self._generate_recent_aqi_mock(days)
        
        # Extract relevant columns
        return df[['pm25', 'pm10', 'no2', 'so2']].values
    
    def _generate_mock_aqi_data(self, days=365):
        """
        Generate mock AQI data for demonstration
        """
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        cities = ['Lahore', 'Karachi', 'Faisalabad', 'Sargodha']
        
        data = []
        for city in cities:
            for date in dates:
                # Generate synthetic pollution data with seasonality
                day_of_year = date.dayofyear
                seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * day_of_year / 365)
                
                data.append({
                    'date': date,
                    'city': city,
                    'pm25': max(10, np.random.normal(75 * seasonal_factor, 15)),
                    'pm10': max(15, np.random.normal(120 * seasonal_factor, 20)),
                    'no2': max(5, np.random.normal(45, 10)),
                    'so2': max(2, np.random.normal(25, 5)),
                    'co': max(1, np.random.normal(15, 3)),
                    'o3': max(10, np.random.normal(50, 8))
                })
        
        return pd.DataFrame(data)
    
    def _generate_mock_energy_data(self, days=365):
        """
        Generate mock energy consumption data
        """
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        cities = {
            'Lahore': 11126285,
            'Karachi': 14910352,
            'Faisalabad': 3203846,
            'Sargodha': 659862
        }
        
        data = []
        for city, population in cities.items():
            for date in dates:
                # Seasonal temperature variation
                day_of_year = date.dayofyear
                temp = 25 + 10 * np.sin(2 * np.pi * (day_of_year - 80) / 365) + np.random.randn() * 3
                
                # Energy consumption based on population and temperature
                base_consumption = (population / 1000) * 500
                temp_factor = 1 + (temp - 25) * 0.02
                consumption = base_consumption * temp_factor + np.random.randn() * base_consumption * 0.05
                
                data.append({
                    'date': date,
                    'city': city,
                    'population': population,
                    'temperature': max(10, temp),
                    'consumption_kwh': max(0, consumption),
                    'industrial_zones': {'Lahore': 15, 'Karachi': 20, 'Faisalabad': 25, 'Sargodha': 8}[city],
                    'residential_areas': {'Lahore': 45, 'Karachi': 50, 'Faisalabad': 35, 'Sargodha': 25}[city],
                    'commercial_areas': {'Lahore': 25, 'Karachi': 30, 'Faisalabad': 15, 'Sargodha': 10}[city]
                })
        
        return pd.DataFrame(data)
    
    def _generate_mock_flood_data(self, num_zones=50):
        """
        Generate mock flood risk geographical data
        """
        cities = ['Lahore', 'Karachi', 'Faisalabad', 'Sargodha']
        
        data = []
        for city in cities:
            for i in range(num_zones):
                data.append({
                    'city': city,
                    'zone_id': f"{city}_zone_{i+1}",
                    'elevation_m': np.random.uniform(10, 300),
                    'distance_to_water_km': np.random.uniform(0.5, 15),
                    'annual_rainfall_mm': np.random.uniform(600, 1800),
                    'drainage_quality': np.random.randint(1, 10),
                    'soil_permeability': np.random.randint(1, 10),
                    'urbanization_level': np.random.randint(3, 10),
                    'slope_percentage': np.random.uniform(0, 10)
                })
        
        return pd.DataFrame(data)
    
    def _generate_recent_aqi_mock(self, days=7):
        """
        Generate recent AQI mock data
        """
        return np.array([
            [70 + np.random.randn() * 5, 110 + np.random.randn() * 8, 40 + np.random.randn() * 3, 22 + np.random.randn() * 2]
            for _ in range(days)
        ])


# Singleton instance
data_loader = DataLoader()
