/**
 * Main App Component
 * Layout and state management for the Urban Sustainability Simulator
 */

import React, { useState, useEffect } from 'react';
import MapDashboard from './components/MapDashboard';
import ScenarioSelector from './components/ScenarioSelector';
import ChartsPanel from './components/ChartsPanel';
import { getCityOverview, runScenario } from './services/api';

function App() {
  const [selectedCity, setSelectedCity] = useState('Lahore');
  const [cityData, setCityData] = useState(null);
  const [scenarioResults, setScenarioResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const cities = ['Lahore', 'Karachi', 'Faisalabad', 'Sargodha'];

  // Load city overview data
  useEffect(() => {
    loadCityData();
  }, [selectedCity]);

  const loadCityData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await getCityOverview(selectedCity);
      setCityData(data);
    } catch (err) {
      setError('Failed to load city data: ' + err.message);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleRunScenario = async (scenarioParams) => {
    setLoading(true);
    setError(null);
    
    try {
      const results = await runScenario(selectedCity, scenarioParams);
      setScenarioResults(results);
    } catch (err) {
      setError('Failed to run scenario: ' + err.message);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCityChange = (city) => {
    setSelectedCity(city);
    setScenarioResults(null); // Reset scenario when changing city
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <h1>🌍 Urban Sustainability Simulator</h1>
          <p className="subtitle">AI-Driven Forecasting for Pakistani Cities</p>
        </div>
        
        {/* City Selector */}
        <div className="city-selector">
          <label>Select City: </label>
          <select 
            value={selectedCity} 
            onChange={(e) => handleCityChange(e.target.value)}
            disabled={loading}
          >
            {cities.map(city => (
              <option key={city} value={city}>{city}</option>
            ))}
          </select>
        </div>
      </header>

      {/* Error Message */}
      {error && (
        <div className="error-banner">
          <strong>Error:</strong> {error}
        </div>
      )}

      {/* Loading Indicator */}
      {loading && (
        <div className="loading-banner">
          Loading data...
        </div>
      )}

      {/* Main Content */}
      <div className="main-content">
        {/* Left Panel: Map */}
        <div className="left-panel">
          <MapDashboard 
            city={selectedCity}
            cityData={cityData}
            scenarioResults={scenarioResults}
          />
        </div>

        {/* Right Panel: Controls and Charts */}
        <div className="right-panel">
          {/* Scenario Controls */}
          <ScenarioSelector 
            onRunScenario={handleRunScenario}
            loading={loading}
          />

          {/* Charts and Metrics */}
          {cityData && (
            <ChartsPanel 
              cityData={cityData}
              scenarioResults={scenarioResults}
            />
          )}
        </div>
      </div>

      {/* Footer */}
      <footer className="app-footer">
        <p>
          Aligned with UN SDGs: 
          <span className="sdg-badge">SDG 3</span>
          <span className="sdg-badge">SDG 7</span>
          <span className="sdg-badge">SDG 11</span>
          <span className="sdg-badge">SDG 13</span>
        </p>
        <p className="footer-note">
          Demo version - Using mock data for demonstration purposes
        </p>
      </footer>
    </div>
  );
}

export default App;
