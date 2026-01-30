import pandas as pd
from pathlib import Path
from datetime import datetime

# =====================================
# CONFIGURATION
# =====================================

FAIRNESS_THRESHOLD = 0.8   # 80% rule (industry standard)

# Column names for Adult dataset
COLUMNS = [
    "age", "workclass", "fnlwgt", "education", "education_num",
    "marital_status", "occupation", "relationship", "race", "sex",
    "capital_gain", "capital_loss", "hours_per_week",
    "native_country", "income"
]

# =====================================
# LOAD DATA
# =====================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "adult.csv"

df = pd.read_csv(DATA_PATH, header=None, names=COLUMNS)

# Clean columns
df["income"] = df["income"].str.strip()
df["sex"] = df["sex"].str.strip()

# Binary target
df["income_binary"] = df["income"].apply(lambda x: 1 if x == ">50K" else 0)

# =====================================
# FAIRNESS MONITORING REPORT
# =====================================

print("\n=== FAIRNESS MONITORING REPORT ===")
print("Timestamp:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# -------------------------------------
# Selection Rates by Gender
# -------------------------------------

selection_rates = df.groupby("sex")["income_binary"].mean()

print("\nSelection Rates:")
print(selection_rates)

female_rate = selection_rates.get("Female", 0)
male_rate = selection_rates.get("Male", 0)

# Avoid division by zero
if male_rate > 0:
    disparate_impact = female_rate / male_rate
else:
    disparate_impact = 0

print("\nDisparate Impact Ratio (Female/Male):", round(disparate_impact, 3))

# -------------------------------------
# GOVERNANCE CONTROL CHECK
# -------------------------------------

if disparate_impact < FAIRNESS_THRESHOLD:
    print("\nGOVERNANCE ALERT:")
    print("Fairness threshold violated.")
    print("Disparate Impact Ratio below", FAIRNESS_THRESHOLD)
    print("Potential gender bias detected.")
    print("Action required: Review data, model, or mitigation strategy.")
else:
    print("\nGOVERNANCE STATUS:")
    print("Fairness threshold satisfied.")
    print("No immediate bias risk detected.")

# =====================================
# END OF REPORT
# =====================================
