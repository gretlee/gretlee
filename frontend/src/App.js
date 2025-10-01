import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import io from 'socket.io-client';
import LoginForm from './components/LoginForm';
import ReportForm from './components/ReportForm';
import MapView from './components/MapView';
import './App.css';
import './i18n';

function App() {
  const { t, i18n } = useTranslation();
  const [user, setUser] = useState(null);
  const [selectedLocation, setSelectedLocation] = useState(null);
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    // Initialize WebSocket connection
    const newSocket = io('http://localhost:5000');
    
    newSocket.on('connect', () => {
      console.log('Connected to WebSocket server');
    });

    newSocket.on('disconnect', () => {
      console.log('Disconnected from WebSocket server');
    });

    setSocket(newSocket);

    return () => {
      newSocket.close();
    };
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    setUser(null);
    setSelectedLocation(null);
  };

  const handleLocationSelect = (location) => {
    setSelectedLocation(location);
  };

  const handleReportSubmit = (data) => {
    // Reset selected location after successful submit
    setSelectedLocation(null);
  };

  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng);
  };

  if (!user) {
    return <LoginForm onLogin={handleLogin} />;
  }

  return (
    <div className="App">
      <header className="app-header">
        <div className="header-content">
          <h1>{t('nav.home')} - Disaster Relief Resource Allocator</h1>
          <div className="header-controls">
            <div className="user-info">
              <span className="username">{user.username}</span>
              <span className="role-badge">{user.role}</span>
            </div>
            <div className="language-selector">
              <button 
                onClick={() => changeLanguage('en')}
                className={i18n.language === 'en' ? 'active' : ''}
              >
                English
              </button>
              <button 
                onClick={() => changeLanguage('ur')}
                className={i18n.language === 'ur' ? 'active' : ''}
              >
                اردو
              </button>
            </div>
            <button onClick={handleLogout} className="logout-button">
              {t('nav.logout')}
            </button>
          </div>
        </div>
      </header>

      <main className="app-main">
        <div className="content-grid">
          <div className="sidebar">
            {(user.role === 'relief_worker' || user.role === 'admin') && (
              <ReportForm 
                selectedLocation={selectedLocation}
                onSubmit={handleReportSubmit}
                userRole={user.role}
              />
            )}
          </div>

          <div className="map-section">
            <MapView 
              onLocationSelect={handleLocationSelect}
              userRole={user.role}
              socket={socket}
            />
          </div>
        </div>
      </main>

      <footer className="app-footer">
        <p>© 2025 Disaster Relief Resource Allocator - Emergency Response System</p>
      </footer>
    </div>
  );
}

export default App;
