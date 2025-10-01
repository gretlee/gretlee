# Disaster Relief Resource Allocator

A full-stack web application for optimizing emergency resource distribution during disaster events. The system enables relief workers to report disasters, administrators to manage relief centers, and automatically allocates resources using an intelligent priority-based algorithm.

![System Architecture](https://img.shields.io/badge/Stack-Flask%20%2B%20React-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![Node](https://img.shields.io/badge/Node-14%2B-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Features

### Core Functionality
- **🚨 Disaster Reporting**: Relief workers can submit disaster requests with location, affected people, resource needs, and urgency
- **📍 Interactive Mapping**: Real-time Leaflet.js map showing relief centers, disaster requests, and allocation routes
- **🎯 Intelligent Allocation**: Priority-based algorithm that:
  - Sorts requests by urgency (high > medium > low)
  - Assigns nearest center with available stock
  - Calculates optimal routes using Haversine distance
- **📊 ML Predictions**: RandomForest model predicts resource demand for next 7 days
- **🔔 Real-time Updates**: WebSocket integration for live map updates
- **🌐 Internationalization**: Multi-language support (English, Urdu)
- **👥 Role-Based Access**: Admin and Relief Worker roles with different permissions

### Technical Highlights
- **Backend**: Flask + SQLAlchemy ORM
- **Frontend**: React 18 + Leaflet.js
- **Database**: SQLite (dev), PostgreSQL-ready (prod)
- **Real-time**: Flask-SocketIO with Socket.io-client
- **ML**: scikit-learn (RandomForest)
- **Analytics**: Jupyter notebooks with matplotlib, seaborn, folium

## 📁 Project Structure

```
disaster-relief-allocator/
├── backend/                    # Flask backend
│   ├── app.py                 # Main Flask application
│   ├── services/              # Business logic services
│   │   ├── allocator.py       # Resource allocation algorithm
│   │   ├── notifications.py   # SMS/Email alerts (Twilio, SMTP)
│   │   └── prediction.py      # ML prediction service
│   ├── utils/                 # Utility functions
│   │   └── geo.py            # Haversine distance calculations
│   ├── auth/                  # Authentication & authorization
│   │   └── roles.py          # Role-based access control
│   └── requirements.txt       # Python dependencies
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── LoginForm.jsx  # User authentication
│   │   │   ├── ReportForm.jsx # Disaster report submission
│   │   │   └── MapView.jsx    # Interactive Leaflet map
│   │   ├── i18n.js           # Internationalization (en/ur)
│   │   ├── App.js            # Main React component
│   │   └── index.js          # React entry point
│   ├── public/
│   └── package.json
├── data/                       # Sample data
│   ├── centers.csv            # Relief centers (3 centers)
│   ├── requests.csv           # Sample requests (5 requests)
│   └── historical_requests.csv # Training data (90+ records)
├── notebooks/                  # Jupyter analysis
│   └── allocation.ipynb       # Analysis, visualization, ML training
├── docs/                       # Documentation
│   ├── architecture.md        # System architecture
│   └── setup.md              # Setup guide
├── tests/                      # Test suites
│   ├── test_allocator.py     # Allocation algorithm tests
│   └── test_prediction.py    # Prediction service tests
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm 6+

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd disaster-relief-allocator
```

2. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Frontend Setup**
```bash
cd frontend
npm install
```

4. **Initialize Database** (Optional - will auto-create)
```bash
cd backend
python
```
```python
from app import app, db
with app.app_context():
    db.create_all()
exit()
```

### Running the Application

1. **Start Backend** (Terminal 1)
```bash
cd backend
source venv/bin/activate
python app.py
```
Backend runs on: http://localhost:5000

2. **Start Frontend** (Terminal 2)
```bash
cd frontend
npm start
```
Frontend runs on: http://localhost:3000

3. **Open Browser**
Navigate to http://localhost:3000 and login with:
- Username: any name (e.g., "john_doe")
- Role: Admin or Relief Worker

## 📖 Usage Guide

### As a Relief Worker
1. **Login** with role "Relief Worker"
2. **Click on map** to select disaster location
3. **Fill report form**:
   - Number of people affected
   - Resource needed (water/food/tents/medical/shelter)
   - Urgency level (high/medium/low)
4. **Submit** - Map updates in real-time with red marker

### As an Administrator
1. **Login** with role "Administrator"
2. **View all reports** on the map
3. **Run optimization**:
   - Click "Run Optimization" button
   - Algorithm allocates resources
   - Green lines show allocation routes
4. **View predictions**: GET /predict endpoint
5. **Manage centers**: POST /centers endpoint

## 🧪 Running Tests

```bash
cd backend
pytest tests/test_allocator.py -v
pytest tests/test_prediction.py -v
```

Test coverage includes:
- ✅ Single/multiple request allocation
- ✅ Urgency prioritization
- ✅ Stock management
- ✅ Distance calculations
- ✅ ML model training
- ✅ Prediction output validation

## 📊 API Endpoints

### Public
- `GET /reports` - List all disaster reports
- `GET /centers` - List all relief centers
- `GET /allocations` - Get allocation history

### Relief Worker
- `POST /reports` - Submit new disaster report

### Admin Only
- `POST /centers` - Create new relief center
- `POST /optimize` - Run allocation algorithm
- `GET /predict` - Get 7-day demand forecast

## 🔧 Configuration

### Environment Variables

**Twilio SMS (Optional)**
```bash
export TWILIO_ACCOUNT_SID="your_sid"
export TWILIO_AUTH_TOKEN="your_token"
export TWILIO_PHONE_NUMBER="+1234567890"
```

**SMTP Email (Optional)**
```bash
export SMTP_HOST="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USER="your_email@gmail.com"
export SMTP_PASSWORD="your_app_password"
```

**Database (Production)**
```bash
export DATABASE_URL="postgresql://user:password@localhost/disaster_relief"
```

## 📈 Analytics & Visualization

Open the Jupyter notebook for detailed analysis:

```bash
cd notebooks
jupyter notebook allocation.ipynb
```

**Notebook includes:**
- 📊 Data exploration
- 🎯 Allocation algorithm demo
- 📉 Performance metrics (allocation rate, avg distance)
- 🤖 ML model training & evaluation
- 🗺️ Interactive Folium map with allocation routes
- 📅 7-day demand forecast visualization

## 🏗️ Architecture

```
React Frontend → Flask API → SQLAlchemy ORM → Database
       ↓              ↓
  Socket.io ← Flask-SocketIO
       ↓              ↓
  Real-time ← Allocation Engine
   Updates     ↓
            ML Prediction
```

See [docs/architecture.md](docs/architecture.md) for detailed architecture.

## 🛠️ Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Leaflet.js, Socket.io-client, i18next |
| Backend | Flask, SQLAlchemy, Flask-SocketIO |
| Database | SQLite (dev), PostgreSQL (prod) |
| ML/Analytics | scikit-learn, pandas, numpy |
| Visualization | matplotlib, seaborn, folium |
| Testing | pytest |

## 🌍 Internationalization

Currently supports:
- 🇬🇧 English (default)
- 🇵🇰 Urdu (اردو)

Add more languages in `frontend/src/i18n.js`

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👏 Credits

Built with:
- [Flask](https://flask.palletsprojects.com/) - Backend framework
- [React](https://react.dev/) - Frontend framework
- [Leaflet.js](https://leafletjs.com/) - Mapping library
- [scikit-learn](https://scikit-learn.org/) - Machine learning
- [Socket.IO](https://socket.io/) - Real-time communication

## 📞 Support

For issues, questions, or contributions:
- Create a GitHub issue
- See [docs/setup.md](docs/setup.md) for detailed setup
- See [docs/architecture.md](docs/architecture.md) for system design

---

**Built for disaster relief coordination and emergency resource optimization** 🌍
