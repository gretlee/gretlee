import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import './ReportForm.css';

const ReportForm = ({ selectedLocation, onSubmit, userRole }) => {
  const { t } = useTranslation();
  const [formData, setFormData] = useState({
    lat: selectedLocation?.lat || '',
    lon: selectedLocation?.lng || '',
    people: '',
    need_type: 'water',
    urgency: 'medium'
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState(null);

  React.useEffect(() => {
    if (selectedLocation) {
      setFormData(prev => ({
        ...prev,
        lat: selectedLocation.lat,
        lon: selectedLocation.lng
      }));
    }
  }, [selectedLocation]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.lat || !formData.lon) {
      alert(t('report.selectLocation'));
      return;
    }

    setIsSubmitting(true);
    setSubmitStatus(null);

    try {
      const response = await fetch('http://localhost:5000/reports', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-User-Role': userRole
        },
        body: JSON.stringify({
          lat: parseFloat(formData.lat),
          lon: parseFloat(formData.lon),
          people: parseInt(formData.people),
          need_type: formData.need_type,
          urgency: formData.urgency
        })
      });

      const data = await response.json();

      if (data.success) {
        setSubmitStatus({
          type: 'success',
          message: t('report.success', { id: data.request_id })
        });
        
        // Reset form
        setFormData({
          lat: '',
          lon: '',
          people: '',
          need_type: 'water',
          urgency: 'medium'
        });

        // Call parent callback
        if (onSubmit) {
          onSubmit(data);
        }
      } else {
        setSubmitStatus({
          type: 'error',
          message: t('report.error', { error: data.error })
        });
      }
    } catch (error) {
      setSubmitStatus({
        type: 'error',
        message: t('report.networkError')
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="report-form">
      <h2>{t('report.title')}</h2>
      <p className="form-description">{t('report.description')}</p>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="lat">{t('report.latitude')}</label>
          <input
            type="number"
            step="any"
            id="lat"
            name="lat"
            value={formData.lat}
            onChange={handleChange}
            placeholder={t('report.clickMap')}
            required
            readOnly
          />
        </div>

        <div className="form-group">
          <label htmlFor="lon">{t('report.longitude')}</label>
          <input
            type="number"
            step="any"
            id="lon"
            name="lon"
            value={formData.lon}
            onChange={handleChange}
            placeholder={t('report.clickMap')}
            required
            readOnly
          />
        </div>

        <div className="form-group">
          <label htmlFor="people">{t('report.people')}</label>
          <input
            type="number"
            id="people"
            name="people"
            value={formData.people}
            onChange={handleChange}
            placeholder={t('report.peoplePlaceholder')}
            min="1"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="need_type">{t('report.needType')}</label>
          <select
            id="need_type"
            name="need_type"
            value={formData.need_type}
            onChange={handleChange}
            required
          >
            <option value="water">{t('report.water')}</option>
            <option value="food">{t('report.food')}</option>
            <option value="tent">{t('report.tent')}</option>
            <option value="medical">{t('report.medical')}</option>
            <option value="shelter">{t('report.shelter')}</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="urgency">{t('report.urgency')}</label>
          <select
            id="urgency"
            name="urgency"
            value={formData.urgency}
            onChange={handleChange}
            required
          >
            <option value="low">{t('report.low')}</option>
            <option value="medium">{t('report.medium')}</option>
            <option value="high">{t('report.high')}</option>
          </select>
        </div>

        <button 
          type="submit" 
          className="submit-button"
          disabled={isSubmitting || !formData.lat || !formData.lon}
        >
          {isSubmitting ? t('report.submitting') : t('report.submit')}
        </button>
      </form>

      {submitStatus && (
        <div className={`status-message ${submitStatus.type}`}>
          {submitStatus.message}
        </div>
      )}
    </div>
  );
};

export default ReportForm;
