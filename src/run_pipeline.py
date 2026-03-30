print("🚀 AI Governance V3 (Dynamic System) Started")

import pandas as pd
import json
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# -------------------------
# LOAD DATA
# -------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "adult.csv"

print("📂 Loading dataset from:", DATA_PATH)

df = pd.read_csv(DATA_PATH, header=None)

df.columns = [
    "age", "workclass", "fnlwgt", "education", "education_num",
    "marital_status", "occupation", "relationship", "race", "sex",
    "capital_gain", "capital_loss", "hours_per_week",
    "native_country", "income"
]

print("✅ Dataset Loaded")

# -------------------------
# CLEAN DATA
# -------------------------
df["income"] = df["income"].str.strip()
df["sex"] = df["sex"].str.strip()

df["income_binary"] = df["income"].apply(
    lambda x: 1 if x == ">50K" else 0
)

print("✅ Data cleaned")

# -------------------------
# FEATURES
# -------------------------
features = [
    "age", "education_num", "hours_per_week",
    "capital_gain", "capital_loss"
]

X = df[features]
y = df["income_binary"]
gender = df["sex"]

# -------------------------
# SPLIT
# -------------------------
X_train, X_test, y_train, y_test, gender_train, gender_test = train_test_split(
    X, y, gender, test_size=0.3, random_state=42
)

print("✅ Data split completed")

# -------------------------
# FUNCTION: EVALUATE MODEL
# -------------------------
def evaluate_model(model, name):
    print(f"\n🔍 Evaluating {name}")

    model.fit(X_train, y_train)

    # BEFORE (No mitigation)
    y_pred_before = model.predict(X_test)

    df_before = pd.DataFrame({
        "gender": gender_test,
        "prediction": y_pred_before
    })

    sel_before = df_before.groupby("gender")["prediction"].mean()
    f_before = sel_before.get("Female", 0)
    m_before = sel_before.get("Male", 1)
    dir_before = f_before / m_before

    # AFTER (Threshold mitigation)
    probs = model.predict_proba(X_test)[:, 1]

    y_pred_after = []
    for p, g in zip(probs, gender_test):
        if g == "Female":
            y_pred_after.append(1 if p > 0.3 else 0)
        else:
            y_pred_after.append(1 if p > 0.5 else 0)

    y_pred_after = pd.Series(y_pred_after)

    df_after = pd.DataFrame({
        "gender": gender_test,
        "prediction": y_pred_after
    })

    sel_after = df_after.groupby("gender")["prediction"].mean()
    f_after = sel_after.get("Female", 0)
    m_after = sel_after.get("Male", 1)
    dir_after = f_after / m_after

    # Accuracy
    acc = accuracy_score(y_test, y_pred_after)

    # Risk
    risk = (1 - dir_after) * 70 + (1 - acc) * 30

    print(f"Accuracy: {round(acc,3)} | DIR: {round(dir_after,3)} | Risk: {round(risk,2)}")

    return {
        "model": name,
        "accuracy": acc,
        "dir": dir_after,
        "risk": risk,
        "female_before": f_before,
        "male_before": m_before,
        "female_after": f_after,
        "male_after": m_after
    }

# -------------------------
# MODELS
# -------------------------
lr = LogisticRegression(max_iter=1000)
rf = RandomForestClassifier(n_estimators=100, random_state=42)

results = []
results.append(evaluate_model(lr, "Logistic Regression"))
results.append(evaluate_model(rf, "Random Forest"))

# -------------------------
# SELECT BEST MODEL
# -------------------------
best_model = sorted(results, key=lambda x: x["risk"])[0]

print("\n🏆 BEST MODEL:", best_model["model"])

# -------------------------
# DECISION
# -------------------------
if best_model["risk"] > 50:
    decision = "NOT SAFE TO DEPLOY"
elif best_model["risk"] > 30:
    decision = "DEPLOY WITH CONTROLS"
else:
    decision = "SAFE TO DEPLOY"

print("⚖️ Decision:", decision)

# -------------------------
# SAVE RESULTS
# -------------------------
output = best_model
output["decision"] = decision

with open("results.json", "w") as f:
    json.dump(output, f, indent=4)

print("📁 results.json created successfully")