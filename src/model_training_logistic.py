"""
DAY 7: Model Training using Logistic Regression
Project: Applied AI Governance & Fairness Audit
"""

import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# -----------------------------
# PROJECT ROOT & DATA PATH
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "processed_adult.csv"

# -----------------------------
# LOAD DATA
# -----------------------------
data = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully")
print("Columns:", data.columns.tolist())

# -----------------------------
# FEATURE SELECTION
# (Simple + interpretable features)
# -----------------------------
features = [
    "age",
    "education_num",
    "hours_per_week",
    "capital_gain",
    "capital_loss"
]

target = "income_binary"

X = data[features]
y = data[target]

# -----------------------------
# TRAIN–TEST SPLIT
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42,
    stratify=y
)

# -----------------------------
# TRAIN LOGISTIC REGRESSION
# Governance-friendly model
# -----------------------------
model = LogisticRegression(
    max_iter=1000,
    solver="liblinear"
)

model.fit(X_train, y_train)

print("\nModel training completed")

# -----------------------------
# MODEL EVALUATION
# -----------------------------
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:", round(accuracy, 3))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# -----------------------------
# MODEL INTERPRETABILITY
# -----------------------------
coefficients = pd.DataFrame({
    "Feature": features,
    "Coefficient": model.coef_[0]
}).sort_values(by="Coefficient", ascending=False)

print("\nModel Coefficients (Interpretability):")
print(coefficients)

# -----------------------------
# GOVERNANCE NOTE
# -----------------------------
print("\nGovernance Note:")
print("Logistic Regression is used due to its transparency,")
print("interpretability, and suitability for fairness audits.")
