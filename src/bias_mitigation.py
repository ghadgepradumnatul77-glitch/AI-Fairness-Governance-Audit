import pandas as pd

# ---------------------------
# COLUMN NAMES (OFFICIAL ADULT DATASET SCHEMA)
# ---------------------------
columns = [
    "age", "workclass", "fnlwgt", "education", "education_num",
    "marital_status", "occupation", "relationship", "race", "sex",
    "capital_gain", "capital_loss", "hours_per_week",
    "native_country", "income"
]

# ---------------------------
# LOAD DATASET (NO HEADER IN CSV)
# ---------------------------
df = pd.read_csv("data/adult.csv", header=None, names=columns)

print("Dataset loaded successfully")
print("\nColumns in dataset:")
print(df.columns.tolist())

print("\nSample data:")
print(df[["sex", "income"]].head())

# ---------------------------
# CLEAN DATA
# ---------------------------
df["income"] = df["income"].str.strip()
df["sex"] = df["sex"].str.strip()

# Convert income to binary
df["income_binary"] = df["income"].apply(lambda x: 1 if x == ">50K" else 0)

# ---------------------------
# ORIGINAL SELECTION RATES
# ---------------------------
original_rates = df.groupby("sex")["income_binary"].mean()

print("\nOriginal Selection Rates:")
print(original_rates)

# ---------------------------
# BIAS MITIGATION (REWEIGHTING)
# ---------------------------
df["weight"] = 1.0
df.loc[df["sex"] == "Female", "weight"] = 2.0

mitigated_rates = (
    df.groupby("sex")[["income_binary", "weight"]]
    .apply(lambda x: (x["income_binary"] * x["weight"]).sum() / x["weight"].sum())
)

print("\nMitigated Selection Rates:")
print(mitigated_rates)
