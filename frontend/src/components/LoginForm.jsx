import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import './LoginForm.css';

const LoginForm = ({ onLogin }) => {
  const { t } = useTranslation();
  const [username, setUsername] = useState('');
  const [role, setRole] = useState('relief_worker');

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (username.trim()) {
      onLogin({ username, role });
    } else {
      alert(t('login.enterUsername'));
    }
  };

  return (
    <div className="login-container">
      <div className="login-form">
        <h2>{t('login.title')}</h2>
        <p className="login-subtitle">{t('login.subtitle')}</p>
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">{t('login.username')}</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder={t('login.usernamePlaceholder')}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="role">{t('login.role')}</label>
            <select
              id="role"
              value={role}
              onChange={(e) => setRole(e.target.value)}
            >
              <option value="relief_worker">{t('login.reliefWorker')}</option>
              <option value="admin">{t('login.admin')}</option>
            </select>
          </div>

          <button type="submit" className="login-button">
            {t('login.loginButton')}
          </button>
        </form>

        <div className="role-info">
          <h3>{t('login.roleInfo')}</h3>
          <div className="role-description">
            <strong>{t('login.reliefWorker')}:</strong> {t('login.reliefWorkerDesc')}
          </div>
          <div className="role-description">
            <strong>{t('login.admin')}:</strong> {t('login.adminDesc')}
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginForm;
