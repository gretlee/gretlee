/**
 * API Service
 * Handles all communication with the backend API
 */

import axios from 'axios';

// Base URL for API (uses proxy in development)
const API_BASE_URL = process.env.REACT_APP_API_URL || '/api';

/**
 * Check API health
 */
export const checkHealth = async () => {
  const response = await axios.get(`${API_BASE_URL}/health`);
  return response.data;
};

/**
 * Get AQI forecast for a city
 * @param {string} city - City name
 * @param {number} days - Number of days to forecast (default: 7)
 */
export const getAQIForecast = async (city, days = 7) => {
  const response = await axios.get(`${API_BASE_URL}/forecast/aqi`, {
    params: { city, days }
  });
  return response.data;
};

/**
 * Get energy demand forecast for a city
 * @param {string} city - City name
 */
export const getEnergyForecast = async (city) => {
  const response = await axios.get(`${API_BASE_URL}/forecast/energy`, {
    params: { city }
  });
  return response.data;
};

/**
 * Get flood risk assessment for a city
 * @param {string} city - City name
 * @param {number} zones - Number of zones to analyze (default: 20)
 */
export const getFloodRisk = async (city, zones = 20) => {
  const response = await axios.get(`${API_BASE_URL}/forecast/flood-risk`, {
    params: { city, zones }
  });
  return response.data;
};

/**
 * Get comprehensive city overview
 * @param {string} city - City name
 */
export const getCityOverview = async (city) => {
  const response = await axios.get(`${API_BASE_URL}/forecast/overview`, {
    params: { city }
  });
  return response.data.data;
};

/**
 * Run a scenario simulation
 * @param {string} city - City name
 * @param {object} scenarioParams - Scenario parameters
 */
export const runScenario = async (city, scenarioParams) => {
  const response = await axios.post(`${API_BASE_URL}/simulation/scenario`, {
    city,
    ...scenarioParams
  });
  return response.data.data;
};

/**
 * Compare multiple scenarios
 * @param {string} city - City name
 * @param {array} scenarios - Array of scenario objects
 */
export const compareScenarios = async (city, scenarios) => {
  const response = await axios.post(`${API_BASE_URL}/simulation/compare`, {
    city,
    scenarios
  });
  return response.data;
};

/**
 * Get predefined scenario templates
 */
export const getScenarioTemplates = async () => {
  const response = await axios.get(`${API_BASE_URL}/simulation/templates`);
  return response.data.templates;
};
