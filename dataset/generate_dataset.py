# generate_dataset.py
# Run this script ONCE to create health_data.csv
# It generates 1500 synthetic but realistic health records
# Based on patterns from the UCI Heart Disease / Pima Diabetes datasets

import numpy as np
import pandas as pd

np.random.seed(42)
N = 1500  # number of records

age         = np.random.randint(20, 80, N)
gender      = np.random.randint(0, 2, N)          # 0=Female, 1=Male
height_cm   = np.random.normal(165, 10, N).clip(140, 200)
weight_kg   = np.random.normal(70, 15, N).clip(35, 150)
bmi         = weight_kg / ((height_cm / 100) ** 2)

# Systolic blood pressure (mmHg)
bp          = np.random.normal(120, 20, N).clip(80, 200)
# Fasting blood glucose (mg/dL)
glucose     = np.random.normal(100, 30, N).clip(60, 300)
# Cholesterol (mg/dL)
cholesterol = np.random.normal(200, 40, N).clip(100, 400)
# Resting heart rate (bpm)
heart_rate  = np.random.normal(75, 12, N).clip(45, 130)

# 0=Non-smoker, 1=Smoker
smoking     = np.random.randint(0, 2, N)
# 0=Sedentary, 1=Light, 2=Moderate, 3=Active
activity    = np.random.randint(0, 4, N)
# 0=No, 1=Yes
family_hist = np.random.randint(0, 2, N)

# ------------------------------------------------------------------
# Build a realistic risk score that drives the target label
# High BMI, high BP, high glucose, old age, smoking → higher risk
# ------------------------------------------------------------------
risk_score = (
    0.04  * (age - 20) +
    0.05  * (bmi - 18) +
    0.03  * (bp - 80) +
    0.04  * (glucose - 60) +
    0.015 * (cholesterol - 100) +
    0.02  * (heart_rate - 45) +
    0.8   * smoking +
    -0.5  * activity +
    1.0   * family_hist +
    np.random.normal(0, 1.5, N)     # add noise
)

# Normalise to [0, 1] using sigmoid — centre on 0 so ~50% class balance
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Standardise risk_score to zero-mean before applying sigmoid
risk_score_std = (risk_score - risk_score.mean()) / risk_score.std()
prob = sigmoid(risk_score_std)
target = (prob > 0.5).astype(int)  # 1 = at risk, 0 = not at risk

df = pd.DataFrame({
    'age':         age.astype(int),
    'gender':      gender,
    'height':      np.round(height_cm, 1),
    'weight':      np.round(weight_kg, 1),
    'bmi':         np.round(bmi, 2),
    'blood_pressure': np.round(bp, 1),
    'glucose':     np.round(glucose, 1),
    'cholesterol': np.round(cholesterol, 1),
    'heart_rate':  heart_rate.astype(int),
    'smoking':     smoking,
    'activity':    activity,
    'family_history': family_hist,
    'risk':        target          # 0 = Low Risk, 1 = High Risk
})

df.to_csv('health_data.csv', index=False)
print(f"Dataset created: {len(df)} rows")
print(df['risk'].value_counts())
print(df.head())
