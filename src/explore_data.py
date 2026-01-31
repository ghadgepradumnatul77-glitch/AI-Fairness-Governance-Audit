import pandas as pd
from pathlib import Path

# Get project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Data path
DATA_PATH = BASE_DIR / "data" / "adult.csv"

columns = [
    "age", "workclass", "fnlwgt", "education", "education-num",
    "marital-status", "occupation", "relationship", "race", "sex",
    "capital-gain", "capital-loss", "hours-per-week", "native-country",
    "income"
]

# Load dataset
df = pd.read_csv(
    DATA_PATH,
    header=None,
    names=columns,
    sep=", ",
    engine="python"
)

print("First 5 rows:")
print(df.head())

print("\nDataset Info:")
print(df.info())

print("\nGender distribution:")
print(df["sex"].value_counts())

print("\nIncome distribution:")
print(df["income"].value_counts())

