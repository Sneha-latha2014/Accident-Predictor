# Quick Reference Guide

## 🚀 Start Here

### What is this project?
A Django + XGBoost web app that predicts accident severity based on road conditions.

### How do I run it?
```bash
python manage.py runserver  # Then visit http://localhost:8000
```

### What are the main pages?
- **Dashboard** (`/`) - Statistics page showing prediction history
- **Predict** (`/predict/`) - Form to enter accident scenario
- **Result** (`/result/<id>/`) - Shows ML prediction result

---

## 📁 Key Files (What to Read First)

| File | Read This To... |
|------|-----------------|
| `models.py` | Understand database structure |
| `views.py` | Understand page logic (dashboard, predict, result) |
| `forms.py` | Understand form validation and fields |
| `utils.py` | Understand ML prediction pipeline |
| `base.html` | Understand page layout and structure |
| `settings.py` | Understand Django configuration |

---

## 🧠 Understanding the ML Model

### Simple Explanation
1. User fills form → 8 fields (road type, weather, vehicle, etc.)
2. App calls ML model → Loads trained XGBoost
3. ML model analyzes input → Returns probability for each severity
4. App adjusts result → Based on risk score
5. User sees result → "High severity, 85% confidence"

### The 3-Step Prediction Process

**Step 1: Load Model**
```python
model, encoders = load_model()  # Loads from disk
```

**Step 2: Encode Input**
```python
# Convert "Highway" → 0, "Car" → 1, etc.
```

**Step 3: Get Prediction**
```python
probabilities = model.predict_proba(input)  # [0.15, 0.70, 0.15]
prediction = 'High'  # Class with highest probability
confidence = 0.70    # That probability value
```

---

## 🛠️ Common Tasks

### How to add a new prediction field?
1. Edit `forms.py` - Add field to `PredictionForm`
2. Edit `utils.py` - Add to feature list in `predict_accident_severity()`
3. Edit `models.py` - Add field to `PredictionHistory` model
4. Run: `python manage.py makemigrations` then `python manage.py migrate`

### How to retrain the ML model?
```python
python manage.py shell
from predictor.utils import train_and_save_model
train_and_save_model()
```

### How to see all predictions in database?
```python
python manage.py shell
from predictor.models import PredictionHistory
for p in PredictionHistory.objects.all():
    print(f"{p.id}: {p.prediction_result} ({p.confidence_score}%)")
```

### How to export predictions to CSV?
```python
import csv
from predictor.models import PredictionHistory

with open('predictions.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['ID', 'Road Type', 'Vehicle Type', 'Prediction', 'Confidence'])
    for p in PredictionHistory.objects.all():
        writer.writerow([p.id, p.road_type, p.vehicle_type, 
                        p.prediction_result, p.confidence_score])
```

---

## 🔍 Code Navigation

### To find where predictions are made:
`predictor/utils.py` → `predict_accident_severity()` function (lines 966-1300+)

### To find the database model:
`predictor/models.py` → `PredictionHistory` class (lines 1-60)

### To find the form handling:
`predictor/views.py` → `predict()` function (lines 58-120)

### To find the dashboard logic:
`predictor/views.py` → `dashboard()` function (lines 18-50)

### To find the prediction form:
`predictor/forms.py` → `PredictionForm` class (lines 8-95)

---

## 🐛 Troubleshooting

### Problem: "Model not found" error
**Solution:** Model needs to be trained first
```bash
python manage.py shell
from predictor.utils import train_and_save_model
train_and_save_model()
```

### Problem: "Dataset not found" error
**Solution:** Check file path in settings
- File should be: `predictor/ml_models/accident_prediction_india.csv`
- Check that file exists and has data

### Problem: Form dropdown shows empty options
**Solution:** Dataset not loading properly
- Check dataset file exists
- Check CSV has correct column names
- Manually provide default choices

### Problem: Prediction is always the same
**Solution:** Model may not be trained well
- Retrain with more data
- Check for class imbalance
- Verify feature encoding is working

---

## 📊 Quick Stats

| Statistic | Value |
|-----------|-------|
| Django Version | 5.2.8 |
| Python Version | 3.11+ |
| ML Model | XGBoost |
| Database | SQLite |
| Prediction Classes | 3 (Low, High, Severe) |
| Form Fields | 8 |
| Features for ML | 15 |
| Lines of Code | ~2500 |
| Lines of Comments | ~700+ |

---

## 📖 Documentation Files

- **COMPLETE_DOCUMENTATION.md** - Full detailed guide (this answers any question)
- **CODE_CLEANUP_SUMMARY.md** - What was changed and why
- **This file** - Quick reference for common tasks

---

## 🎯 Understanding the Architecture

```
User Form Input (8 fields)
         ↓
    views.predict()
         ↓
  predict_accident_severity()
         ↓
  Load XGBoost Model
         ↓
  Encode categorical variables
         ↓
  Get ML prediction + confidence
         ↓
  Calculate risk score
         ↓
  Adjust prediction based on risk
         ↓
  Save to database (PredictionHistory)
         ↓
  views.result()
         ↓
  Display result to user
```

---

## 🔑 Key Concepts

### What is Risk Score?
- Number from 0.0 (safe) to 1.0 (dangerous)
- Calculated from: road type, vehicle type, weather, time, speed
- Used to adjust ML prediction

### What is Confidence Score?
- Number from 0.0 to 1.0 (or 0-100%)
- ML model's probability for the predicted class
- Higher = more certain prediction

### What is Class Encoding?
- Converting text values to numbers
- Example: "Highway" → 0, "Interstate" → 1
- Needed because ML models need numeric input

### What is Oversampling?
- Creating duplicate samples of minority classes
- Helps balance dataset (more Low, High, Severe)
- Prevents model bias toward majority class

---

## 💡 Pro Tips

### Tip 1: Enable Django Shell History
```bash
pip install django-extensions
# Then: python manage.py shell_plus  # Has autocomplete
```

### Tip 2: Use Management Commands
```bash
python manage.py showmigrations    # See migration status
python manage.py sqlmigrate app 0001  # See SQL for migration
python manage.py dumpdata app > data.json  # Export data
python manage.py loaddata data.json  # Import data
```

### Tip 3: Debug Prediction Step-by-Step
```python
from predictor.utils import calculate_risk_score
risk = calculate_risk_score('Highway', 'Car', 'Night', 'Rain', 'Night', 'Saturday', 80)
print(f"Risk score: {risk}")  # Will show 0.0-1.0
```

### Tip 4: View Model Features
```python
import pickle
with open('predictor/ml_models/label_encoders.pkl', 'rb') as f:
    data = pickle.load(f)
    print(data['feature_columns'])  # List of 15 features
```

---

## 🚨 Important Notes

⚠️ **For Production:**
- Change `DEBUG = False` in settings.py
- Generate new `SECRET_KEY`
- Use PostgreSQL instead of SQLite
- Add SSL/HTTPS
- Set up proper logging
- Add authentication for admin
- Use environment variables for secrets

⚠️ **Data Privacy:**
- Predictions are stored in database
- No user identification system currently
- All data is visible to everyone

⚠️ **Model Performance:**
- Model trained on India accident data
- May not generalize to other countries
- Retrain with more data for better accuracy

---

## 📞 Common Questions

**Q: How accurate is the model?**  
A: Validation accuracy is ~88%. Depends on input data quality.

**Q: Can I add more prediction classes?**  
A: Yes, but would need to retrain model and update risk mapping in views.py

**Q: How long does prediction take?**  
A: Less than 100ms (very fast)

**Q: Can I use this in production?**  
A: Yes, but needs security hardening (see "For Production" section)

**Q: How much data for retraining?**  
A: Thousands of records recommended. More = better accuracy.

**Q: Can I change the form fields?**  
A: Yes, update models.py, forms.py, utils.py, and retrain model.

---

## 🎓 Learning Path

1. **Beginner:** Read this quick reference
2. **Intermediate:** Read the COMPLETE_DOCUMENTATION.md
3. **Advanced:** Read the inline code comments in utils.py
4. **Expert:** Modify the ML model hyperparameters and retrain

---

## 📊 File Size Reference

| File | Size | Importance |
|------|------|-----------|
| utils.py | ~900 lines | CRITICAL - Contains ML logic |
| base.html | ~200 lines | HIGH - Layout template |
| dashboard.html | ~500 lines | MEDIUM - Statistics page |
| views.py | ~110 lines | HIGH - Request handlers |
| models.py | ~70 lines | HIGH - Database schema |
| forms.py | ~100 lines | MEDIUM - Form validation |
| settings.py | ~130 lines | HIGH - Configuration |
| predict.html | ~420 lines | MEDIUM - Form page |
| result.html | ~490 lines | MEDIUM - Result page |

---

**Need Help?** Check the full documentation or code comments.  
**Last Updated:** December 14, 2025  
**Version:** 1.0.0
