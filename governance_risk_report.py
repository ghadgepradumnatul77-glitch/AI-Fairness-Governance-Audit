import pandas as pd
from pathlib import Path
from datetime import datetime

# -----------------------------
# LOAD DATA
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "adult.csv"

columns = [
    "age", "workclass", "fnlwgt", "education", "education_num",
    "marital_status", "occupation", "relationship", "race", "sex",
    "capital_gain", "capital_loss", "hours_per_week",
    "native_country", "income"
]

df = pd.read_csv(DATA_PATH, header=None, names=columns)

# Clean columns
df["income"] = df["income"].str.strip()
df["sex"] = df["sex"].str.strip()

# Binary target
df["income_binary"] = df["income"].apply(lambda x: 1 if x == ">50K" else 0)

print("Dataset loaded successfully")

# -----------------------------
# FAIRNESS METRICS
# -----------------------------
selection_rates = df.groupby("sex")["income_binary"].mean()

female_rate = selection_rates.get("Female", 0)
male_rate = selection_rates.get("Male", 1)

dir_gender = female_rate / male_rate if male_rate != 0 else 0

# -----------------------------
# RISK SCORING LOGIC
# -----------------------------
if dir_gender < 0.6:
    risk_level = "HIGH"
elif dir_gender < 0.8:
    risk_level = "MEDIUM"
else:
    risk_level = "LOW"

# -----------------------------
# GOVERNANCE REPORT
# -----------------------------
print("\n=== AI GOVERNANCE RISK REPORT ===")
print("Timestamp:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

print("\nSelection Rates:")
print(selection_rates)

print("\nDisparate Impact Ratio (Female / Male):")
print(round(dir_gender, 3))

print("\nFairness Risk Level:", risk_level)

print("\nGovernance Interpretation:")
if risk_level == "HIGH":
    print("- Significant gender bias detected")
    print("- Immediate mitigation recommended")
elif risk_level == "MEDIUM":
    print("- Potential bias detected")
    print("- Monitoring and mitigation advised")
else:
    print("- Fairness within acceptable limits")

print("\nAudit Notes:")
print("- Metrics align with 80 percent fairness rule")
print("- Results suitable for compliance documentation")
print("- Supports internal and external audit review")
