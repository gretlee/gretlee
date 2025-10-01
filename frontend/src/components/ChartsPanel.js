/**
 * Charts Panel Component
 * Displays Plotly charts for AQI, energy, and other metrics
 */

import React from 'react';
import Plot from 'react-plotly.js';

const ChartsPanel = ({ cityData, scenarioResults }) => {
  // Extract AQI data
  const aqiData = cityData?.aqi?.predictions || null;
  
  // Extract energy data
  const energyData = cityData?.energy || null;
  
  // Extract flood risk data
  const floodRisk = cityData?.flood_risk || null;

  // AQI Forecast Chart
  const renderAQIChart = () => {
    if (!aqiData || !aqiData.dates) return null;

    return (
      <div className="chart-container">
        <h3>📊 AQI Forecast (7 Days)</h3>
        <Plot
          data={[
            {
              x: aqiData.dates,
              y: aqiData.aqi,
              type: 'scatter',
              mode: 'lines+markers',
              marker: { color: '#FF5722', size: 8 },
              line: { width: 3 },
              name: 'AQI'
            }
          ]}
          layout={{
            autosize: true,
            margin: { l: 50, r: 30, t: 30, b: 50 },
            xaxis: { title: 'Date' },
            yaxis: { title: 'AQI Value' },
            hovermode: 'closest',
            showlegend: false
          }}
          style={{ width: '100%', height: '300px' }}
          config={{ responsive: true }}
        />
        <div className="chart-legend">
          <span className="legend-note">
            Current trend: {aqiData.category?.[0] || 'Moderate'}
          </span>
        </div>
      </div>
    );
  };

  // Pollutants Chart
  const renderPollutantsChart = () => {
    if (!aqiData || !aqiData.dates) return null;

    return (
      <div className="chart-container">
        <h3>🌫️ Pollutant Levels</h3>
        <Plot
          data={[
            {
              x: aqiData.dates,
              y: aqiData.pm25,
              type: 'scatter',
              mode: 'lines',
              name: 'PM2.5',
              line: { color: '#E91E63' }
            },
            {
              x: aqiData.dates,
              y: aqiData.pm10,
              type: 'scatter',
              mode: 'lines',
              name: 'PM10',
              line: { color: '#9C27B0' }
            },
            {
              x: aqiData.dates,
              y: aqiData.no2,
              type: 'scatter',
              mode: 'lines',
              name: 'NO2',
              line: { color: '#2196F3' }
            },
            {
              x: aqiData.dates,
              y: aqiData.so2,
              type: 'scatter',
              mode: 'lines',
              name: 'SO2',
              line: { color: '#4CAF50' }
            }
          ]}
          layout={{
            autosize: true,
            margin: { l: 50, r: 30, t: 30, b: 50 },
            xaxis: { title: 'Date' },
            yaxis: { title: 'Concentration (µg/m³)' },
            hovermode: 'closest',
            showlegend: true,
            legend: { x: 0, y: 1 }
          }}
          style={{ width: '100%', height: '300px' }}
          config={{ responsive: true }}
        />
      </div>
    );
  };

  // Energy Metrics
  const renderEnergyMetrics = () => {
    if (!energyData) return null;

    const baseline = energyData.demand_kwh || energyData.baseline_demand_kwh || 0;
    const adjusted = energyData.adjusted_demand_kwh || baseline;

    return (
      <div className="metrics-container">
        <h3>⚡ Energy Demand</h3>
        <div className="metrics-grid">
          <div className="metric-card">
            <div className="metric-value">
              {(baseline / 1000000).toFixed(2)}
            </div>
            <div className="metric-label">Baseline (GWh)</div>
          </div>
          
          {scenarioResults && (
            <>
              <div className="metric-card highlight">
                <div className="metric-value">
                  {(adjusted / 1000000).toFixed(2)}
                </div>
                <div className="metric-label">Scenario (GWh)</div>
              </div>
              
              <div className="metric-card">
                <div className="metric-value" style={{ 
                  color: energyData.change_percentage < 0 ? '#4CAF50' : '#F44336' 
                }}>
                  {energyData.change_percentage?.toFixed(1) || '0'}%
                </div>
                <div className="metric-label">Change</div>
              </div>
            </>
          )}
        </div>
      </div>
    );
  };

  // Flood Risk Distribution
  const renderFloodRiskChart = () => {
    if (!floodRisk || !floodRisk.risk_distribution) return null;

    const distribution = floodRisk.risk_distribution;

    return (
      <div className="chart-container">
        <h3>🌊 Flood Risk Distribution</h3>
        <Plot
          data={[
            {
              values: [distribution.Low, distribution.Medium, distribution.High],
              labels: ['Low Risk', 'Medium Risk', 'High Risk'],
              type: 'pie',
              marker: {
                colors: ['#4CAF50', '#FF9800', '#F44336']
              },
              textinfo: 'label+percent',
              hoverinfo: 'label+value'
            }
          ]}
          layout={{
            autosize: true,
            margin: { l: 20, r: 20, t: 20, b: 20 },
            showlegend: true,
            legend: { x: 0, y: 1 }
          }}
          style={{ width: '100%', height: '300px' }}
          config={{ responsive: true }}
        />
      </div>
    );
  };

  // Scenario Impact Charts
  const renderScenarioImpact = () => {
    if (!scenarioResults || !scenarioResults.impacts) return null;

    const impacts = scenarioResults.impacts;

    return (
      <div className="scenario-impact">
        <h3>🎯 Scenario Impact Analysis</h3>
        
        {/* Air Quality Impact */}
        {impacts.air_quality && (
          <div className="impact-card">
            <h4>Air Quality</h4>
            <div className="impact-comparison">
              <div>
                <span className="label">Baseline AQI:</span>
                <span className="value">{impacts.air_quality.baseline_aqi}</span>
              </div>
              <div>
                <span className="label">Projected AQI:</span>
                <span className="value improved">{impacts.air_quality.projected_aqi}</span>
              </div>
              <div>
                <span className="label">Improvement:</span>
                <span className="value positive">
                  -{impacts.air_quality.improvement} ({impacts.air_quality.improvement_percentage}%)
                </span>
              </div>
            </div>
          </div>
        )}

        {/* Carbon Emissions Impact */}
        {impacts.carbon_emissions && (
          <div className="impact-card">
            <h4>Carbon Emissions</h4>
            <div className="impact-comparison">
              <div>
                <span className="label">Baseline:</span>
                <span className="value">{impacts.carbon_emissions.baseline_tons_co2.toLocaleString()} tons CO₂</span>
              </div>
              <div>
                <span className="label">Projected:</span>
                <span className="value improved">{impacts.carbon_emissions.projected_tons_co2.toLocaleString()} tons CO₂</span>
              </div>
              <div>
                <span className="label">Reduction:</span>
                <span className="value positive">
                  -{impacts.carbon_emissions.reduction_tons.toLocaleString()} tons 
                  ({impacts.carbon_emissions.reduction_percentage}%)
                </span>
              </div>
            </div>
          </div>
        )}

        {/* SDG Alignment */}
        {scenarioResults.sdg_alignment && (
          <div className="sdg-scores">
            <h4>UN SDG Alignment</h4>
            <div className="sdg-grid">
              {Object.entries(scenarioResults.sdg_alignment.individual_scores).map(([sdg, score]) => (
                <div key={sdg} className="sdg-score-card">
                  <div className="sdg-name">{sdg.replace('_', ' ')}</div>
                  <div className="sdg-score">{score.toFixed(0)}/100</div>
                  <div className="score-bar">
                    <div 
                      className="score-fill" 
                      style={{ width: `${score}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
            <div className="overall-sdg">
              <strong>Overall SDG Score:</strong> 
              <span className="score">{scenarioResults.sdg_alignment.overall_score}/100</span>
              <span className="rating">({scenarioResults.sdg_alignment.rating})</span>
            </div>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="charts-panel">
      <h2>📈 Analytics Dashboard</h2>
      
      {renderAQIChart()}
      {renderPollutantsChart()}
      {renderEnergyMetrics()}
      {renderFloodRiskChart()}
      {renderScenarioImpact()}

      {!cityData && (
        <div className="no-data">
          <p>Loading city data...</p>
        </div>
      )}
    </div>
  );
};

export default ChartsPanel;
