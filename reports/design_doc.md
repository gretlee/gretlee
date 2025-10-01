# Urban Sustainability Simulator - Technical Design Document

## 1. Project Overview

### 1.1 Mission Statement
To provide AI-driven sustainability forecasting and scenario planning for urban Pakistani cities, enabling evidence-based policy decisions aligned with UN Sustainable Development Goals.

### 1.2 Target Users
- Urban planners and city administrators
- Environmental policy makers
- Academic researchers
- NGOs focused on sustainability
- General public interested in urban development

### 1.3 Supported Cities
- Lahore (Punjab)
- Karachi (Sindh)
- Faisalabad (Punjab)
- Sargodha (Punjab)

---

## 2. System Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (React)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Map Dashboard│  │   Scenario   │  │    Charts    │      │
│  │  (Leaflet)   │  │   Selector   │  │   (Plotly)   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└───────────────────────────┬─────────────────────────────────┘
                            │ REST API (HTTP/JSON)
┌───────────────────────────▼─────────────────────────────────┐
│                      Backend (Flask)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Forecast   │  │  Simulation  │  │ Health Check │      │
│  │    Routes    │  │    Routes    │  │    Routes    │      │
│  └──────┬───────┘  └──────┬───────┘  └──────────────┘      │
│         │                  │                                 │
│  ┌──────▼──────────────────▼──────┐                         │
│  │        Services Layer           │                         │
│  │  • Model Inference              │                         │
│  │  • Data Loader                  │                         │
│  │  • Simulation Engine            │                         │
│  └─────────────┬───────────────────┘                         │
└────────────────┼─────────────────────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────────────────────┐
│                    ML Models Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  AQI LSTM    │  │   Energy     │  │  Flood Risk  │       │
│  │   Model      │  │  Regression  │  │ Classifier   │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└───────────────────────────────────────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────────────────────┐
│                      Data Layer                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  Raw Data    │  │  Processed   │  │   Trained    │       │
│  │   (CSV)      │  │    Data      │  │   Models     │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└───────────────────────────────────────────────────────────────┘
```

### 2.2 Technology Stack

#### Frontend
- **Framework**: React 18.2
- **State Management**: React Hooks (useState, useEffect)
- **HTTP Client**: Axios
- **Mapping**: Leaflet.js + React-Leaflet
- **Charting**: Plotly.js
- **Styling**: Custom CSS with responsive design

#### Backend
- **Framework**: Flask 3.0
- **API Design**: RESTful architecture
- **CORS**: Flask-CORS for cross-origin requests
- **Server**: Gunicorn for production

#### Machine Learning
- **Deep Learning**: TensorFlow/Keras 2.15
- **Classical ML**: scikit-learn 1.3
- **Data Processing**: Pandas, NumPy
- **Geospatial**: GeoPandas

#### Deployment
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **Frontend Hosting**: Vercel
- **Backend Hosting**: Render
- **Version Control**: Git

---

## 3. Machine Learning Models

### 3.1 Air Quality Index (AQI) Forecasting

**Model Type**: LSTM (Long Short-Term Memory) Neural Network

**Architecture**:
```
Input Layer (7 timesteps, 4 features)
    ↓
LSTM Layer (64 units, return sequences)
    ↓
Dropout (20%)
    ↓
LSTM Layer (32 units)
    ↓
Dropout (20%)
    ↓
Dense Layer (16 units, ReLU)
    ↓
Output Layer (4 units) → [PM2.5, PM10, NO2, SO2]
```

**Features**:
- PM2.5 concentration
- PM10 concentration
- NO₂ concentration
- SO₂ concentration

**Sequence Length**: 7 days
**Forecast Horizon**: 1-30 days
**Loss Function**: Mean Squared Error (MSE)
**Optimizer**: Adam

**Training Process**:
1. Load historical AQI data
2. Normalize features using MinMaxScaler (0-1)
3. Create sliding window sequences (7 days → 1 day)
4. Split 80/20 train/test
5. Train for 50 epochs with batch size 32
6. Inverse transform predictions to original scale

### 3.2 Energy Demand Prediction

**Model Type**: Random Forest Regression

**Architecture**:
- Number of estimators: 100
- Max depth: 15
- Min samples split: 5
- Min samples leaf: 2

**Features** (8 total):
- Population
- Temperature (°C)
- Month (1-12)
- Day of week (0-6)
- Is weekend (0/1)
- Industrial zones (count)
- Residential areas (count)
- Commercial areas (count)

**Target**: Energy consumption (kWh)

**Preprocessing**:
- StandardScaler for feature normalization
- Temporal feature engineering from dates
- Handle missing values with defaults

**Alternative Model**: Gradient Boosting Regressor
- Learning rate: 0.1
- Max depth: 5
- Similar performance, faster inference

### 3.3 Flood Risk Assessment

**Model Type**: Random Forest Classifier

**Architecture**:
- Number of estimators: 150
- Max depth: 10
- Class weights: Balanced
- Classes: 3 (Low, Medium, High)

**Features** (7 total):
- Elevation (meters)
- Distance to water bodies (km)
- Annual rainfall (mm)
- Drainage quality (0-10 scale)
- Soil permeability (0-10 scale)
- Urbanization level (0-10 scale)
- Slope percentage

**Target**: Risk level (Low/Medium/High)

**Evaluation Metrics**:
- Accuracy
- Precision, Recall, F1-score per class
- Confusion matrix

---

## 4. API Design

### 4.1 Endpoint Structure

#### Base URL
- Development: `http://localhost:5000/api`
- Production: `https://your-backend.onrender.com/api`

#### Forecast Endpoints

**GET /api/forecast/aqi**
```json
Query Parameters:
  - city: string (required)
  - days: integer (1-30, default: 7)

Response:
{
  "status": "success",
  "city": "Lahore",
  "forecast_days": 7,
  "data": {
    "dates": ["2025-10-02", "2025-10-03", ...],
    "predictions": {
      "pm25": [75.2, 73.8, ...],
      "pm10": [120.5, 118.2, ...],
      "no2": [44.3, 43.1, ...],
      "so2": [24.7, 25.1, ...],
      "aqi": [150, 148, ...],
      "category": ["Unhealthy", "Unhealthy", ...]
    }
  }
}
```

**GET /api/forecast/energy**
```json
Query Parameters:
  - city: string (required)

Response:
{
  "status": "success",
  "city": "Lahore",
  "data": {
    "demand_kwh": 5563142500,
    "demand_mwh": 5563142.5,
    "per_capita_kwh": 500.12
  }
}
```

**GET /api/forecast/flood-risk**
```json
Query Parameters:
  - city: string (required)
  - zones: integer (1-100, default: 20)

Response:
{
  "status": "success",
  "city": "Lahore",
  "data": {
    "total_zones": 20,
    "risk_distribution": {
      "Low": 12,
      "Medium": 6,
      "High": 2
    },
    "high_risk_zones": ["Lahore_zone_3", "Lahore_zone_15"],
    "zones": [...]
  }
}
```

#### Simulation Endpoints

**POST /api/simulation/scenario**
```json
Request Body:
{
  "city": "Lahore",
  "solar_percentage": 30,
  "green_spaces_increase": 20,
  "electric_transport_percentage": 40,
  "tree_planting": 100000
}

Response:
{
  "status": "success",
  "data": {
    "city": "Lahore",
    "scenario": {...},
    "impacts": {
      "energy": {...},
      "air_quality": {...},
      "carbon_emissions": {...},
      "green_spaces": {...}
    },
    "sdg_alignment": {...},
    "sustainability_score": {
      "score": 68.5,
      "rating": "Good"
    }
  }
}
```

### 4.2 Error Handling

**Standard Error Response**:
```json
{
  "status": "error",
  "message": "Descriptive error message",
  "code": 400
}
```

**HTTP Status Codes**:
- 200: Success
- 400: Bad Request (invalid parameters)
- 404: Not Found
- 500: Internal Server Error

---

## 5. Data Management

### 5.1 Data Sources

**Current** (Mock Data):
- Synthetically generated time series
- Realistic statistical distributions
- Seasonal patterns included

**Future** (Real Data):
- Pakistan Meteorological Department
- Environmental Protection Agencies
- OpenStreetMap for geospatial data
- City utility companies (energy data)
- Remote sensing (satellite imagery)

### 5.2 Data Schema

**AQI Data** (`data/raw/aqi_data.csv`):
```
date, city, pm25, pm10, no2, so2, co, o3
2024-01-01, Lahore, 89.5, 135.2, 48.3, 26.1, 15.8, 52.3
```

**Energy Data** (`data/raw/energy_data.csv`):
```
date, city, population, temperature, consumption_kwh, industrial_zones, residential_areas, commercial_areas
2024-01-01, Lahore, 11126285, 18.5, 5500000000, 15, 45, 25
```

**Flood Risk Data** (`data/raw/flood_risk_data.csv`):
```
city, zone_id, elevation_m, distance_to_water_km, annual_rainfall_mm, drainage_quality, soil_permeability, urbanization_level, slope_percentage
Lahore, Lahore_zone_1, 215, 3.5, 628, 6, 7, 8, 2.3
```

### 5.3 Data Preprocessing Pipeline

1. **Loading**: Read CSV files with pandas
2. **Cleaning**: Handle missing values, outliers
3. **Transformation**: Normalize/standardize features
4. **Feature Engineering**: Extract temporal features, create sequences
5. **Splitting**: Train/test split (80/20)
6. **Validation**: Check data quality and consistency

---

## 6. Frontend Design

### 6.1 Component Hierarchy

```
App
├── Header
│   ├── Title
│   └── CitySelector
├── MainContent
│   ├── LeftPanel
│   │   └── MapDashboard
│   │       ├── LeafletMap
│   │       ├── FloodRiskLayers
│   │       └── Legend
│   └── RightPanel
│       ├── ScenarioSelector
│       │   ├── TemplateButtons
│       │   ├── ScenarioForm
│       │   └── InfoBox
│       └── ChartsPanel
│           ├── AQIChart
│           ├── PollutantsChart
│           ├── EnergyMetrics
│           ├── FloodRiskChart
│           └── ScenarioImpact
└── Footer
```

### 6.2 State Management

**App-Level State**:
- `selectedCity`: Currently selected city
- `cityData`: Loaded city overview data
- `scenarioResults`: Results from scenario simulation
- `loading`: Loading indicator
- `error`: Error messages

**Component-Level State**:
- Form inputs in ScenarioSelector
- Map zoom/center in MapDashboard
- Chart configurations in ChartsPanel

### 6.3 User Flows

**Flow 1: View City Overview**
1. User selects city from dropdown
2. App fetches city overview data
3. Map updates to city location
4. Charts display forecast data
5. Flood risk zones appear on map

**Flow 2: Run Scenario**
1. User adjusts scenario parameters (sliders)
2. User clicks "Run Scenario" button
3. Frontend sends POST request to backend
4. Backend runs simulation
5. Results displayed in impact cards and charts
6. Map shows sustainability score

**Flow 3: Compare Scenarios**
1. User selects template scenario
2. User runs scenario
3. User modifies parameters
4. User runs second scenario
5. Results compared side-by-side

---

## 7. Deployment Strategy

### 7.1 Docker Deployment

**Benefits**:
- Consistent environment across dev/prod
- Easy dependency management
- Scalable with orchestration tools

**Dockerfile**:
- Multi-stage build (builder + runtime)
- Optimized Python image
- Health checks included

**Docker Compose**:
- Single command deployment (`docker-compose up`)
- Volume mounts for data persistence
- Network isolation

### 7.2 Cloud Deployment

**Frontend (Vercel)**:
- Automatic GitHub integration
- Global CDN for fast loading
- Serverless architecture
- Free tier available

**Backend (Render)**:
- Free tier with 750 hours/month
- Automatic HTTPS
- Health check monitoring
- Auto-deploy on git push

### 7.3 CI/CD Pipeline (Future)

```
GitHub Push
    ↓
Run Tests (pytest, jest)
    ↓
Build Docker Image
    ↓
Push to Registry
    ↓
Deploy to Production
    ↓
Health Check
```

---

## 8. Performance Optimization

### 8.1 Backend Optimization

- **Model Caching**: Load models once at startup
- **Response Compression**: Gzip for large JSON responses
- **Request Throttling**: Rate limiting to prevent abuse
- **Async Processing**: For long-running simulations

### 8.2 Frontend Optimization

- **Code Splitting**: Load components on demand
- **Lazy Loading**: Defer non-critical resources
- **Memoization**: Cache expensive computations
- **Image Optimization**: Compress assets

### 8.3 Database Optimization (Future)

- **Indexing**: On frequently queried columns
- **Caching**: Redis for hot data
- **Query Optimization**: Efficient SQL queries
- **Connection Pooling**: Reuse database connections

---

## 9. Security Considerations

### 9.1 API Security

- **CORS**: Restricted to known origins
- **Input Validation**: Sanitize all user inputs
- **Rate Limiting**: Prevent DDoS attacks
- **Authentication** (Future): API keys for production

### 9.2 Data Security

- **No PII Collection**: Anonymous usage
- **Secure Storage**: Encrypted at rest (future)
- **Secure Transmission**: HTTPS only
- **Access Control**: Role-based permissions (future)

---

## 10. Testing Strategy

### 10.1 Backend Tests

**Unit Tests**:
- Test each ML model prediction function
- Test data loading and preprocessing
- Test API route handlers

**Integration Tests**:
- Test full API request/response cycle
- Test model inference pipeline
- Test simulation engine

**Test Coverage Target**: 80%+

### 10.2 Frontend Tests

**Component Tests**:
- Test each React component renders
- Test user interactions (clicks, inputs)
- Test API integration

**E2E Tests** (Future):
- Test complete user flows
- Test cross-browser compatibility

---

## 11. Future Enhancements

### 11.1 Short-term (0-6 months)

1. **Real Data Integration**: Replace mock data with actual datasets
2. **User Accounts**: Save scenarios and comparisons
3. **Export Functionality**: Download reports as PDF
4. **Mobile App**: React Native version

### 11.2 Medium-term (6-12 months)

1. **More Cities**: Expand to 10+ Pakistani cities
2. **Advanced Models**: Incorporate weather forecasting
3. **Real-time Updates**: WebSocket for live data
4. **Collaboration Tools**: Share scenarios with teams

### 11.3 Long-term (12+ months)

1. **International Expansion**: Adapt for cities worldwide
2. **AI Recommendations**: Automatic scenario optimization
3. **Policy Integration**: Direct API for government systems
4. **Satellite Integration**: Real-time remote sensing data

---

## 12. Maintenance & Support

### 12.1 Monitoring

- **Uptime Monitoring**: Pingdom or similar
- **Error Tracking**: Sentry for error reporting
- **Analytics**: Google Analytics for usage patterns
- **Performance Monitoring**: Application performance metrics

### 12.2 Documentation

- **API Documentation**: Swagger/OpenAPI specification
- **User Guide**: Tutorial videos and written guides
- **Developer Docs**: Contributing guidelines
- **Changelog**: Track version updates

---

**Document Version**: 1.0  
**Last Updated**: October 2025  
**Maintained By**: Development Team
