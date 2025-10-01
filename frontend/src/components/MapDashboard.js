/**
 * Map Dashboard Component
 * Interactive map using Leaflet showing city boundaries and risk zones
 */

import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

// Fix for default marker icons in React-Leaflet
import L from 'leaflet';
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41]
});

L.Marker.prototype.options.icon = DefaultIcon;

const MapDashboard = ({ city, cityData, scenarioResults }) => {
  // City coordinates
  const cityCoordinates = {
    'Lahore': [31.5497, 74.3436],
    'Karachi': [24.8607, 67.0011],
    'Faisalabad': [31.4504, 73.1350],
    'Sargodha': [32.0836, 72.6711]
  };

  const [center, setCenter] = useState(cityCoordinates[city] || [31.5497, 74.3436]);
  const [floodZones, setFloodZones] = useState([]);

  useEffect(() => {
    setCenter(cityCoordinates[city] || [31.5497, 74.3436]);
    
    // Generate mock flood risk zones
    if (cityData && cityData.flood_risk && cityData.flood_risk.zones) {
      const zones = cityData.flood_risk.zones.slice(0, 10).map((zone, idx) => {
        // Generate random positions around city center
        const lat = center[0] + (Math.random() - 0.5) * 0.2;
        const lng = center[1] + (Math.random() - 0.5) * 0.2;
        
        return {
          id: zone.zone_id,
          position: [lat, lng],
          risk: zone.risk_level,
          confidence: zone.confidence
        };
      });
      setFloodZones(zones);
    }
  }, [city, cityData]);

  const getRiskColor = (risk) => {
    switch (risk) {
      case 'Low': return '#4CAF50';
      case 'Medium': return '#FF9800';
      case 'High': return '#F44336';
      default: return '#9E9E9E';
    }
  };

  const getRiskRadius = (risk) => {
    switch (risk) {
      case 'Low': return 1000;
      case 'Medium': return 1500;
      case 'High': return 2000;
      default: return 1000;
    }
  };

  return (
    <div className="map-dashboard">
      <div className="map-header">
        <h2>📍 {city} Map View</h2>
        {cityData && cityData.metadata && (
          <div className="city-stats">
            <span>Population: {cityData.metadata.population.toLocaleString()}</span>
            <span>Area: {cityData.metadata.area_km2} km²</span>
          </div>
        )}
      </div>

      <MapContainer
        center={center}
        zoom={11}
        style={{ height: '500px', width: '100%', borderRadius: '8px' }}
        key={city} // Force re-render on city change
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {/* City Center Marker */}
        <Marker position={center}>
          <Popup>
            <strong>{city} City Center</strong>
            <br />
            Coordinates: {center[0].toFixed(4)}, {center[1].toFixed(4)}
          </Popup>
        </Marker>

        {/* Flood Risk Zones */}
        {floodZones.map((zone) => (
          <Circle
            key={zone.id}
            center={zone.position}
            radius={getRiskRadius(zone.risk)}
            pathOptions={{
              color: getRiskColor(zone.risk),
              fillColor: getRiskColor(zone.risk),
              fillOpacity: 0.3
            }}
          >
            <Popup>
              <strong>{zone.id}</strong>
              <br />
              Risk Level: <strong>{zone.risk}</strong>
              <br />
              Confidence: {(zone.confidence * 100).toFixed(0)}%
            </Popup>
          </Circle>
        ))}
      </MapContainer>

      {/* Legend */}
      <div className="map-legend">
        <h4>Flood Risk Legend</h4>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#4CAF50' }}></span>
          Low Risk
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#FF9800' }}></span>
          Medium Risk
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#F44336' }}></span>
          High Risk
        </div>
      </div>

      {/* Scenario Impact Summary */}
      {scenarioResults && scenarioResults.sustainability_score && (
        <div className="scenario-impact-summary">
          <h3>Scenario Impact</h3>
          <div className="impact-score">
            <div className="score-circle">
              <span className="score-value">{scenarioResults.sustainability_score.score}</span>
              <span className="score-label">Sustainability Score</span>
            </div>
            <div className="score-rating">
              {scenarioResults.sustainability_score.rating}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MapDashboard;
