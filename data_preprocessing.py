"""
Data Preprocessing for AI Governance Project
Creates processed_adult.csv
"""

import pandas as pd
from pathlib import Path

# Column names for Adult dataset
columns = [
    "age", "workclass", "fnlwgt", "education", "education_num",
    "marital_status", "occupation", "relationship", "race", "sex",
    "capital_gain", "capital_loss", "hours_per_week",
    "native_country", "income"
]

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA = BASE_DIR / "data" / "adult.csv"
PROCESSED_DATA = BASE_DIR / "data" / "processed_adult.csv"

# Load raw data
df = pd.read_csv(RAW_DATA, header=None, names=columns)

# Clean columns
df["income"] = df["income"].str.strip()
df["sex"] = df["sex"].str.strip()

# Binary target
df["income_binary"] = df["income"].apply(
    lambda x: 1 if x == ">50K" else 0
)

# Save processed data
df.to_csv(PROCESSED_DATA, index=False)

print("processed_adult.csv created successfully")
