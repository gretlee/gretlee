/**
 * Scenario Selector Component
 * Form for inputting what-if scenario parameters
 */

import React, { useState, useEffect } from 'react';
import { getScenarioTemplates } from '../services/api';

const ScenarioSelector = ({ onRunScenario, loading }) => {
  const [solarPercentage, setSolarPercentage] = useState(30);
  const [greenSpaces, setGreenSpaces] = useState(20);
  const [electricTransport, setElectricTransport] = useState(40);
  const [treePlanting, setTreePlanting] = useState(100000);
  const [templates, setTemplates] = useState({});

  useEffect(() => {
    // Load scenario templates
    loadTemplates();
  }, []);

  const loadTemplates = async () => {
    try {
      const data = await getScenarioTemplates();
      setTemplates(data);
    } catch (err) {
      console.error('Failed to load templates:', err);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    const scenarioParams = {
      solar_percentage: parseFloat(solarPercentage),
      green_spaces_increase: parseFloat(greenSpaces),
      electric_transport_percentage: parseFloat(electricTransport),
      tree_planting: parseInt(treePlanting)
    };

    onRunScenario(scenarioParams);
  };

  const handleTemplateSelect = (templateName) => {
    const template = templates[templateName];
    if (template) {
      setSolarPercentage(template.solar_percentage);
      setGreenSpaces(template.green_spaces_increase);
      setElectricTransport(template.electric_transport_percentage);
      setTreePlanting(template.tree_planting);
    }
  };

  const handleReset = () => {
    setSolarPercentage(0);
    setGreenSpaces(0);
    setElectricTransport(0);
    setTreePlanting(0);
  };

  return (
    <div className="scenario-selector">
      <h2>🎯 Scenario Builder</h2>
      <p className="section-description">
        Adjust parameters to simulate sustainability interventions
      </p>

      {/* Template Buttons */}
      <div className="template-buttons">
        <h4>Quick Templates:</h4>
        <div className="button-group">
          {Object.keys(templates).map((key) => (
            <button
              key={key}
              onClick={() => handleTemplateSelect(key)}
              className="template-btn"
              disabled={loading}
            >
              {templates[key].name}
            </button>
          ))}
        </div>
      </div>

      {/* Scenario Form */}
      <form onSubmit={handleSubmit} className="scenario-form">
        {/* Solar Energy */}
        <div className="form-group">
          <label>
            ☀️ Solar Energy Adoption: {solarPercentage}%
          </label>
          <input
            type="range"
            min="0"
            max="100"
            value={solarPercentage}
            onChange={(e) => setSolarPercentage(e.target.value)}
            disabled={loading}
          />
          <small>Percentage of energy from solar sources</small>
        </div>

        {/* Green Spaces */}
        <div className="form-group">
          <label>
            🌳 Green Spaces Increase: {greenSpaces}%
          </label>
          <input
            type="range"
            min="0"
            max="100"
            value={greenSpaces}
            onChange={(e) => setGreenSpaces(e.target.value)}
            disabled={loading}
          />
          <small>Additional green space as % of city area</small>
        </div>

        {/* Electric Transport */}
        <div className="form-group">
          <label>
            🚌 Electric Transport: {electricTransport}%
          </label>
          <input
            type="range"
            min="0"
            max="100"
            value={electricTransport}
            onChange={(e) => setElectricTransport(e.target.value)}
            disabled={loading}
          />
          <small>Percentage of electric vehicles in fleet</small>
        </div>

        {/* Tree Planting */}
        <div className="form-group">
          <label>
            🌲 Tree Planting Program
          </label>
          <input
            type="number"
            min="0"
            max="1000000"
            step="10000"
            value={treePlanting}
            onChange={(e) => setTreePlanting(e.target.value)}
            disabled={loading}
          />
          <small>Number of trees to plant</small>
        </div>

        {/* Action Buttons */}
        <div className="form-actions">
          <button
            type="submit"
            className="btn-primary"
            disabled={loading}
          >
            {loading ? 'Running Simulation...' : '🚀 Run Scenario'}
          </button>
          <button
            type="button"
            onClick={handleReset}
            className="btn-secondary"
            disabled={loading}
          >
            Reset
          </button>
        </div>
      </form>

      {/* Info Box */}
      <div className="info-box">
        <h4>💡 How It Works</h4>
        <p>
          Adjust the sliders to simulate different sustainability interventions.
          The AI models will predict the impact on air quality, energy demand,
          and carbon emissions.
        </p>
      </div>
    </div>
  );
};

export default ScenarioSelector;
