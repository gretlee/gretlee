# 🎬 Expected Output Guide

## What You Should See When Running the Application

---

## 🐍 Backend Startup (Terminal 1)

When you run `python backend/app.py`, you should see:

```
============================================================
🌍 Urban Sustainability Simulator API
============================================================
Starting Flask development server...
API available at: http://localhost:5000
Health check: http://localhost:5000/api/health
============================================================
 * Serving Flask app 'backend.app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://localhost:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: xxx-xxx-xxx
```

### ✅ Success Indicators:
- No import errors
- Server running on port 5000
- Debug mode active
- No crash on startup

### Testing Backend:
Open browser and visit: `http://localhost:5000/api/health`

**Expected Response:**
```json
{
  "status": "healthy",
  "message": "Urban Sustainability Simulator API is running",
  "timestamp": "2025-10-01T17:30:00.000000",
  "version": "1.0.0"
}
```

---

## ⚛️ Frontend Startup (Terminal 2)

When you run `cd frontend && npm start`, you should see:

```
Compiled successfully!

You can now view urban-sustainability-simulator-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.1.x:3000

Note that the development build is not optimized.
To create a production build, use npm run build.

webpack compiled successfully
```

### ✅ Success Indicators:
- Compilation successful
- No JSX errors
- Browser opens automatically
- Running on port 3000

---

## 🌐 Web Interface (Browser)

When you open `http://localhost:3000`, you should see:

### Header Section
```
┌─────────────────────────────────────────────────────────┐
│  🌍 Urban Sustainability Simulator                      │
│  AI-Driven Forecasting for Pakistani Cities             │
│                                                          │
│                            Select City: [Lahore     ▼]  │
└─────────────────────────────────────────────────────────┘
```

### Main Dashboard

#### Left Panel: Map
```
┌─────────────────────────────────────────────────────────┐
│ 📍 Lahore Map View                                      │
│ Population: 11,126,285  Area: 1,772 km²                 │
│                                                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │                                                   │   │
│  │     [Interactive OpenStreetMap showing Lahore]   │   │
│  │                                                   │   │
│  │     • City center marker                         │   │
│  │     • Colored circles for flood zones            │   │
│  │     • Green = Low Risk                           │   │
│  │     • Orange = Medium Risk                       │   │
│  │     • Red = High Risk                            │   │
│  │                                                   │   │
│  └─────────────────────────────────────────────────┘   │
│                                                          │
│  Flood Risk Legend                                      │
│  🟢 Low Risk                                            │
│  🟠 Medium Risk                                         │
│  🔴 High Risk                                           │
└─────────────────────────────────────────────────────────┘
```

#### Right Panel: Scenario Builder
```
┌─────────────────────────────────────────────────────────┐
│ 🎯 Scenario Builder                                     │
│ Adjust parameters to simulate sustainability interventions │
│                                                          │
│ Quick Templates:                                         │
│ [Conservative] [Moderate] [Aggressive] [Carbon Neutral] │
│                                                          │
│ ☀️ Solar Energy Adoption: 30%                           │
│ [============================----------------] 30        │
│ Percentage of energy from solar sources                 │
│                                                          │
│ 🌳 Green Spaces Increase: 20%                           │
│ [====================------------------------] 20        │
│ Additional green space as % of city area                │
│                                                          │
│ 🚌 Electric Transport: 40%                              │
│ [================================------------] 40        │
│ Percentage of electric vehicles in fleet                │
│                                                          │
│ 🌲 Tree Planting Program                                │
│ [100000                            ] trees              │
│ Number of trees to plant                                │
│                                                          │
│ [🚀 Run Scenario]  [Reset]                              │
│                                                          │
│ 💡 How It Works                                         │
│ Adjust the sliders to simulate different                │
│ sustainability interventions. The AI models              │
│ will predict the impact on air quality,                  │
│ energy demand, and carbon emissions.                     │
└─────────────────────────────────────────────────────────┘
```

#### Right Panel: Charts
```
┌─────────────────────────────────────────────────────────┐
│ 📈 Analytics Dashboard                                  │
│                                                          │
│ 📊 AQI Forecast (7 Days)                                │
│ ┌─────────────────────────────────────────────────┐    │
│ │ AQI                                              │    │
│ │ 160│              ○                              │    │
│ │ 150│         ○         ○                         │    │
│ │ 140│    ○                   ○                    │    │
│ │ 130│                             ○          ○    │    │
│ │    └──────────────────────────────────────────  │    │
│ │     Oct 2  Oct 3  Oct 4  Oct 5  Oct 6  Oct 7   │    │
│ └─────────────────────────────────────────────────┘    │
│ Current trend: Unhealthy                                │
│                                                          │
│ 🌫️ Pollutant Levels                                    │
│ ┌─────────────────────────────────────────────────┐    │
│ │ [Multi-line chart showing:]                      │    │
│ │ — PM2.5 (red line)                               │    │
│ │ — PM10 (purple line)                             │    │
│ │ — NO2 (blue line)                                │    │
│ │ — SO2 (green line)                               │    │
│ └─────────────────────────────────────────────────┘    │
│                                                          │
│ ⚡ Energy Demand                                        │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐                │
│ │  5.56    │ │  N/A     │ │  N/A     │                │
│ │ Baseline │ │ Scenario │ │  Change  │                │
│ │  (GWh)   │ │  (GWh)   │ │   (%)    │                │
│ └──────────┘ └──────────┘ └──────────┘                │
│                                                          │
│ 🌊 Flood Risk Distribution                              │
│ ┌─────────────────────────────────────────────────┐    │
│ │     [Pie chart showing:]                         │    │
│ │     🟢 60% Low Risk                              │    │
│ │     🟠 30% Medium Risk                           │    │
│ │     🔴 10% High Risk                             │    │
│ └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

### Footer Section
```
┌─────────────────────────────────────────────────────────┐
│ Aligned with UN SDGs: [SDG 3] [SDG 7] [SDG 11] [SDG 13]│
│ Demo version - Using mock data for demonstration        │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 After Running a Scenario

When you click "🚀 Run Scenario" with Solar: 30%, Green: 20%, Electric: 40%, Trees: 100,000:

### Updated Map Panel
```
┌─────────────────────────────────────────────────────────┐
│ Scenario Impact                                          │
│                                                          │
│ ┌──────────┐                                            │
│ │   68.5   │  Good                                      │
│ │          │                                             │
│ │Sustainability Score                                    │
│ └──────────┘                                            │
└─────────────────────────────────────────────────────────┘
```

### New Impact Analysis Section
```
┌─────────────────────────────────────────────────────────┐
│ 🎯 Scenario Impact Analysis                             │
│                                                          │
│ Air Quality                                              │
│ ├─ Baseline AQI: 150                                    │
│ ├─ Projected AQI: 130.5                                 │
│ └─ Improvement: -19.5 (13.0%)                           │
│                                                          │
│ Carbon Emissions                                         │
│ ├─ Baseline: 27,815,713 tons CO₂                        │
│ ├─ Projected: 22,252,570 tons CO₂                       │
│ └─ Reduction: -5,563,143 tons (20.0%)                   │
│                                                          │
│ UN SDG Alignment                                         │
│ ┌─────────────────────────────────────────────────┐    │
│ │ SDG 3  [████████████████░░░░] 72/100            │    │
│ │ SDG 7  [██████████████░░░░░░] 60/100            │    │
│ │ SDG 11 [█████████████████░░░] 73/100            │    │
│ │ SDG 13 [██████████████████░░] 77/100            │    │
│ └─────────────────────────────────────────────────┘    │
│                                                          │
│ Overall SDG Score: 70.5/100 (Good)                      │
└─────────────────────────────────────────────────────────┘
```

---

## 🧪 Testing the API Directly

### Test 1: Health Check
```bash
curl http://localhost:5000/api/health
```

**Expected:**
```json
{
  "status": "healthy",
  "message": "Urban Sustainability Simulator API is running",
  "timestamp": "2025-10-01T17:30:00.000000",
  "version": "1.0.0"
}
```

### Test 2: AQI Forecast
```bash
curl "http://localhost:5000/api/forecast/aqi?city=Lahore&days=7"
```

**Expected:**
```json
{
  "status": "success",
  "city": "Lahore",
  "forecast_days": 7,
  "data": {
    "dates": ["2025-10-02", "2025-10-03", ...],
    "predictions": {
      "pm25": [75.2, 73.8, 76.1, ...],
      "pm10": [120.5, 118.2, 121.3, ...],
      "no2": [44.3, 43.1, 45.2, ...],
      "so2": [24.7, 25.1, 24.3, ...],
      "aqi": [150, 148, 152, ...],
      "category": ["Unhealthy", "Unhealthy", ...]
    }
  }
}
```

### Test 3: Run Scenario
```bash
curl -X POST http://localhost:5000/api/simulation/scenario \
  -H "Content-Type: application/json" \
  -d '{
    "city": "Lahore",
    "solar_percentage": 30,
    "green_spaces_increase": 20,
    "electric_transport_percentage": 40,
    "tree_planting": 100000
  }'
```

**Expected:**
```json
{
  "status": "success",
  "data": {
    "city": "Lahore",
    "scenario": {...},
    "impacts": {
      "energy": {...},
      "air_quality": {...},
      "carbon_emissions": {...}
    },
    "sdg_alignment": {...},
    "sustainability_score": {
      "score": 68.5,
      "rating": "Good"
    }
  }
}
```

---

## 🐳 Docker Output

When you run `docker-compose up --build`:

```
[+] Building 45.2s (18/18) FINISHED
 => [backend internal] load build definition
 => => transferring dockerfile: 1.23kB
 => [backend internal] load .dockerignore
 => [backend internal] load metadata for docker.io/library/python:3.11-slim
 => [backend builder 1/6] FROM docker.io/library/python:3.11-slim
 => [backend builder 2/6] WORKDIR /app
 => [backend builder 3/6] RUN apt-get update && apt-get install -y gcc
 => [backend builder 4/6] COPY requirements.txt .
 => [backend builder 5/6] RUN pip install --no-cache-dir -r requirements.txt
 => [backend stage-1 1/6] FROM python:3.11-slim
 => [backend stage-1 2/6] WORKDIR /app
 => [backend stage-1 3/6] RUN apt-get update && apt-get install -y libgomp1
 => [backend stage-1 4/6] COPY --from=builder /usr/local/lib/python3.11
 => [backend stage-1 5/6] COPY . .
 => [backend stage-1 6/6] RUN mkdir -p data/raw data/processed
 => [backend] exporting to image
 => => exporting layers
 => => writing image sha256:abc123...
 => => naming to docker.io/library/deployment_backend

[+] Running 2/2
 ✔ Network sustainability-network  Created
 ✔ Container sustainability-backend Started

sustainability-backend  | ============================================================
sustainability-backend  | 🌍 Urban Sustainability Simulator API
sustainability-backend  | ============================================================
sustainability-backend  | Starting Flask development server...
sustainability-backend  | API available at: http://localhost:5000
sustainability-backend  |  * Serving Flask app 'backend.app'
sustainability-backend  |  * Running on all addresses (0.0.0.0)
sustainability-backend  |  * Running on http://0.0.0.0:5000
```

---

## ✅ Success Checklist

When everything is working correctly, you should be able to:

- [ ] Backend runs without errors on port 5000
- [ ] Frontend runs without errors on port 3000
- [ ] Browser opens automatically to frontend
- [ ] Map displays with city marker
- [ ] City selector shows 4 cities
- [ ] AQI chart displays with data
- [ ] Pollutants chart shows 4 lines
- [ ] Energy metrics display
- [ ] Flood risk pie chart appears
- [ ] Sliders are interactive and responsive
- [ ] "Run Scenario" button works
- [ ] Scenario results appear after submission
- [ ] Impact analysis shows improvements
- [ ] SDG scores display correctly
- [ ] No console errors in browser
- [ ] No Python errors in terminal
- [ ] API endpoints respond correctly
- [ ] Loading indicators work
- [ ] Template buttons function

---

## 🚨 Common Issues & Solutions

### Issue: "Module not found" error

**Symptom:**
```
ModuleNotFoundError: No module named 'flask'
```

**Solution:**
```bash
source venv/bin/activate  # Activate virtual environment
pip install -r requirements.txt
```

---

### Issue: Port already in use

**Symptom:**
```
OSError: [Errno 48] Address already in use
```

**Solution:**
```bash
# Find and kill process on port 5000
lsof -ti:5000 | xargs kill -9
# Or change port in backend/app.py
```

---

### Issue: React compilation errors

**Symptom:**
```
Failed to compile.
Module not found: Can't resolve 'leaflet'
```

**Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

### Issue: Blank white screen

**Symptom:** Frontend loads but shows blank page

**Solution:**
1. Check browser console for errors (F12)
2. Ensure backend is running on port 5000
3. Check network tab for failed API calls
4. Verify proxy setting in frontend/package.json

---

## 🎉 Successful Deployment Indicators

### Backend Health
```bash
curl http://localhost:5000/api/health
# Should return: {"status": "healthy", ...}
```

### Frontend Access
```bash
curl http://localhost:3000
# Should return: HTML with "Urban Sustainability Simulator"
```

### Docker Health
```bash
docker ps
# Should show: sustainability-backend (healthy)
```

### Full Integration
1. Open http://localhost:3000
2. Select "Karachi" from dropdown
3. Map updates to Karachi location
4. Charts display Karachi data
5. Adjust sliders
6. Click "Run Scenario"
7. Impact analysis appears within 2 seconds

---

**If you see all of the above, congratulations! 🎉**

Your Urban Sustainability Simulator is fully operational and ready for use!

🌍 Start simulating sustainable futures for Pakistani cities! 🌱
