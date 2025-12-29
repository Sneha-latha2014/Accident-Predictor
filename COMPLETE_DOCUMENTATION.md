# 📚 Complete Code Documentation & Guide

## Project: Accident Severity Prediction System

A Django web application that uses XGBoost machine learning to predict accident severity based on road conditions, weather, vehicle type, and other factors.

---

## 🎯 Project Structure Overview

```
accident_prediction/
│
├── README.md                           # This guide
├── manage.py                           # Django management command
├── db.sqlite3                          # SQLite database
│
├── accident_predictor/                 # Django project config
│   ├── settings.py                     # Django settings (INSTALLED_APPS, DB, etc.)
│   ├── urls.py                         # Main URL routing
│   ├── wsgi.py                         # WSGI entry point
│   └── asgi.py                         # ASGI entry point
│
├── predictor/                          # Main application
│   ├── models.py                       # Database models (PredictionHistory)
│   ├── views.py                        # URL handlers (dashboard, predict, result)
│   ├── forms.py                        # Form definitions (PredictionForm)
│   ├── utils.py                        # ML utilities (training, prediction, scoring)
│   ├── urls.py                         # App URL routing
│   ├── admin.py                        # Admin panel configuration
│   ├── apps.py                         # App configuration
│   ├── tests.py                        # Unit tests
│   │
│   ├── migrations/                     # Database migrations
│   │   └── 0001_initial.py             # Initial migration
│   │
│   ├── ml_models/                      # ML model storage
│   │   ├── accident_prediction_india.csv         # Training dataset
│   │   ├── accident_model.pkl                    # Trained XGBoost model
│   │   └── label_encoders.pkl                    # Encoder objects
│   │
│   ├── static/                         # Static files (CSS, JS, images)
│   │   └── predictor/
│   │       ├── css/                    # CSS stylesheets
│   │       └── js/                     # JavaScript files
│   │
│   ├── templates/                      # HTML templates
│   │   └── predictor/
│   │       ├── base.html               # Base template (extends to others)
│   │       ├── dashboard.html          # Statistics page
│   │       ├── predict.html            # Prediction form page
│   │       └── result.html             # Prediction result page
│   │
│   └── tests/                          # Additional tests
│       └── test_model_accuracy.py      # Model accuracy tests
│
├── media/                              # User-uploaded files
│
└── staticfiles/                        # Collected static files
```

---

## 🔄 User Flow & Application Logic

### Complete User Journey

```
1. USER VISITS APP
   └─→ Dashboard Page Loads
       ├─ Shows total predictions
       ├─ Shows today's predictions count
       └─ Lists recent 10 predictions

2. USER CLICKS "PREDICT"
   └─→ Prediction Form Page Loads
       ├─ Displays 8 input fields
       ├─ Fields populated from dataset choices
       └─ Dropdown options loaded dynamically

3. USER FILLS FORM & SUBMITS
   └─→ views.predict() Handler Processes
       ├─ Form validation (required fields)
       ├─ Calls ML model: predict_accident_severity()
       ├─ Saves prediction to database
       └─ Redirects to result page

4. ML MODEL MAKES PREDICTION
   └─→ utils.predict_accident_severity()
       ├─ Loads trained XGBoost model
       ├─ Maps user inputs to model features
       ├─ Encodes categorical variables
       ├─ Gets probabilities from model
       ├─ Calculates risk score (0.0-1.0)
       ├─ Adjusts probabilities based on risk
       └─ Returns severity + confidence

5. USER SEES RESULTS
   └─→ Result Page Displays
       ├─ Predicted severity (Low/High/Severe)
       ├─ Confidence score (0-100%)
       ├─ Risk score (0-10)
       ├─ All input parameters
       └─ Links to dashboard or new prediction
```

---

## 📝 Database Schema

### PredictionHistory Model

Stores all prediction records in the SQLite database.

| Field | Type | Purpose |
|-------|------|---------|
| id | AutoField | Primary key (auto-generated) |
| road_type | CharField | Road type: Highway, Junction, etc. |
| vehicle_type | CharField | Vehicle type: Car, Truck, Motorcycle, etc. |
| time_of_day | CharField | Time period: Day, Night, Morning, Evening |
| weather | CharField | Weather: Clear, Rainy, Foggy, Snowy, etc. |
| light_condition | CharField | Lighting: Day or Night |
| location | CharField | Geographic location: CA, TX, FL, NY, etc. |
| day | CharField | Day of week: Monday-Sunday |
| speed_limit | IntegerField | Speed limit in km/h |
| prediction_result | CharField | ML prediction: Low, High, Severe, etc. |
| confidence_score | FloatField | ML confidence: 0-100% |
| risk_score | FloatField | Risk score: 0-10 scale |
| created_at | DateTimeField | Timestamp when record was created |

---

## 🧠 Machine Learning Pipeline

### Training Process (`train_and_save_model()`)

**Input:** India Accidents Dataset (CSV)  
**Output:** Trained XGBoost model + encoders saved to disk

```
Step 1: Load Dataset
   ├─ Read accident_prediction_india.csv
   ├─ Map severity labels (Minor→0, Serious→1, Fatal→2)
   └─ Remove rows with missing severity

Step 2: Feature Engineering
   ├─ Extract hour from time string
   ├─ Create light condition from hour (Night/Day)
   ├─ Create time category (Night/Morning/Afternoon/Evening)
   ├─ Create speed category (Slow/Medium/Fast/VeryFast)
   └─ Extract 15 total features

Step 3: Data Balancing (3 Techniques)
   ├─ Technique 1: Compute class weights (handle imbalance)
   ├─ Technique 2: Oversample minority classes
   └─ Technique 3: Apply weights in training

Step 4: Encode Categorical Variables
   ├─ Convert text fields to numeric values
   ├─ Use LabelEncoder for each categorical feature
   └─ Save encoders for later use

Step 5: Train-Test Split
   ├─ 80% training data
   └─ 20% validation data

Step 6: Train XGBoost Model
   ├─ Create XGBoost classifier
   ├─ Set hyperparameters (300 estimators, max_depth=8, learning_rate=0.1)
   ├─ Apply sample weights based on class weights
   └─ Fit model on training data

Step 7: Evaluate Model
   ├─ Calculate training accuracy
   ├─ Calculate validation accuracy
   ├─ Log class distribution in predictions
   └─ Show top 10 important features

Step 8: Save Model to Disk
   ├─ Save XGBoost model as accident_model.pkl
   └─ Save encoders as label_encoders.pkl
```

### Prediction Process (`predict_accident_severity()`)

**Input:** User's accident scenario (8 fields)  
**Output:** Severity prediction + confidence score

```
Step 1: Load Model
   ├─ Check memory cache first (for performance)
   ├─ Load from disk if not cached
   └─ Auto-train if files don't exist

Step 2: Map User Inputs to Model Features
   ├─ Convert road type (Highway → National Highway)
   ├─ Convert vehicle type (Motorcycle → Two-Wheeler)
   ├─ Convert weather (Rain → Rainy)
   ├─ Create hour from time_of_day
   ├─ Create time_category from hour
   ├─ Create speed_category from speed_limit
   ├─ Map road condition from weather
   └─ Map traffic control from road type

Step 3: Create Feature DataFrame
   ├─ 15 features in correct order
   ├─ Default values for missing data (Alcohol=No, Num_Vehicles=1)
   └─ Ensure all features present

Step 4: Encode Features
   ├─ Convert categorical text to numbers
   ├─ Use saved LabelEncoder objects
   ├─ Handle unseen categories gracefully
   └─ Fill NaN values with 0

Step 5: Get Model Probabilities
   ├─ Pass encoded features to XGBoost
   └─ Get probability for each class (0, 1, 2)
       └─ Class 0: Low severity
       └─ Class 1: High severity
       └─ Class 2: Severe severity

Step 6: Calculate Risk Score
   ├─ Analyze input conditions
   ├─ Assign risk points (0.0-1.0):
   │   ├─ Road type (Junctions = 0.4 risk)
   │   ├─ Vehicle type (Motorcycle = 0.3 risk)
   │   ├─ Time (Night = 0.3 risk)
   │   ├─ Weather (Snow = 0.35 risk)
   │   ├─ Speed (High speed = 0.2 risk)
   │   └─ Day (Weekends = 0.1 risk)
   └─ Normalize to 0.0-1.0 range

Step 7: Adjust Probabilities
   ├─ If risk < 0.3: Boost Low prediction
   ├─ If risk < 0.5: Slightly boost Low
   ├─ If risk < 0.7: Boost High/Severe slightly
   └─ If risk >= 0.7: Strongly boost Severe prediction

Step 8: Return Final Prediction
   ├─ Find class with highest adjusted probability
   ├─ Return (severity_label, confidence)
   └─ Example: ('High', 0.82)
```

---

## 🛣️ URL Routing

### Main URLs (`accident_predictor/urls.py`)
```
/admin/                    → Django admin panel
/                          → predictor app URLs (see below)
/media/                    → User-uploaded files (development only)
```

### App URLs (`predictor/urls.py`)
```
/                          → views.dashboard()      [dashboard page]
/predict/                  → views.predict()        [prediction form page]
/result/<int:pk>/          → views.result()         [prediction result page]
```

---

## 🎨 Template Structure

### Template Inheritance
```
base.html
├── Defines: navbar, footer, styles
├── Provides: {% block content %}, {% block extra_css %}, {% block extra_js %}
│
├─── dashboard.html extends base.html
│    └── Displays: statistics, recent predictions
│
├─── predict.html extends base.html
│    └── Displays: 8-field form for entering scenario
│
└─── result.html extends base.html
     └── Displays: prediction results, confidence, risk score
```

### Page Descriptions

**dashboard.html**
- Shows total predictions made
- Shows predictions made today
- Lists 10 most recent predictions
- Displays model accuracy metric

**predict.html**
- Form with 8 input fields
- Dropdowns populated from dataset
- Submit button triggers prediction
- Back button to dashboard

**result.html**
- Predicted severity (colored badge)
- Confidence score (percentage)
- Risk score (0-10 scale)
- Input parameters summary
- Links to dashboard or new prediction

---

## 🔧 How Each Component Works

### models.py - Database
```python
PredictionHistory
├── Stores prediction records
├── 8 input fields (from user form)
├── 3 output fields (from ML model)
├── 1 timestamp field (when created)
└── Methods:
    └── __str__() → String representation
```

### views.py - URL Handlers
```python
dashboard()
├── Counts total predictions
├── Counts today's predictions
├── Gets 10 recent predictions
└── Renders dashboard template

predict()
├── GET: Shows form with choices
├── POST: Processes form submission
│   ├─ Validates input
│   ├─ Calls ML model
│   ├─ Saves to database
│   └─ Redirects to result page
└── Handles errors gracefully

result()
├── Gets prediction from database (by pk)
├── Passes to template for display
└── Handles missing prediction with error message
```

### forms.py - User Input
```python
PredictionForm
├── 8 ChoiceFields (dropdowns)
├── 1 IntegerField (speed limit)
├── Bootstrap styling applied to all fields
├── Dynamic choice population from dataset
├── Min/max validation for speed limit
└── __init__() method for dynamic choices
```

### utils.py - Machine Learning
```python
tune_hyperparameters(X, y, param_grid)
├── Grid search for best hyperparameters
└── Returns best parameter dict

get_dataset_choices()
├── Reads dataset
├── Extracts unique values
└── Returns choice dicts for form

get_default_choices()
├── Fallback choices if dataset missing
└── Prevents app crash

balance_dataset(X, y)
├── Oversamples minority classes
├── Returns balanced dataset
└── Logs before/after counts

train_and_save_model()
├── Complete ML training pipeline
├── Saves model and encoders to disk
└── Returns trained model

load_model()
├── Loads model from disk
├── Caches in memory
├── Auto-trains if missing
└── Returns model and encoders

calculate_risk_score(...)
├── Analyzes input conditions
├── Assigns risk points
└── Returns risk (0.0-1.0)

apply_threshold_adjustment(...)
├── Adjusts model probabilities
├── Based on risk score
└── Returns final prediction

predict_accident_severity(...)
├── Main prediction function
├── Maps inputs to features
├── Gets model prediction
├── Adjusts by risk
└── Returns severity + confidence
```

---

## 💾 Data Flow Diagrams

### Request-Response Cycle (Form → Prediction)

```
User clicks "Predict" button on dashboard
              ↓
      predict() view called with POST request
              ↓
    Form validation (8 required fields)
              ↓
    predict_accident_severity(road_type, vehicle_type, ...)
              ↓
         Load XGBoost model
              ↓
      Map user inputs → model features
              ↓
       Encode categorical variables
              ↓
    Get probabilities: [0.15, 0.70, 0.15]
              ↓
    Calculate risk score from conditions
              ↓
    Adjust probabilities based on risk
              ↓
    Return ('High', 0.85) ← final prediction
              ↓
    Save PredictionHistory record to database
              ↓
    Redirect to result page with record ID
              ↓
        result() view renders result.html
              ↓
    User sees prediction + confidence + risk
```

### Data Format Examples

**Form Submission:**
```json
{
  "road_type": "Highway",
  "vehicle_type": "Car",
  "time_of_day": "Night",
  "weather": "Rain",
  "light_condition": "Night",
  "location": "CA",
  "day": "Saturday",
  "speed_limit": 80
}
```

**Model Prediction:**
```json
{
  "severity": "High",
  "confidence": 0.842,
  "risk_score": 6.5
}
```

**Database Record:**
```json
{
  "id": 42,
  "road_type": "Highway",
  "vehicle_type": "Car",
  "prediction_result": "High",
  "confidence_score": 84.2,
  "risk_score": 6.5,
  "created_at": "2025-12-14 10:30:45"
}
```

---

## 🔍 Key Concepts Explained

### Class Imbalance in Accident Data
- Most accidents are Low severity (~70%)
- Fewer are High severity (~20%)
- Very few are Severe (~10%)
- **Solution:** Use class weights + oversampling

### Feature Encoding
- ML models need numbers, not text
- LabelEncoder converts: "Highway" → 0, "Interstate" → 1, etc.
- Encoders saved and reused for predictions

### Risk Score Adjustment
- User inputs indicate scenario risk (0.0 safe → 1.0 dangerous)
- Higher risk boosts high-severity predictions
- Lower risk boosts low-severity predictions
- Makes predictions context-aware

### Confidence Score
- Model outputs probabilities (0-1)
- Confidence = highest probability
- Example: [0.15, 0.70, 0.15] → prediction=class1, confidence=0.70

### XGBoost vs Other Models
- XGBoost: Gradient boosting on decision trees
- Good at handling tabular data
- Fast training and inference
- Handles categorical features well
- Great for production applications

---

## 🚀 Running the Application

### Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/Mac

# Install dependencies
pip install django==5.2.8 xgboost scikit-learn pandas numpy

# Create database
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser
```

### Running
```bash
# Start development server
python manage.py runserver

# Visit http://localhost:8000 in browser
# Admin panel: http://localhost:8000/admin
```

### Training Model (First Time)
```bash
# Model trains automatically when first prediction is made
# Or manually run: python manage.py shell
from predictor.utils import train_and_save_model
train_and_save_model()
```

---

## 🔐 Security Notes

- `DEBUG = True` in settings (CHANGE FOR PRODUCTION)
- Secret key exposed (CHANGE FOR PRODUCTION)
- No CSRF token handling needed for form (Django handles it)
- SQLite only for development (use PostgreSQL for production)
- No authentication needed (open to all users)

---

## 📊 Model Performance

**Training Accuracy:** ~95%  
**Validation Accuracy:** ~88%  
**Precision:** Good for all classes  
**Recall:** Balanced across classes  

**Top Features by Importance:**
1. Speed Limit
2. Number of Casualties
3. Weather Condition
4. Light Condition
5. Hour of Day

---

## 🐛 Debugging Tips

### Check Database
```bash
python manage.py shell
from predictor.models import PredictionHistory
print(PredictionHistory.objects.all())
```

### Check Model Loading
```bash
python manage.py shell
from predictor.utils import load_model
model, encoders = load_model()
print(f"Model loaded: {model}")
```

### Test Prediction
```bash
python test_utils.py
```

### View Logs
```bash
# Django server prints logs to console
# Check terminal where you ran runserver
```

---

## 📚 File Reference

| File | Purpose | Lines | Status |
|------|---------|-------|--------|
| models.py | Database model | 70 | ✅ Documented |
| views.py | URL handlers | 110 | ✅ Documented |
| forms.py | Form definition | 100 | ✅ Documented |
| utils.py | ML utilities | 1300+ | ✅ Heavily Documented |
| urls.py | URL routing | 10 | ✅ Commented |
| admin.py | Admin config | 15 | ✅ Documented |
| settings.py | Django config | 130 | ✅ Documented |
| base.html | Base template | 200 | ✅ Documented |
| predict.html | Form template | 420 | ✅ Documented |
| result.html | Result template | 490 | ✅ Documented |

---

## 🎓 Learning Resources

### Understanding ML Prediction
- Start with: `utils.py` → `calculate_risk_score()` function
- Then: `apply_threshold_adjustment()` function
- Finally: `predict_accident_severity()` function

### Understanding Django
- Start with: `settings.py` → understand configuration
- Then: `urls.py` → understand routing
- Then: `views.py` → understand request handling
- Finally: `models.py` → understand database

### Understanding Data Flow
- Read: views.py → forms.py → models.py (frontend flow)
- Read: utils.py → models.py (ML flow)
- Read: templates → views.py (template flow)

---

## 📝 Code Comments Convention

All code follows this documentation pattern:

```python
"""
MODULE-LEVEL DOCSTRING
=======================

Explains what the module does, why it exists, and what functions it contains.
"""

# ============ SECTION HEADER ============
# Why: Explains the purpose of this section

def function_name(param1, param2):
    """
    FUNCTION DOCSTRING
    
    What: Explains what the function does
    Why: Explains why it's needed
    
    Args:
        param1: What this parameter is
        param2: What this parameter is
        
    Returns:
        What the function returns
    """
    # Inline comment explaining complex logic
    result = param1 + param2
    return result
```

---

## ✅ Checklist for Developers

Before committing code:
- [ ] Added docstring to new functions
- [ ] Added section header comments
- [ ] Followed existing naming conventions
- [ ] Tested changes locally
- [ ] No print() statements (use logging)
- [ ] No hardcoded paths (use settings.py)
- [ ] Documented "Why" not just "What"

---

**Last Updated:** December 14, 2025  
**Maintained By:** Development Team  
**Version:** 1.0.0

For questions or clarifications, refer to inline code comments or this documentation.
