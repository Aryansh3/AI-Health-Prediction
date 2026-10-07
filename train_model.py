"""
train_model.py
==============
This script:
  1. Generates the dataset (if not already present)
  2. Trains three ML models: Logistic Regression, Decision Tree, Random Forest
  3. Compares their accuracy and picks the best one
  4. Saves the best model + scaler to disk as model.pkl and scaler.pkl

Run this ONCE before starting the Flask app:
    python train_model.py
"""

import os
import sys
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, classification_report
)

# ─────────────────────────────────────────────
# Step 1: Generate dataset if it doesn't exist
# ─────────────────────────────────────────────
DATASET_PATH = os.path.join("dataset", "health_data.csv")

if not os.path.exists(DATASET_PATH):
    print("Dataset not found. Generating synthetic dataset...")
    # Run the generator script
    exec(open(os.path.join("dataset", "generate_dataset.py")).read())
    # Move the generated file
    if os.path.exists("health_data.csv"):
        os.rename("health_data.csv", DATASET_PATH)
    print(f"Dataset saved to {DATASET_PATH}\n")
else:
    print(f"Dataset found: {DATASET_PATH}\n")

# ─────────────────────────────────────────────
# Step 2: Load and prepare the data
# ─────────────────────────────────────────────
df = pd.read_csv(DATASET_PATH)
print("Dataset shape:", df.shape)
print("Risk distribution:\n", df['risk'].value_counts(), "\n")

# Features used for prediction
FEATURES = ['age', 'gender', 'bmi', 'blood_pressure', 'glucose',
            'cholesterol', 'heart_rate', 'smoking', 'activity', 'family_history']

X = df[FEATURES]
y = df['risk']

# ─────────────────────────────────────────────
# Step 3: Train / Test Split (80% / 20%)
# ─────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ─────────────────────────────────────────────
# Step 4: Scale features (important for Logistic Regression)
# ─────────────────────────────────────────────
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

# ─────────────────────────────────────────────
# Step 5: Define the three models
# ─────────────────────────────────────────────
models = {
    "Logistic Regression": LogisticRegression(max_iter=200, random_state=42),
    "Decision Tree":       DecisionTreeClassifier(max_depth=5, random_state=42),
    "Random Forest":       RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
}

results = {}  # store metrics for each model

print("=" * 55)
print("  MODEL COMPARISON")
print("=" * 55)

for name, model in models.items():
    # Logistic Regression needs scaled data; trees work fine with raw data too
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)

    acc  = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec  = recall_score(y_test, y_pred, zero_division=0)
    f1   = f1_score(y_test, y_pred, zero_division=0)

    results[name] = {
        "model":     model,
        "accuracy":  acc,
        "precision": prec,
        "recall":    rec,
        "f1":        f1
    }

    print(f"\n{name}")
    print(f"  Accuracy : {acc:.4f}")
    print(f"  Precision: {prec:.4f}")
    print(f"  Recall   : {rec:.4f}")
    print(f"  F1-Score : {f1:.4f}")

# ─────────────────────────────────────────────
# Step 6: Pick the best model by F1-score
# ─────────────────────────────────────────────
best_name = max(results, key=lambda k: results[k]['f1'])
best_model = results[best_name]['model']

print("\n" + "=" * 55)
print(f"  BEST MODEL: {best_name}")
print("=" * 55 + "\n")

# ─────────────────────────────────────────────
# Step 7: Full evaluation report for the best model
# ─────────────────────────────────────────────
y_pred_best = best_model.predict(X_test_scaled)
print("Classification Report:\n")
print(classification_report(y_test, y_pred_best, target_names=["Low Risk", "High Risk"]))

# Confusion matrix plot
cm = confusion_matrix(y_test, y_pred_best)
plt.figure(figsize=(5, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=["Low Risk", "High Risk"],
            yticklabels=["Low Risk", "High Risk"])
plt.title(f"Confusion Matrix — {best_name}")
plt.ylabel("Actual")
plt.xlabel("Predicted")
plt.tight_layout()
plt.savefig(os.path.join("static", "confusion_matrix.png"))
plt.close()
print("Confusion matrix saved to static/confusion_matrix.png")

# ─────────────────────────────────────────────
# Step 8: Save model, scaler, and metrics
# ─────────────────────────────────────────────
with open("model.pkl", "wb") as f:
    pickle.dump(best_model, f)

with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

# Save metrics as a JSON-like dict for the Flask app to display
metrics = {
    "best_model":  best_name,
    "accuracy":    round(results[best_name]['accuracy']  * 100, 2),
    "precision":   round(results[best_name]['precision'] * 100, 2),
    "recall":      round(results[best_name]['recall']    * 100, 2),
    "f1":          round(results[best_name]['f1']        * 100, 2),
    "all_models":  {k: {"accuracy":  round(v['accuracy']  * 100, 2),
                        "precision": round(v['precision'] * 100, 2),
                        "recall":    round(v['recall']    * 100, 2),
                        "f1":        round(v['f1']        * 100, 2)}
                    for k, v in results.items()},
    "features":    FEATURES
}

with open("metrics.pkl", "wb") as f:
    pickle.dump(metrics, f)

print("\nFiles saved: model.pkl, scaler.pkl, metrics.pkl")
print("\nTraining complete! You can now run:  python app.py")
