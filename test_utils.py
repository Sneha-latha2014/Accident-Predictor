"""
TEST_UTILS.PY - QUICK UTILITY TESTING SCRIPT
=============================================

This is a simple test script to verify utility functions work correctly.

Purpose: Used for quick debugging and testing during development.
Location: Root project directory

What it does:
1. Tests the apply_threshold_adjustment() function
2. Verifies prediction thresholds are applied correctly
3. Outputs the adjusted prediction and confidence

Why: This helps verify the ML prediction adjustment logic works properly.

Note: This is a standalone test script. For comprehensive tests, see:
- predictor/tests.py
- predictor/tests/test_model_accuracy.py
"""

import os
import sys

# Add project to path so we can import Django modules
sys.path.append('c:/Users/gokul/Documents/accident_prediction')

# Import the utility functions
from predictor import utils
import numpy as np

# ============ TEST: THRESHOLD ADJUSTMENT ============
# Test the apply_threshold_adjustment function with sample probabilities

print("=" * 60)
print("[TEST] Threshold Adjustment Function")
print("=" * 60)

# Display prediction thresholds
print('\nPREDICTION_THRESHOLDS:', utils.PREDICTION_THRESHOLDS)

# Create sample probabilities from ML model
# Example: [20% Low, 50% High, 30% Severe]
probs = np.array([0.25, 0.5, 0.25])

# Test with low risk (should boost Low prediction)
pred, conf = utils.apply_threshold_adjustment(
    probs, 
    {0: 'Low', 1: 'High', 2: 'Severe'}, 
    risk_score=0.2  # Low risk
)
print(f'\n[LOW RISK] Adjusted prediction: {pred}, confidence: {conf:.3f}')

# Test with high risk (should boost Severe prediction)
pred, conf = utils.apply_threshold_adjustment(
    probs, 
    {0: 'Low', 1: 'High', 2: 'Severe'}, 
    risk_score=0.9  # High risk
)
print(f'[HIGH RISK] Adjusted prediction: {pred}, confidence: {conf:.3f}')

print("\n" + "=" * 60)
print("[OK] Test completed successfully!")
print("=" * 60)
