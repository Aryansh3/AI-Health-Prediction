# 🏥 AI Health Risk Prediction System
### Aligned with UN SDG 3 — Good Health & Well-Being

link - https://ai-health-prediction-5hmv.onrender.com

> **Disclaimer:** This project is for **educational and awareness purposes only**.  
> It does not provide medical diagnosis or replace professional medical advice.

---

## 📌 Project Overview

This is a beginner-friendly web application that uses a **machine learning model** to estimate a user's risk of developing common health conditions based on basic health inputs.

Built with **Python + Flask** (backend) and **HTML/CSS/JS** (frontend).

---

## 🗂️ Project Structure

```
AI-Health-Risk-Prediction/
├── app.py                  ← Flask web application (backend)
├── train_model.py          ← ML training script (run once)
├── model.pkl               ← Saved trained model (auto-generated)
├── scaler.pkl              ← Saved feature scaler (auto-generated)
├── metrics.pkl             ← Model performance metrics (auto-generated)
├── requirements.txt        ← Python dependencies
│
├── dataset/
│   ├── generate_dataset.py ← Generates health_data.csv
│   └── health_data.csv     ← Dataset (auto-generated)
│
├── templates/
│   ├── index.html          ← Home page
│   ├── assessment.html     ← Health input form
│   ├── result.html         ← Prediction result dashboard
│   └── about.html          ← About the project
│
├── static/
│   ├── css/style.css       ← All styles
│   └── js/script.js        ← BMI calculator + form validation
│
└── README.md
```

---

## ⚡ How to Run (Step-by-Step for Windows)

### Step 1 — Open Command Prompt / PowerShell

Navigate to the project folder:
```
cd path\to\AI-Health-Risk-Prediction
```

### Step 2 — Create a Virtual Environment (Recommended)
```
python -m venv venv
venv\Scripts\activate
```

### Step 3 — Install Dependencies
```
pip install -r requirements.txt
```

### Step 4 — Train the ML Model (Run Once)
```
python train_model.py
```
This will:
- Generate `dataset/health_data.csv` (1500 records)
- Train Logistic Regression, Decision Tree, Random Forest
- Save the best model as `model.pkl`, `scaler.pkl`, `metrics.pkl`
- Save confusion matrix to `static/confusion_matrix.png`

### Step 5 — Start the Web App
```
python app.py
```

### Step 6 — Open in Browser
```
http://127.0.0.1:5000
```

---

## 🤖 Machine Learning — Simple Explanation for Viva

| Question | Answer |
|----------|--------|
| **What is the model doing?** | Learning patterns from health data to predict who is at risk |
| **What algorithm is used?** | Logistic Regression (primary) + Decision Tree + Random Forest |
| **What is the output?** | Probability of health risk (0–1 scale) |
| **How is risk classified?** | < 35% = Low Risk, 35–65% = Medium, > 65% = High Risk |
| **What is Logistic Regression?** | A model that outputs a probability using a mathematical S-curve (sigmoid function) |
| **Why scale the data?** | So that large-valued features (like glucose = 300) don't dominate small ones (like age = 25) |
| **What is the train/test split?** | 80% data used for training, 20% held back for testing accuracy |

---

## 📊 Model Features Used

| Feature | Description |
|---------|-------------|
| age | Patient age |
| gender | 0 = Female, 1 = Male |
| bmi | Calculated from height and weight |
| blood_pressure | Systolic BP (mmHg) |
| glucose | Fasting blood glucose (mg/dL) |
| cholesterol | Total cholesterol (mg/dL) |
| heart_rate | Resting heart rate (bpm) |
| smoking | 0 = Non-smoker, 1 = Smoker |
| activity | 0=Sedentary, 1=Light, 2=Moderate, 3=Active |
| family_history | 0 = No, 1 = Yes |

---

## 🌍 Connection to SDG 3

**SDG 3 — Good Health and Well-Being** aims to ensure healthy lives for all.

This project supports SDG 3 by:
- ✅ Raising health awareness
- ✅ Encouraging preventive healthcare
- ✅ Demonstrating how AI can support health literacy

---

## 🛠️ Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, CSS3, JavaScript |
| Charts | Chart.js (CDN) |
| Backend | Python 3, Flask |
| ML Library | Scikit-learn |
| Data | Pandas, NumPy |
| Visualisation | Matplotlib, Seaborn |

---

## ⚠️ Medical Disclaimer

> This system is developed for **educational and awareness purposes only**.  
> It does **not** provide medical diagnosis or replace professional medical advice.  
> **Please consult a qualified healthcare professional for any medical concerns.**
