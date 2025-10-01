# 🚀 Quick Setup Guide - Urban Sustainability Simulator

## Prerequisites

- Python 3.9+ installed
- Node.js 16+ installed
- Git installed
- Docker (optional, for containerized deployment)

---

## 🐍 Backend Setup (5 minutes)

### Step 1: Create Virtual Environment

```bash
# Navigate to project root
cd urban-sustainability-simulator

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 2: Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This installs:
- Flask (web framework)
- TensorFlow/Keras (deep learning)
- scikit-learn (machine learning)
- Pandas, NumPy (data processing)
- GeoPandas (geospatial data)
- And more...

### Step 3: Run the Backend

```bash
cd backend
python app.py
```

You should see:
```
🌍 Urban Sustainability Simulator API
Starting Flask development server...
API available at: http://localhost:5000
```

### Step 4: Test the API

Open your browser and visit:
- Health Check: http://localhost:5000/api/health
- Status: http://localhost:5000/api/status
- AQI Forecast: http://localhost:5000/api/forecast/aqi?city=Lahore&days=7

---

## ⚛️ Frontend Setup (5 minutes)

### Step 1: Install Node Dependencies

```bash
# Open a new terminal window
cd frontend
npm install
```

This installs:
- React (UI framework)
- Leaflet (mapping library)
- Plotly (charting library)
- Axios (HTTP client)

### Step 2: Start Development Server

```bash
npm start
```

The app will automatically open in your browser at:
http://localhost:3000

---

## 🐳 Docker Setup (Alternative - 2 minutes)

If you prefer Docker:

```bash
cd deployment
docker-compose up --build
```

This starts both backend and frontend in containers.

Access:
- Backend: http://localhost:5000
- Frontend: http://localhost:3000

---

## 📊 Using the Application

### 1. Select a City

Choose from the dropdown:
- Lahore
- Karachi
- Faisalabad
- Sargodha

### 2. View Current Forecasts

The dashboard automatically loads:
- 7-day AQI forecast
- Energy demand predictions
- Flood risk assessment
- Interactive map with risk zones

### 3. Run What-If Scenarios

Adjust the sliders:
- **Solar Energy**: 0-100% renewable adoption
- **Green Spaces**: 0-100% increase in urban parks
- **Electric Transport**: 0-100% EV adoption
- **Tree Planting**: Number of trees (0-1,000,000)

Click "🚀 Run Scenario" to see:
- Air quality improvements
- Energy demand changes
- Carbon emission reductions
- UN SDG alignment scores

### 4. Try Quick Templates

Use predefined scenarios:
- **Conservative Growth**: Modest 20% improvements
- **Moderate Progress**: Balanced 40% improvements
- **Aggressive Transformation**: Ambitious 70% improvements
- **Carbon Neutral 2040**: Path to net-zero emissions

---

## 🧪 Running Tests

### Backend Tests

```bash
cd backend
pytest tests/ -v
```

Expected output:
```
test_health_check ✓
test_aqi_forecast ✓
test_energy_forecast ✓
test_flood_risk ✓
test_scenario_simulation ✓
... 15 tests passed
```

### Frontend Tests (if implemented)

```bash
cd frontend
npm test
```

---

## 📁 Project Structure Overview

```
urban-sustainability-simulator/
│
├── README.md                    # Main documentation
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
│
├── data/                        # Datasets
│   ├── raw/                     # Raw CSV/GeoJSON files
│   ├── processed/               # Cleaned data
│   └── notebooks/               # Jupyter notebooks for EDA
│
├── ml_models/                   # Machine learning models
│   ├── air_quality_forecast.py  # LSTM AQI model
│   ├── energy_demand_model.py   # Energy regression model
│   ├── flood_risk_model.py      # Flood classifier
│   ├── utils.py                 # Helper functions
│   └── saved_models/            # Trained model files
│
├── backend/                     # Flask API
│   ├── app.py                   # Main Flask application
│   ├── routes/                  # API endpoints
│   ├── services/                # Business logic
│   └── tests/                   # Unit tests
│
├── frontend/                    # React application
│   ├── public/                  # Static assets
│   ├── src/                     # React source code
│   │   ├── App.js              # Main app component
│   │   ├── components/         # React components
│   │   ├── services/           # API integration
│   │   └── styles/             # CSS stylesheets
│   └── package.json            # Node dependencies
│
├── deployment/                  # Deployment configs
│   ├── Dockerfile              # Docker image
│   ├── docker-compose.yml      # Multi-container setup
│   ├── vercel.json             # Frontend hosting
│   └── render.yaml             # Backend hosting
│
└── reports/                     # Documentation
    ├── sdg_alignment.md        # UN SDG analysis
    ├── design_doc.md           # Technical design
    └── final_paper_draft.docx  # Research paper
```

---

## 🔧 Troubleshooting

### Issue: Port 5000 already in use

**Solution**: Change the port in `backend/app.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

### Issue: Module not found errors

**Solution**: Ensure virtual environment is activated and dependencies installed:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Issue: React app won't start

**Solution**: Delete `node_modules` and reinstall:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

### Issue: TensorFlow installation fails

**Solution**: Install without GPU support (smaller):
```bash
pip uninstall tensorflow
pip install tensorflow-cpu
```

### Issue: CORS errors in browser

**Solution**: Backend is configured for CORS. Ensure backend is running on port 5000.

---

## 📝 Adding Real Data

Currently using mock/demo data. To use real datasets:

### 1. Prepare AQI Data

Create `data/raw/aqi_data.csv`:
```csv
date,city,pm25,pm10,no2,so2,co,o3
2024-01-01,Lahore,89.5,135.2,48.3,26.1,15.8,52.3
2024-01-02,Lahore,92.1,140.5,49.2,27.3,16.2,53.1
...
```

### 2. Prepare Energy Data

Create `data/raw/energy_data.csv`:
```csv
date,city,population,temperature,consumption_kwh,industrial_zones,residential_areas,commercial_areas
2024-01-01,Lahore,11126285,18.5,5500000000,15,45,25
...
```

### 3. Train Models

```bash
cd ml_models
python air_quality_forecast.py  # Trains and saves LSTM model
python energy_demand_model.py   # Trains and saves regression model
python flood_risk_model.py      # Trains and saves classifier
```

### 4. Restart Backend

The API will automatically load the newly trained models.

---

## 🚀 Deployment to Production

### Option 1: Vercel (Frontend) + Render (Backend)

**Frontend (Vercel)**:
1. Push code to GitHub
2. Connect repository to Vercel
3. Set build command: `cd frontend && npm install && npm run build`
4. Deploy (automatic)

**Backend (Render)**:
1. Push code to GitHub
2. Create new Web Service on Render
3. Connect repository
4. Use `deployment/render.yaml` configuration
5. Deploy

### Option 2: Docker Deployment

```bash
cd deployment
docker-compose up -d
```

Access via:
- http://your-server-ip:5000 (backend)
- http://your-server-ip:3000 (frontend)

---

## 📚 Additional Resources

- **API Documentation**: See `/` endpoint when backend is running
- **Technical Design**: Read `reports/design_doc.md`
- **SDG Alignment**: Read `reports/sdg_alignment.md`
- **Research Paper**: See `reports/final_paper_draft.docx`

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📧 Support

For questions or issues:
- Open a GitHub Issue
- Email: sustainability-simulator@example.com
- Check `reports/design_doc.md` for technical details

---

## ✅ Quick Verification Checklist

After setup, verify:
- [ ] Backend runs without errors
- [ ] Frontend loads in browser
- [ ] Can select different cities
- [ ] AQI forecast displays
- [ ] Map shows city location
- [ ] Scenario simulator responds to slider changes
- [ ] Charts update when scenario runs
- [ ] All API tests pass

---

## 🎉 You're Ready!

Your Urban Sustainability Simulator is now running. Start exploring sustainability scenarios for Pakistani cities!

**Next Steps**:
1. Explore all four cities
2. Try different scenario templates
3. Run custom what-if analyses
4. Review SDG alignment scores
5. Export results for reports

Happy simulating! 🌍🌱
