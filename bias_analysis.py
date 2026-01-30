import pandas as pd
from pathlib import Path

# Define column names (VERY IMPORTANT)
columns = [
    "age", "workclass", "fnlwgt", "education", "education-num",
    "marital-status", "occupation", "relationship", "race", "sex",
    "capital-gain", "capital-loss", "hours-per-week",
    "native-country", "income"
]

# Get project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Load dataset with column names
data_path = BASE_DIR / "data" / "adult.csv"
df = pd.read_csv(data_path, header=None, names=columns)

# Clean target column
df["income"] = df["income"].str.strip()

print("Dataset loaded successfully")
print(df[["sex", "income"]].head())

# -----------------------------
# Selection Rate Calculation
# -----------------------------

# Total count per gender
total_by_gender = df.groupby("sex").size()

# Count of favorable outcomes (>50K) per gender
positive_by_gender = df[df["income"] == ">50K"].groupby("sex").size()

# Selection rate = positive / total
selection_rate = positive_by_gender / total_by_gender

print("\nSelection Rates (P(income >50K | gender)):")
print(selection_rate)

# -----------------------------
# Disparate Impact Ratio (SAFE)
# -----------------------------

# Normalize index values
selection_rate.index = selection_rate.index.str.strip()

female_rate = selection_rate.get("Female")
male_rate = selection_rate.get("Male")

dir_gender = female_rate / male_rate

print("\nDisparate Impact Ratio (Female / Male):")
print(round(dir_gender, 3))

# -----------------------------
# Intersectional Group Creation
# -----------------------------

df["sex"] = df["sex"].str.strip()
df["race"] = df["race"].str.strip()

df["intersection_group"] = df["sex"] + "_" + df["race"]

print("\nSample intersectional groups:")
print(df[["intersection_group", "income"]].head())

# -----------------------------
# Intersectional Selection Rates
# -----------------------------

intersection_selection = (
    df[df["income"] == ">50K"]
    .groupby("intersection_group")
    .size()
    / df.groupby("intersection_group").size()
)

intersection_selection = intersection_selection.sort_values()

print("\nIntersectional Selection Rates (Income >50K):")
print(intersection_selection)

# -----------------------------
# Intersectional Disparate Impact
# -----------------------------

reference_group = "Male_White"
reference_rate = intersection_selection.get(reference_group)

intersection_dir = intersection_selection / reference_rate

print("\nIntersectional Disparate Impact Ratios (vs Male_White):")
print(intersection_dir)



