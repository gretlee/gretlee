import React, { useEffect, useState, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline, useMapEvents } from 'react-leaflet';
import L from 'leaflet';
import { useTranslation } from 'react-i18next';
import 'leaflet/dist/leaflet.css';
import './MapView.css';

// Fix for default marker icons in React-Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

// Custom marker icons
const redIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

const blueIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

const greenIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

// Component to handle map clicks
function MapClickHandler({ onMapClick }) {
  useMapEvents({
    click: (e) => {
      onMapClick(e.latlng);
    },
  });
  return null;
}

const MapView = ({ onLocationSelect, userRole, socket }) => {
  const { t } = useTranslation();
  const [requests, setRequests] = useState([]);
  const [centers, setCenters] = useState([]);
  const [allocations, setAllocations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedLocation, setSelectedLocation] = useState(null);

  // Fetch initial data
  useEffect(() => {
    fetchRequests();
    fetchCenters();
    fetchAllocations();
  }, []);

  // WebSocket for real-time updates
  useEffect(() => {
    if (socket) {
      socket.on('new_report', (data) => {
        console.log('New report received:', data);
        fetchRequests();
      });

      socket.on('allocations_updated', (data) => {
        console.log('Allocations updated:', data);
        fetchRequests();
        fetchAllocations();
        fetchCenters();
      });

      return () => {
        socket.off('new_report');
        socket.off('allocations_updated');
      };
    }
  }, [socket]);

  const fetchRequests = async () => {
    try {
      const response = await fetch('http://localhost:5000/reports');
      const data = await response.json();
      if (data.success) {
        setRequests(data.reports);
      }
    } catch (error) {
      console.error('Error fetching requests:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchCenters = async () => {
    try {
      const response = await fetch('http://localhost:5000/centers');
      const data = await response.json();
      if (data.success) {
        setCenters(data.centers);
      }
    } catch (error) {
      console.error('Error fetching centers:', error);
    }
  };

  const fetchAllocations = async () => {
    try {
      const response = await fetch('http://localhost:5000/allocations');
      const data = await response.json();
      if (data.success) {
        setAllocations(data.allocations);
      }
    } catch (error) {
      console.error('Error fetching allocations:', error);
    }
  };

  const handleMapClick = (latlng) => {
    setSelectedLocation(latlng);
    if (onLocationSelect) {
      onLocationSelect(latlng);
    }
  };

  const handleOptimize = async () => {
    if (userRole !== 'admin') {
      alert(t('map.adminOnly'));
      return;
    }

    try {
      const response = await fetch('http://localhost:5000/optimize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-User-Role': userRole
        }
      });

      const data = await response.json();
      if (data.success) {
        alert(t('map.optimizeSuccess', { count: data.allocations.length }));
        fetchRequests();
        fetchAllocations();
        fetchCenters();
      } else {
        alert(t('map.optimizeError', { error: data.error }));
      }
    } catch (error) {
      alert(t('map.optimizeError', { error: error.message }));
    }
  };

  // Create polylines for allocations
  const allocationLines = allocations.map(allocation => {
    const request = requests.find(r => r.request_id === allocation.request_id);
    const center = centers.find(c => c.center_id === allocation.center_id);

    if (request && center) {
      return {
        id: allocation.request_id,
        positions: [
          [request.lat, request.lon],
          [center.lat, center.lon]
        ],
        color: 'green'
      };
    }
    return null;
  }).filter(Boolean);

  const center = [33.6844, 73.0479]; // Default center (Islamabad)

  if (loading) {
    return <div className="map-loading">{t('map.loading')}</div>;
  }

  return (
    <div className="map-view">
      <div className="map-controls">
        <div className="map-legend">
          <h3>{t('map.legend')}</h3>
          <div className="legend-item">
            <span className="legend-marker red"></span>
            <span>{t('map.requests')}</span>
          </div>
          <div className="legend-item">
            <span className="legend-marker blue"></span>
            <span>{t('map.centers')}</span>
          </div>
          <div className="legend-item">
            <span className="legend-marker green"></span>
            <span>{t('map.allocated')}</span>
          </div>
          <div className="legend-line">
            <span style={{ borderTop: '2px solid green', width: '20px', display: 'inline-block' }}></span>
            <span>{t('map.allocationRoutes')}</span>
          </div>
        </div>

        {userRole === 'admin' && (
          <button onClick={handleOptimize} className="optimize-button">
            {t('map.optimize')}
          </button>
        )}

        <div className="map-stats">
          <h3>{t('map.statistics')}</h3>
          <p>{t('map.totalRequests')}: {requests.length}</p>
          <p>{t('map.pendingRequests')}: {requests.filter(r => r.status === 'pending').length}</p>
          <p>{t('map.allocatedRequests')}: {requests.filter(r => r.status === 'allocated').length}</p>
          <p>{t('map.reliefCenters')}: {centers.length}</p>
        </div>
      </div>

      <MapContainer 
        center={center} 
        zoom={7} 
        style={{ height: '600px', width: '100%' }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        <MapClickHandler onMapClick={handleMapClick} />

        {/* Render requests as red markers */}
        {requests.map(request => (
          <Marker
            key={request.request_id}
            position={[request.lat, request.lon]}
            icon={request.status === 'allocated' ? greenIcon : redIcon}
          >
            <Popup>
              <div className="popup-content">
                <h4>{t('map.request')} {request.request_id}</h4>
                <p><strong>{t('map.people')}:</strong> {request.people}</p>
                <p><strong>{t('map.needType')}:</strong> {request.need_type}</p>
                <p><strong>{t('map.urgency')}:</strong> {request.urgency}</p>
                <p><strong>{t('map.status')}:</strong> {request.status}</p>
                {request.allocated_center_id && (
                  <>
                    <p><strong>{t('map.allocatedTo')}:</strong> {request.allocated_center_id}</p>
                    <p><strong>{t('map.resourcesSent')}:</strong> {request.resources_sent}</p>
                    <p><strong>{t('map.distance')}:</strong> {request.distance} km</p>
                  </>
                )}
              </div>
            </Popup>
          </Marker>
        ))}

        {/* Render centers as blue markers */}
        {centers.map(center => (
          <Marker
            key={center.center_id}
            position={[center.lat, center.lon]}
            icon={blueIcon}
          >
            <Popup>
              <div className="popup-content">
                <h4>{t('map.center')} {center.center_id}</h4>
                <p><strong>{t('map.water')}:</strong> {center.water_stock}</p>
                <p><strong>{t('map.food')}:</strong> {center.food_stock}</p>
                <p><strong>{t('map.tents')}:</strong> {center.tent_stock}</p>
              </div>
            </Popup>
          </Marker>
        ))}

        {/* Render allocation routes as polylines */}
        {allocationLines.map(line => (
          <Polyline
            key={line.id}
            positions={line.positions}
            color={line.color}
            weight={2}
            opacity={0.7}
          />
        ))}

        {/* Selected location marker */}
        {selectedLocation && (
          <Marker position={[selectedLocation.lat, selectedLocation.lng]}>
            <Popup>
              <div className="popup-content">
                <h4>{t('map.selectedLocation')}</h4>
                <p>{t('map.lat')}: {selectedLocation.lat.toFixed(4)}</p>
                <p>{t('map.lon')}: {selectedLocation.lng.toFixed(4)}</p>
              </div>
            </Popup>
          </Marker>
        )}
      </MapContainer>
    </div>
  );
};

export default MapView;
