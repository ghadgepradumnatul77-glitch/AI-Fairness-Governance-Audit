import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from datetime import datetime

# ---------------------------
# LOAD DATA
# ---------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "adult.csv"

columns = [
    "age", "workclass", "fnlwgt", "education", "education_num",
    "marital_status", "occupation", "relationship", "race", "sex",
    "capital_gain", "capital_loss", "hours_per_week",
    "native_country", "income"
]

df = pd.read_csv(DATA_PATH, header=None, names=columns)

# Clean data
df["income"] = df["income"].str.strip()
df["sex"] = df["sex"].str.strip()

# Binary target
df["income_binary"] = df["income"].apply(lambda x: 1 if x == ">50K" else 0)

# Encode gender (protected attribute)
df["sex_binary"] = df["sex"].apply(lambda x: 1 if x == "Male" else 0)

# ---------------------------
# FEATURE SELECTION
# ---------------------------
features = ["age", "education_num", "hours_per_week", "sex_binary"]
X = df[features]
y = df["income_binary"]

# ---------------------------
# TRAIN TEST SPLIT
# ---------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# ---------------------------
# TRAIN MODEL (SLM)
# ---------------------------
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# ---------------------------
# PREDICTIONS
# ---------------------------
df_test = X_test.copy()
df_test["actual"] = y_test
df_test["prediction"] = model.predict(X_test)

# ---------------------------
# FAIRNESS METRICS
# ---------------------------
def selection_rate(data, gender_value):
    group = data[data["sex_binary"] == gender_value]
    if len(group) == 0:
        return 0
    return group["prediction"].mean()

female_rate = selection_rate(df_test, 0)
male_rate = selection_rate(df_test, 1)

# Safe division
DIR = female_rate / male_rate if male_rate != 0 else 0

# ---------------------------
# GOVERNANCE REPORT
# ---------------------------
print("\n=== MODEL BIAS GOVERNANCE REPORT (DAY 6) ===")
print("Timestamp:", datetime.now())

print("\nSelection Rates (Predicted >50K):")
print("Female:", round(female_rate, 3))
print("Male  :", round(male_rate, 3))

print("\nDisparate Impact Ratio (Female / Male):", round(DIR, 3))

# 80% Rule
if DIR < 0.8:
    print("\nGOVERNANCE ALERT:")
    print("Model violates the 80% fairness rule.")
    print("Bias mitigation or model review required.")
else:
    print("\nGovernance Status: Model passes fairness threshold.")

print("\nModel Coefficients (Explainability):")
for feature, coef in zip(features, model.coef_[0]):
    print(f"{feature}: {round(coef, 4)}")
