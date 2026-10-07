"""
app.py
======
Flask backend for the AI Health Risk Prediction System.

Routes:
  GET  /           → Home page
  GET  /assessment → Health assessment form
  POST /predict    → Process form + return prediction
  GET  /about      → About the project page
"""

from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import pandas as pd
import os
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

app = Flask(__name__)

# ─────────────────────────────────────────────
# Load model, scaler, and metrics at startup
# ─────────────────────────────────────────────
def load_artifacts():
    """Load model.pkl, scaler.pkl, and metrics.pkl from disk."""
    if not os.path.exists("model.pkl"):
        raise FileNotFoundError(
            "model.pkl not found. Please run:  python train_model.py"
        )
    with open("model.pkl",  "rb") as f: model   = pickle.load(f)
    with open("scaler.pkl", "rb") as f: scaler  = pickle.load(f)
    with open("metrics.pkl","rb") as f: metrics = pickle.load(f)
    return model, scaler, metrics

try:
    MODEL, SCALER, METRICS = load_artifacts()
    print("[OK] Model loaded successfully.")
except FileNotFoundError as e:
    print(f"[WARNING] {e}")
    MODEL, SCALER, METRICS = None, None, {}

# ─────────────────────────────────────────────
# Helper: map probability to risk level
# ─────────────────────────────────────────────
def get_risk_level(prob):
    """
    prob: probability of being at risk (float 0-1)
    Returns: (risk_label, risk_class, risk_color)
    """
    if prob < 0.35:
        return "Low Risk", "low",    "#28a745"
    elif prob < 0.65:
        return "Medium Risk", "medium", "#ffc107"
    else:
        return "High Risk", "high",  "#dc3545"

# ─────────────────────────────────────────────
# Helper: BMI category
# ─────────────────────────────────────────────
def bmi_category(bmi):
    if bmi < 18.5: return "Underweight"
    elif bmi < 25: return "Normal"
    elif bmi < 30: return "Overweight"
    else:          return "Obese"

# ─────────────────────────────────────────────
# Helper: Build health recommendations
# ─────────────────────────────────────────────
def get_recommendations(data, risk_class):
    tips = []

    if data['bmi'] >= 25:
        tips.append("🏃 Maintain a healthy weight through regular physical activity and a balanced diet.")
    if data['blood_pressure'] >= 130:
        tips.append("💊 Your blood pressure appears elevated. Reduce salt intake and manage stress.")
    if data['glucose'] >= 126:
        tips.append("🍎 Blood glucose is high. Limit sugary foods and consult a doctor for diabetes screening.")
    if data['cholesterol'] >= 240:
        tips.append("🥗 High cholesterol detected. Eat more fibre, reduce saturated fats.")
    if data['smoking'] == 1:
        tips.append("🚭 Smoking significantly increases cardiovascular and cancer risk. Consider quitting.")
    if data['activity'] <= 1:
        tips.append("🚶 Aim for at least 150 minutes of moderate exercise per week.")
    if data['family_history'] == 1:
        tips.append("🧬 You have a family history of disease. Regular health screenings are important.")
    if data['heart_rate'] > 100:
        tips.append("❤️ Resting heart rate is high. Stress reduction and aerobic exercise can help.")

    # Always add a general tip
    if risk_class == "high":
        tips.append("⚠️ Please consult a qualified healthcare professional as soon as possible.")
    elif risk_class == "medium":
        tips.append("📋 Consider scheduling a routine health check-up with your doctor.")
    else:
        tips.append("✅ Keep up the healthy lifestyle! Regular check-ups are still recommended.")

    return tips if tips else ["Maintain a balanced diet and active lifestyle."]

# ─────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────

@app.route("/")
def home():
    """Home page."""
    return render_template("index.html")


@app.route("/assessment")
def assessment():
    """Health assessment form page."""
    return render_template("assessment.html")


@app.route("/predict", methods=["POST"])
def predict():
    """
    Receive form data, run ML prediction, return result page.
    Expected form fields (all numeric after parsing):
        age, gender, height, weight, blood_pressure, glucose,
        cholesterol, heart_rate, smoking, activity, family_history
    """
    if MODEL is None:
        return render_template(
            "result.html",
            error="Model not trained yet. Please run: python train_model.py"
        )

    try:
        # --- Parse inputs ---
        age           = int(request.form['age'])
        gender        = int(request.form['gender'])          # 0=Female, 1=Male
        height        = float(request.form['height'])        # cm
        weight        = float(request.form['weight'])        # kg
        blood_pressure= float(request.form['blood_pressure'])
        glucose       = float(request.form['glucose'])
        cholesterol   = float(request.form['cholesterol'])
        heart_rate    = int(request.form['heart_rate'])
        smoking       = int(request.form['smoking'])         # 0/1
        activity      = int(request.form['activity'])        # 0-3
        family_history= int(request.form['family_history'])  # 0/1

        # --- Calculate BMI ---
        height_m = height / 100
        bmi      = round(weight / (height_m ** 2), 2)
        bmi_cat  = bmi_category(bmi)

        # --- Build feature vector (same order as training) ---
        FEATURE_NAMES = ['age', 'gender', 'bmi', 'blood_pressure', 'glucose',
                         'cholesterol', 'heart_rate', 'smoking', 'activity', 'family_history']
        features = pd.DataFrame([[age, gender, bmi, blood_pressure, glucose,
                                   cholesterol, heart_rate, smoking, activity, family_history]],
                                 columns=FEATURE_NAMES)

        # --- Scale features ---
        features_scaled = SCALER.transform(features)

        # --- Predict ---
        prob_array  = MODEL.predict_proba(features_scaled)[0]  # [P(low), P(high)]
        risk_prob   = round(float(prob_array[1]) * 100, 1)     # % probability of risk
        risk_label, risk_class, risk_color = get_risk_level(prob_array[1])

        # --- Recommendations ---
        input_data = {
            'bmi': bmi, 'blood_pressure': blood_pressure,
            'glucose': glucose, 'cholesterol': cholesterol,
            'smoking': smoking, 'activity': activity,
            'family_history': family_history, 'heart_rate': heart_rate
        }
        recommendations = get_recommendations(input_data, risk_class)

        # --- Prepare display data ---
        result = {
            # Prediction
            "risk_label":   risk_label,
            "risk_class":   risk_class,
            "risk_color":   risk_color,
            "risk_prob":    risk_prob,
            "low_prob":     round(float(prob_array[0]) * 100, 1),

            # User inputs (for display)
            "age":            age,
            "gender":         "Male" if gender == 1 else "Female",
            "height":         height,
            "weight":         weight,
            "bmi":            bmi,
            "bmi_category":   bmi_cat,
            "blood_pressure": blood_pressure,
            "glucose":        glucose,
            "cholesterol":    cholesterol,
            "heart_rate":     heart_rate,
            "smoking":        "Yes" if smoking == 1 else "No",
            "activity_label": ["Sedentary", "Light", "Moderate", "Active"][activity],
            "family_history": "Yes" if family_history == 1 else "No",

            # Recommendations
            "recommendations": recommendations,

            # Model metrics (for About/Results section)
            "metrics": METRICS
        }

        return render_template("result.html", **result)

    except Exception as e:
        return render_template("result.html", error=f"Error processing input: {str(e)}")


@app.route("/about")
def about():
    """About the project page."""
    metrics = METRICS if METRICS else {}
    return render_template("about.html", metrics=metrics)


# ─────────────────────────────────────────────
# Run the app
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)
