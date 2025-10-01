# Disaster Relief Resource Allocator - Setup Guide

This guide will help you set up and run the Disaster Relief Resource Allocator on your local machine.

## Prerequisites

- **Python**: 3.8 or higher
- **Node.js**: 14 or higher
- **npm**: 6 or higher
- **Git**: For version control

## Project Structure

```
disaster-relief-allocator/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── services/
│   │   ├── allocator.py       # Resource allocation logic
│   │   ├── notifications.py   # SMS/Email alerts
│   │   └── prediction.py      # ML prediction service
│   ├── utils/
│   │   └── geo.py             # Geospatial utilities
│   └── auth/
│       └── roles.py           # Role-based access control
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── LoginForm.jsx
│   │   │   ├── ReportForm.jsx
│   │   │   └── MapView.jsx
│   │   ├── i18n.js            # Internationalization
│   │   ├── App.js             # Main React component
│   │   └── index.js           # React entry point
│   ├── public/
│   └── package.json
├── data/
│   ├── centers.csv            # Sample relief centers
│   ├── requests.csv           # Sample disaster requests
│   └── historical_requests.csv # Training data
├── notebooks/
│   └── allocation.ipynb       # Analysis notebook
├── docs/
│   ├── architecture.md        # System architecture
│   └── setup.md               # This file
└── tests/
    ├── test_allocator.py      # Allocation tests
    └── test_prediction.py     # Prediction tests
```

## Installation

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd disaster-relief-allocator
```

### Step 2: Backend Setup

#### 2.1 Create Python Virtual Environment

```bash
cd backend
python -m venv venv

# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

#### 2.2 Install Python Dependencies

Create a `requirements.txt` file in the `backend` directory:

```txt
Flask==2.3.0
Flask-SQLAlchemy==3.0.5
Flask-CORS==4.0.0
Flask-SocketIO==5.3.4
python-socketio==5.9.0
eventlet==0.33.3
pandas==2.0.3
numpy==1.24.3
scikit-learn==1.3.0
joblib==1.3.2
twilio==8.5.0
```

Install dependencies:

```bash
pip install -r requirements.txt
```

#### 2.3 Initialize Database

The database will be created automatically when you first run the application. To pre-load sample data:

```bash
python
```

```python
from app import app, db, Center, Request
import pandas as pd

# Create tables
with app.app_context():
    db.create_all()
    
    # Load centers from CSV
    centers_df = pd.read_csv('../data/centers.csv')
    for _, row in centers_df.iterrows():
        center = Center(
            center_id=row['center_id'],
            lat=row['lat'],
            lon=row['lon'],
            water_stock=row['water_stock'],
            food_stock=row['food_stock'],
            tent_stock=row['tent_stock']
        )
        db.session.add(center)
    
    # Load requests from CSV
    requests_df = pd.read_csv('../data/requests.csv')
    for _, row in requests_df.iterrows():
        request = Request(
            request_id=row['request_id'],
            lat=row['lat'],
            lon=row['lon'],
            people=row['people'],
            need_type=row['need_type'],
            urgency=row['urgency']
        )
        db.session.add(request)
    
    db.session.commit()
    print("Database initialized with sample data!")

exit()
```

### Step 3: Frontend Setup

#### 3.1 Install Node Dependencies

```bash
cd ../frontend
npm install
```

This will install all dependencies listed in `package.json`:
- react
- react-dom
- leaflet
- react-leaflet
- socket.io-client
- i18next
- react-i18next

#### 3.2 Configure API Endpoint (Optional)

If your backend runs on a different port/host, update the API URLs in the frontend components:

- In `MapView.jsx`, `ReportForm.jsx`: Change `http://localhost:5000` to your backend URL
- In `App.js`: Change WebSocket connection URL

### Step 4: Jupyter Notebook Setup (Optional)

If you want to run the analysis notebook:

```bash
cd ../notebooks
pip install jupyter matplotlib seaborn folium
jupyter notebook allocation.ipynb
```

## Running the Application

### Step 1: Start the Backend Server

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python app.py
```

The backend will start on: **http://localhost:5000**

You should see output like:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

### Step 2: Start the Frontend Development Server

In a **new terminal window**:

```bash
cd frontend
npm start
```

The frontend will start on: **http://localhost:3000**

Your browser should automatically open. If not, navigate to `http://localhost:3000`.

## Using the Application

### Login

1. On the login page, enter any username (e.g., "john_doe")
2. Select a role:
   - **Relief Worker**: Can submit and view disaster reports
   - **Administrator**: Full access (manage centers, run optimization, view predictions)
3. Click "Login"

### Submit a Disaster Report (Relief Worker or Admin)

1. Click on the map to select a location
2. The latitude and longitude will auto-fill
3. Enter the number of people affected
4. Select the resource needed (water, food, tents, medical, shelter)
5. Select urgency level (low, medium, high)
6. Click "Submit Report"
7. The map will update in real-time with a new red marker

### Run Optimization (Admin Only)

1. After logging in as Admin
2. Click the "Run Optimization" button on the map
3. The algorithm will:
   - Sort requests by urgency
   - Assign each request to the nearest center with available stock
   - Draw green lines showing allocation routes
   - Update marker colors to green for allocated requests

### View Predictions (Admin Only)

Currently exposed via API endpoint:

```bash
curl http://localhost:5000/predict
```

Returns a 7-day forecast of resource demand.

### Change Language

Click the language buttons in the header:
- **English** (default)
- **اردو** (Urdu)

All UI text will update instantly.

## API Endpoints

### Public Endpoints

- `GET /reports` - Get all disaster reports
- `GET /centers` - Get all relief centers
- `GET /allocations` - Get allocation history

### Relief Worker Endpoints

- `POST /reports` - Submit a new disaster report
  ```json
  {
    "lat": 33.6844,
    "lon": 73.0479,
    "people": 50,
    "need_type": "water",
    "urgency": "high"
  }
  ```

### Admin Endpoints

- `POST /centers` - Create a new relief center
  ```json
  {
    "center_id": "CTR004",
    "lat": 32.0836,
    "lon": 72.6710,
    "water_stock": 1000,
    "food_stock": 800,
    "tent_stock": 150
  }
  ```

- `POST /optimize` - Run resource allocation algorithm
  ```bash
  curl -X POST http://localhost:5000/optimize -H "X-User-Role: admin"
  ```

- `GET /predict` - Get 7-day demand forecast
  ```bash
  curl http://localhost:5000/predict
  ```

## Optional: Configure Notifications

### SMS Notifications (Twilio)

1. Sign up for a Twilio account: https://www.twilio.com/try-twilio
2. Get your Account SID, Auth Token, and Phone Number
3. Set environment variables:

```bash
# Linux/Mac:
export TWILIO_ACCOUNT_SID="your_account_sid"
export TWILIO_AUTH_TOKEN="your_auth_token"
export TWILIO_PHONE_NUMBER="+1234567890"

# Windows:
set TWILIO_ACCOUNT_SID=your_account_sid
set TWILIO_AUTH_TOKEN=your_auth_token
set TWILIO_PHONE_NUMBER=+1234567890
```

4. Restart the Flask server

### Email Notifications (SMTP)

1. Use your email provider's SMTP settings (Gmail, Outlook, etc.)
2. Set environment variables:

```bash
# Linux/Mac:
export SMTP_HOST="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USER="your_email@gmail.com"
export SMTP_PASSWORD="your_app_password"
export FROM_EMAIL="your_email@gmail.com"

# Windows:
set SMTP_HOST=smtp.gmail.com
set SMTP_PORT=587
set SMTP_USER=your_email@gmail.com
set SMTP_PASSWORD=your_app_password
set FROM_EMAIL=your_email@gmail.com
```

**Note**: For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833) instead of your regular password.

## Running Tests

### Backend Tests

```bash
cd backend
pytest tests/
```

Or run specific test files:

```bash
pytest tests/test_allocator.py
pytest tests/test_prediction.py
```

### Frontend Tests (if implemented)

```bash
cd frontend
npm test
```

## Troubleshooting

### Port Already in Use

**Backend (Port 5000)**:
```bash
# Linux/Mac - Find process
lsof -ti:5000

# Kill process
kill -9 <PID>

# Or change port in app.py
socketio.run(app, debug=True, host='0.0.0.0', port=5001)
```

**Frontend (Port 3000)**:
```bash
# Change port
PORT=3001 npm start
```

### Database Errors

Delete the database and recreate:

```bash
cd backend
rm disaster_relief.db
python
# Then run the initialization code from Step 2.3
```

### CORS Errors

Ensure `Flask-CORS` is installed and configured in `app.py`:

```python
from flask_cors import CORS
CORS(app)
```

### WebSocket Connection Failed

- Check that the backend is running
- Verify the WebSocket URL in `App.js` matches your backend
- Check browser console for error messages

### Map Not Loading

- Check internet connection (Leaflet requires external tiles)
- Verify `leaflet.css` is imported
- Check browser console for errors

### Import Errors in Python

Make sure you're in the correct directory and virtual environment:

```bash
cd backend
source venv/bin/activate
python -c "import flask; print(flask.__version__)"
```

## Production Deployment

### Backend

1. **Use PostgreSQL**:
   ```bash
   export DATABASE_URL="postgresql://user:password@localhost/disaster_relief"
   ```

2. **Use Gunicorn** instead of Flask dev server:
   ```bash
   pip install gunicorn
   gunicorn --worker-class eventlet -w 1 app:app --bind 0.0.0.0:5000
   ```

3. **Use Redis** for WebSocket message broker:
   ```bash
   pip install redis
   # In app.py:
   socketio = SocketIO(app, cors_allowed_origins="*", message_queue='redis://')
   ```

### Frontend

1. **Build for production**:
   ```bash
   cd frontend
   npm run build
   ```

2. **Serve with Nginx**:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       root /path/to/frontend/build;
       index index.html;
       
       location / {
           try_files $uri /index.html;
       }
       
       location /api {
           proxy_pass http://localhost:5000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
       }
   }
   ```

### Environment Variables

Create a `.env` file (never commit this):

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost/disaster_relief

# Twilio
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=your_number

# SMTP
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email
SMTP_PASSWORD=your_password
FROM_EMAIL=your_email

# Security
SECRET_KEY=generate-a-random-secret-key
```

## Support and Documentation

- **Architecture**: See `docs/architecture.md`
- **API Reference**: See backend docstrings
- **Issues**: Create a GitHub issue
- **Contributions**: Pull requests welcome!

## License

[Your License Here]

## Credits

Built with Flask, React, Leaflet.js, and scikit-learn for disaster relief coordination.
