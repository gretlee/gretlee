#!/bin/bash

# Disaster Relief Resource Allocator - Project Verification Script
# This script verifies that all required components are present

echo "=============================================="
echo "  Disaster Relief Resource Allocator"
echo "  Project Verification Script"
echo "=============================================="
echo ""

ERRORS=0

# Function to check file exists
check_file() {
    if [ -f "$1" ]; then
        echo "✅ $1"
    else
        echo "❌ MISSING: $1"
        ((ERRORS++))
    fi
}

# Function to check directory exists
check_dir() {
    if [ -d "$1" ]; then
        echo "✅ $1/"
    else
        echo "❌ MISSING: $1/"
        ((ERRORS++))
    fi
}

echo "📂 Checking Backend Structure..."
check_file "backend/app.py"
check_file "backend/requirements.txt"
check_dir "backend/services"
check_file "backend/services/allocator.py"
check_file "backend/services/prediction.py"
check_file "backend/services/notifications.py"
check_dir "backend/utils"
check_file "backend/utils/geo.py"
check_dir "backend/auth"
check_file "backend/auth/roles.py"
echo ""

echo "🎨 Checking Frontend Structure..."
check_file "frontend/package.json"
check_file "frontend/public/index.html"
check_file "frontend/src/App.js"
check_file "frontend/src/index.js"
check_file "frontend/src/i18n.js"
check_dir "frontend/src/components"
check_file "frontend/src/components/LoginForm.jsx"
check_file "frontend/src/components/ReportForm.jsx"
check_file "frontend/src/components/MapView.jsx"
echo ""

echo "📊 Checking Data Files..."
check_file "data/centers.csv"
check_file "data/requests.csv"
check_file "data/historical_requests.csv"
echo ""

echo "📓 Checking Notebooks..."
check_file "notebooks/allocation.ipynb"
echo ""

echo "📚 Checking Documentation..."
check_file "docs/architecture.md"
check_file "docs/setup.md"
check_file "README.md"
check_file "PROJECT_SUMMARY.md"
echo ""

echo "🧪 Checking Tests..."
check_file "tests/test_allocator.py"
check_file "tests/test_prediction.py"
echo ""

echo "⚙️ Checking Configuration..."
check_file ".gitignore"
echo ""

# Summary
echo "=============================================="
if [ $ERRORS -eq 0 ]; then
    echo "✅ ALL CHECKS PASSED!"
    echo "   Project is complete and ready to use."
    echo ""
    echo "🚀 Quick Start:"
    echo "   1. cd backend && pip3 install -r requirements.txt"
    echo "   2. python3 app.py"
    echo "   3. (New terminal) cd frontend && npm install && npm start"
    echo ""
    echo "📖 Documentation:"
    echo "   - Architecture: docs/architecture.md"
    echo "   - Setup Guide: docs/setup.md"
    echo "   - Main README: README.md"
    echo ""
    echo "🧪 Run Tests:"
    echo "   pytest tests/ -v"
else
    echo "❌ VERIFICATION FAILED"
    echo "   $ERRORS file(s) or directory(ies) missing"
    echo "   Please check the output above for details"
fi
echo "=============================================="

exit $ERRORS
