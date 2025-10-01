# AI-Driven Urban Sustainability Simulator 🌍

A web-based AI platform that uses machine learning and geospatial data to simulate sustainability scenarios in urban Pakistani cities (Faisalabad, Lahore, Karachi, Sargodha). The platform predicts Air Quality Index (AQI), energy demand, and flood risk, displaying results in an interactive dashboard aligned with UN Sustainable Development Goals (SDGs).

## 🎯 Project Vision

This simulator empowers urban planners, policymakers, and researchers to:
- **Forecast AQI** using LSTM-based time series models
- **Predict Energy Demand** based on population, temperature, and infrastructure
- **Assess Flood Risk** using geographical and climate data
- **Run What-If Scenarios** (e.g., "What if we add 30% solar energy?")
- **Visualize Results** on interactive maps with Leaflet.js and Plotly charts

### Alignment with UN SDGs
- **SDG 11**: Sustainable Cities and Communities
- **SDG 7**: Affordable and Clean Energy
- **SDG 13**: Climate Action
- **SDG 3**: Good Health and Well-being (air quality)

## ⚡ Tech Stack

### Backend
- **Python 3.9+** with Flask
- **Machine Learning**: scikit-learn, TensorFlow/Keras
- **Data Processing**: Pandas, NumPy, GeoPandas

### Frontend
- **React.js** for UI
- **Leaflet.js** for interactive maps
- **Plotly.js** for data visualizations
- **Axios** for API communication

### Data Sources
- OpenStreetMap (geospatial data)
- CSV datasets (AQI, weather, population)
- Mock data for demonstration

### Deployment
- **Docker** for containerization
- **Render** for backend hosting
- **Vercel** for frontend hosting

## 🗂️ Project Structure

```
urban-sustainability-simulator/
│── README.md
│── requirements.txt
│── .gitignore
│
├── data/                          # Datasets and notebooks
│   ├── raw/                       # Raw data files
│   ├── processed/                 # Preprocessed data
│   └── notebooks/                 # Jupyter notebooks for EDA
│
├── ml_models/                     # Machine learning models
│   ├── air_quality_forecast.py    # LSTM model for AQI
│   ├── energy_demand_model.py     # Regression for energy
│   ├── flood_risk_model.py        # Classification for flood risk
│   └── utils.py                   # Helper functions
│
├── backend/                       # Flask API
│   ├── app.py                     # Main Flask application
│   ├── routes/                    # API endpoints
│   │   ├── forecast_routes.py
│   │   ├── simulation_routes.py
│   │   └── healthcheck.py
│   ├── services/                  # Business logic
│   │   ├── data_loader.py
│   │   ├── model_inference.py
│   │   └── simulation_engine.py
│   └── tests/                     # API tests
│       └── test_api.py
│
├── frontend/                      # React application
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js
│   │   ├── index.js
│   │   ├── components/            # React components
│   │   │   ├── MapDashboard.js
│   │   │   ├── ScenarioSelector.js
│   │   │   └── ChartsPanel.js
│   │   ├── services/              # API integration
│   │   │   └── api.js
│   │   └── styles/
│   │       └── main.css
│   └── package.json
│
├── deployment/                    # Deployment configs
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── vercel.json
│   └── render.yaml
│
└── reports/                       # Documentation
    ├── sdg_alignment.md
    ├── design_doc.md
    └── final_paper_draft.docx
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- Docker (optional)

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd urban-sustainability-simulator
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the backend**
   ```bash
   cd backend
   python app.py
   ```
   Backend will run on `http://localhost:5000`

### Frontend Setup

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server**
   ```bash
   npm start
   ```
   Frontend will run on `http://localhost:3000`

### Docker Setup (Optional)

```bash
docker-compose up --build
```

This will start both backend and frontend in containers.

## 📊 Features

### 1. AQI Forecasting
- Predict air quality for next 7 days
- Uses LSTM neural network
- Visualizes PM2.5, PM10, NO2, SO2 levels

### 2. Energy Demand Prediction
- Forecast energy consumption
- Factors: population, temperature, infrastructure
- Supports scenario analysis (renewable energy integration)

### 3. Flood Risk Assessment
- Classify areas by flood risk (Low/Medium/High)
- Uses elevation, rainfall, proximity to water bodies
- Interactive map visualization

### 4. What-If Scenarios
- Adjust solar energy percentage
- Add green spaces (trees)
- Modify transportation policies
- See real-time impact on metrics

## 🔌 API Endpoints

### Forecast Endpoints
- `GET /api/forecast/aqi?city=Lahore&days=7` - Get AQI forecast
- `GET /api/forecast/energy?city=Karachi` - Get energy demand forecast
- `GET /api/forecast/flood-risk?city=Faisalabad` - Get flood risk map

### Simulation Endpoints
- `POST /api/simulation/scenario` - Run what-if scenario
  ```json
  {
    "city": "Lahore",
    "solar_percentage": 30,
    "green_spaces_increase": 20,
    "transport_policy": "electric_buses"
  }
  ```

### Health Check
- `GET /api/health` - Check API status

## 🧪 Testing

```bash
# Backend tests
cd backend
python -m pytest tests/

# Frontend tests (if implemented)
cd frontend
npm test
```

## 📝 Adding Real Data

Currently, the project uses mock data for demonstration. To add real datasets:

1. **Place raw data** in `data/raw/`
   - AQI data: CSV with columns [date, city, pm25, pm10, no2, so2]
   - Energy data: CSV with columns [date, city, consumption_kwh, temperature]
   - Flood data: GeoJSON with elevation and rainfall data

2. **Update data loaders** in `backend/services/data_loader.py`
   - Modify file paths and parsing logic

3. **Retrain models** using notebooks in `data/notebooks/`
   - Train on real data
   - Save models to `ml_models/saved_models/`

## 🌐 Deployment

### Deploy Backend to Render
1. Connect your GitHub repository to Render
2. Use `deployment/render.yaml` configuration
3. Set environment variables if needed

### Deploy Frontend to Vercel
1. Connect repository to Vercel
2. Set build command: `cd frontend && npm install && npm run build`
3. Set output directory: `frontend/build`

### Docker Deployment
```bash
docker-compose -f deployment/docker-compose.yml up -d
```

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - feel free to use this project for research and education.

## 👥 Authors

This project was developed as part of research on AI-driven urban sustainability in Pakistan.

## 📧 Contact

For questions or collaborations, please open an issue on GitHub.

## 🙏 Acknowledgments

- UN Sustainable Development Goals framework
- OpenStreetMap contributors
- Open-source ML and geospatial communities

---

**Note**: This is a research and educational tool. Predictions should be validated with domain experts before making policy decisions.
