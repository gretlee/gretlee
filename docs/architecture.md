# Disaster Relief Resource Allocator - System Architecture

## Overview

The Disaster Relief Resource Allocator is a full-stack web application designed to optimize emergency resource distribution during disaster events. The system enables relief workers to report disasters, administrators to manage relief centers, and automatically allocates resources using an intelligent algorithm.

## Technology Stack

### Backend
- **Framework**: Flask (Python web framework)
- **ORM**: SQLAlchemy (database abstraction)
- **Real-time Communication**: Flask-SocketIO (WebSocket support)
- **Database**: SQLite (development), PostgreSQL-ready (production)
- **ML/Analytics**: scikit-learn, pandas, numpy

### Frontend
- **Framework**: React 18
- **Mapping**: Leaflet.js with React-Leaflet
- **Real-time**: Socket.io-client
- **Internationalization**: i18next, react-i18next
- **Styling**: CSS3 with custom components

### Data & Analysis
- **Jupyter Notebooks**: Analysis and visualization
- **Visualization**: matplotlib, seaborn, folium

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                          │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Login Form   │  │ Report Form  │  │  Map View    │      │
│  │ (Auth/Role)  │  │ (Submit      │  │ (Leaflet.js) │      │
│  │              │  │  Requests)   │  │              │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │            i18n Translation Layer                     │   │
│  │         (English / Urdu / Other Languages)            │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTP/REST + WebSocket
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                      API LAYER (Flask)                       │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  POST /reports       → Create disaster report                │
│  GET  /reports       → List all reports                      │
│  GET  /centers       → List relief centers                   │
│  POST /centers       → Create center (admin)                 │
│  POST /optimize      → Run allocation algorithm              │
│  GET  /allocations   → Get allocation results                │
│  GET  /predict       → Get demand predictions                │
│                                                               │
│  WebSocket Events:                                           │
│    - new_report         → Broadcast new disaster reports     │
│    - allocations_updated → Notify allocation changes         │
│                                                               │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                     SERVICE LAYER                            │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌────────────────────┐  ┌────────────────────┐            │
│  │ Allocator Service  │  │ Prediction Service │            │
│  │ - Priority-based   │  │ - ML forecasting   │            │
│  │ - Distance calc    │  │ - RandomForest     │            │
│  │ - Stock mgmt       │  │ - 7-day forecast   │            │
│  └────────────────────┘  └────────────────────┘            │
│                                                               │
│  ┌────────────────────┐  ┌────────────────────┐            │
│  │ Notification Svc   │  │ Authentication     │            │
│  │ - SMS (Twilio)     │  │ - Role-based       │            │
│  │ - Email (SMTP)     │  │ - Admin/Worker     │            │
│  └────────────────────┘  └────────────────────┘            │
│                                                               │
│  ┌────────────────────┐                                     │
│  │   Geo Utilities    │                                     │
│  │ - Haversine dist   │                                     │
│  │ - Nearest center   │                                     │
│  └────────────────────┘                                     │
│                                                               │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    DATA LAYER (SQLAlchemy)                   │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │  Centers   │  │  Requests  │  │ Allocations│            │
│  │  Table     │  │  Table     │  │  Table     │            │
│  └────────────┘  └────────────┘  └────────────┘            │
│                                                               │
│  Database: SQLite (dev) / PostgreSQL (prod)                  │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Disaster Report Submission Flow

```
Relief Worker → Report Form → POST /reports → Validate Data
    → Save to Database → Broadcast WebSocket → Update Map
```

### 2. Resource Allocation Flow

```
Admin → Click "Optimize" → POST /optimize
    ↓
Fetch pending requests & centers
    ↓
Run Allocation Algorithm:
  - Sort by urgency (high → medium → low)
  - For each request:
    - Find nearest center with stock
    - Calculate distance (Haversine)
    - Allocate resources
    - Update stock levels
    ↓
Save allocations to database
    ↓
Broadcast WebSocket update
    ↓
Update map with routes & markers
```

### 3. Prediction Flow

```
Admin → View Predictions → GET /predict
    ↓
Load historical data (CSV)
    ↓
Train/Load ML Model:
  - Features: lat, lon, date, need_type, urgency
  - Model: RandomForest Regressor
  - Target: number of people affected
    ↓
Generate 7-day forecast
    ↓
Return predictions as JSON
```

### 4. Real-time Updates Flow

```
Any Event (Report/Allocation)
    ↓
Server emits WebSocket event
    ↓
All connected clients receive event
    ↓
Clients update UI automatically
  - Refresh map markers
  - Update statistics
  - Show notifications
```

## Core Components

### Backend Components

#### 1. **app.py** (Main Application)
- Flask application setup
- Database models (Center, Request, Allocation)
- REST API endpoints
- WebSocket event handlers
- SQLAlchemy ORM integration

#### 2. **services/allocator.py** (Allocation Engine)
- `allocate_resources()`: Main allocation algorithm
  - Priority-based sorting by urgency
  - Nearest-center matching with distance calculation
  - Stock management and deduction
  - Returns allocation results and updated stocks
- `calculate_allocation_metrics()`: Performance evaluation

#### 3. **utils/geo.py** (Geospatial Utilities)
- `haversine()`: Calculate great-circle distance
- `find_nearest_center()`: Find closest relief center

#### 4. **services/prediction.py** (ML Prediction)
- `train_prediction_model()`: Train RandomForest on historical data
- `load_prediction_model()`: Load saved model
- `predict_resource_demand()`: Generate 7-day forecast

#### 5. **services/notifications.py** (Alert System)
- `send_sms_alert()`: SMS via Twilio API
- `send_email_alert()`: Email via SMTP
- `notify_allocation()`: Composite notification handler

#### 6. **auth/roles.py** (Role-Based Access Control)
- Roles: `admin`, `relief_worker`
- Permissions mapping
- Decorators: `@require_permission()`, `@require_role()`

### Frontend Components

#### 1. **LoginForm.jsx**
- User authentication interface
- Role selection (admin/relief_worker)
- Multilingual labels

#### 2. **ReportForm.jsx**
- Disaster report submission
- Map-based location selection
- Need type & urgency dropdowns
- Real-time validation & feedback

#### 3. **MapView.jsx**
- Leaflet.js interactive map
- Red markers: Disaster requests
- Blue markers: Relief centers
- Green markers: Allocated requests
- Polylines: Allocation routes
- WebSocket-powered real-time updates
- Admin-only optimization button

#### 4. **i18n.js**
- Translation definitions (English, Urdu)
- Language switching
- React-i18next integration

### Data Components

#### 1. **centers.csv**
Sample relief centers with stock levels

#### 2. **requests.csv**
Sample disaster requests with coordinates and needs

#### 3. **historical_requests.csv**
Historical data for ML model training (90+ records)

#### 4. **allocation.ipynb**
Jupyter notebook with:
- Data exploration
- Algorithm implementation
- Performance evaluation
- ML model training
- Interactive visualizations (folium, matplotlib)

## Key Features Explained

### 1. Role-Based Access Control
- **Relief Workers**: Can submit and view reports
- **Admins**: Full access including center management, optimization, predictions

### 2. Internationalization (i18n)
- English and Urdu translations
- Easy to extend to additional languages
- All UI strings are translatable
- Language switcher in header

### 3. Real-time Updates via WebSocket
- Instant notifications when new reports arrive
- Live map updates when allocations run
- No manual refresh needed
- Scalable to multiple concurrent users

### 4. Machine Learning Predictions
- RandomForest model trained on historical patterns
- Features: location, time (day/month), need type, urgency
- Predicts people affected for next 7 days
- Helps administrators plan resource stockpiling

### 5. Intelligent Allocation Algorithm
- **Priority**: High urgency requests processed first
- **Proximity**: Nearest center selected to minimize response time
- **Stock Awareness**: Only centers with available stock considered
- **Partial Allocation**: Handles cases where demand exceeds supply

### 6. Interactive Mapping
- Click map to select disaster location
- Color-coded markers for status visualization
- Route lines showing allocation paths
- Popup tooltips with detailed information
- Statistics panel with live counts

## Database Schema

### Centers Table
```sql
id (PK)           INTEGER
center_id         VARCHAR(50) UNIQUE
lat               FLOAT
lon               FLOAT
water_stock       INTEGER
food_stock        INTEGER
tent_stock        INTEGER
```

### Requests Table
```sql
id (PK)           INTEGER
request_id        VARCHAR(50) UNIQUE
lat               FLOAT
lon               FLOAT
people            INTEGER
need_type         VARCHAR(50)
urgency           VARCHAR(20)
status            VARCHAR(20)  -- 'pending' | 'allocated'
created_at        DATETIME
allocated_center_id VARCHAR(50) NULLABLE
resources_sent    INTEGER NULLABLE
distance          FLOAT NULLABLE
```

### Allocations Table
```sql
id (PK)           INTEGER
request_id        VARCHAR(50)
center_id         VARCHAR(50)
resources_sent    INTEGER
distance          FLOAT
created_at        DATETIME
```

## Scalability Considerations

### Current (Development)
- SQLite database (file-based)
- Single-server deployment
- Suitable for 1-100 concurrent users

### Production Ready
- PostgreSQL database (set via DATABASE_URL env var)
- Horizontal scaling with load balancer
- Redis for WebSocket message broker
- Celery for async tasks (notifications, ML training)
- CDN for frontend static assets
- Docker/Kubernetes deployment

## Security Considerations

1. **Authentication**: Currently uses role headers (X-User-Role)
   - Production: Replace with JWT or OAuth2
   - Add user registration/login with password hashing

2. **Authorization**: Role-based permissions enforced
   - Admin-only endpoints protected
   - Client-side and server-side validation

3. **Input Validation**: 
   - Type checking on all inputs
   - SQL injection prevented by SQLAlchemy ORM
   - XSS prevention via React's built-in escaping

4. **API Rate Limiting**: 
   - Recommended for production (Flask-Limiter)

5. **HTTPS**: 
   - Required in production
   - Secure WebSocket (wss://)

## Future Enhancements

1. **Mobile App**: React Native version for field workers
2. **Advanced ML**: LSTM for time-series forecasting
3. **Route Optimization**: Multi-stop delivery planning
4. **Inventory Tracking**: QR codes and barcode scanning
5. **Volunteer Management**: Coordinate human resources
6. **Damage Assessment**: Computer vision for satellite imagery
7. **Multi-tenancy**: Support multiple organizations
8. **Offline Mode**: Progressive Web App with service workers

## Deployment Architecture

### Development
```
npm start (React dev server) → localhost:3000
python app.py (Flask) → localhost:5000
```

### Production
```
Nginx → React Build (static files)
       ↓
    Gunicorn → Flask App (multiple workers)
       ↓
    PostgreSQL Database
       ↓
    Redis (WebSocket sessions)
```

## Monitoring & Logging

- **Application Logs**: Flask logging to file/stdout
- **Database Logs**: Query performance monitoring
- **Error Tracking**: Recommended: Sentry
- **Analytics**: User actions, allocation metrics
- **Health Checks**: /health endpoint for load balancer

## Conclusion

This architecture provides a robust, scalable foundation for disaster relief coordination. The modular design allows for easy extension and maintenance, while the real-time features ensure rapid response during emergencies.
