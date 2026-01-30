import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# -----------------------------
# PROJECT PATHS
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "adult.csv"

# -----------------------------
# COLUMN NAMES (Adult Dataset)
# -----------------------------
columns = [
    "age", "workclass", "fnlwgt", "education", "education_num",
    "marital_status", "occupation", "relationship", "race", "sex",
    "capital_gain", "capital_loss", "hours_per_week",
    "native_country", "income"
]

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv(DATA_PATH, header=None, names=columns)

# Clean columns
df["income"] = df["income"].str.strip()
df["sex"] = df["sex"].str.strip()
df["race"] = df["race"].str.strip()

# Binary target
df["income_binary"] = df["income"].apply(lambda x: 1 if x == ">50K" else 0)

print("Dataset loaded successfully")

# -----------------------------
# FEATURES & TARGET
# -----------------------------
features = ["age", "education_num", "hours_per_week", "capital_gain", "capital_loss"]
X = df[features]
y = df["income_binary"]

# -----------------------------
# TRAIN MODEL
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# -----------------------------
# PREDICTIONS
# -----------------------------
df_test = df.loc[X_test.index].copy()
df_test["prediction"] = model.predict(X_test)

print("\nPredictions generated")

# -----------------------------
# PREDICTION SELECTION RATES
# -----------------------------
prediction_rates = df_test.groupby("sex")["prediction"].mean()

print("\nPrediction Selection Rates (P(predicted >50K | gender)):")
print(prediction_rates)

# -----------------------------
# DISPARATE IMPACT (SAFE)
# -----------------------------
female_rate = prediction_rates.get("Female", 0)
male_rate = prediction_rates.get("Male", 1)

dir_prediction = female_rate / male_rate if male_rate != 0 else 0

print("\nDisparate Impact Ratio (Predictions - Female/Male):")
print(round(dir_prediction, 3))

# -----------------------------
# INTERSECTIONAL PREDICTION BIAS
# -----------------------------
df_test["intersection_group"] = df_test["sex"] + "_" + df_test["race"]

intersection_rates = (
    df_test.groupby("intersection_group")["prediction"]
    .mean()
    .sort_values()
)

print("\nIntersectional Prediction Selection Rates:")
print(intersection_rates)

# -----------------------------
# GOVERNANCE CHECK (80% RULE)
# -----------------------------
print("\nGovernance Assessment:")

if dir_prediction < 0.8:
    print("ALERT: Disparate Impact below 0.8 threshold")
    print("Action Required: Bias mitigation or policy review")
else:
    print("PASS: Prediction fairness within acceptable limits")
