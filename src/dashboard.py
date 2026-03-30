import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Governance Dashboard", layout="wide")

st.title("🤖 AI Governance Dashboard")

# -------------------------
# LOAD RESULTS
# -------------------------
try:
    with open("results.json", "r") as f:
        data = json.load(f)
except:
    st.error("⚠️ Run pipeline first (results.json not found)")
    st.stop()

# -------------------------
# METRICS
# -------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Accuracy", round(data["accuracy"], 3))
col2.metric("DIR", round(data["dir"], 3))
col3.metric("Risk Score", round(data["risk"], 2))

# -------------------------
# DECISION
# -------------------------
st.subheader("📢 Governance Decision")

if data["risk"] > 50:
    st.error(data["decision"])
elif data["risk"] > 30:
    st.warning(data["decision"])
else:
    st.success(data["decision"])

# -------------------------
# TABLE
# -------------------------
st.subheader("📊 Bias Improvement")

df = pd.DataFrame({
    "Metric": ["Female Rate", "Male Rate", "DIR"],
    "Before": [
        data["female_before"],
        data["male_before"],
        data["female_before"] / data["male_before"]
    ],
    "After": [
        data["female_after"],
        data["male_after"],
        data["dir"]
    ]
})

st.dataframe(df)

# -------------------------
# CHART
# -------------------------
st.subheader("📈 Selection Rate Comparison")

labels = ["Female", "Male"]
before = [data["female_before"], data["male_before"]]
after = [data["female_after"], data["male_after"]]

x = range(len(labels))

plt.figure()
plt.bar(x, before)
plt.bar(x, after, bottom=before)
plt.xticks(x, labels)

st.pyplot(plt)

# -------------------------
# DOWNLOAD REPORT
# -------------------------
st.subheader("📄 Download Report")

try:
    with open("AI_Governance_Report.pdf", "rb") as file:
        st.download_button(
            label="📥 Download Governance Report",
            data=file,
            file_name="AI_Governance_Report.pdf",
            mime="application/pdf"
        )
except:
    st.warning("⚠️ Report not found. Run pipeline first.")

# -------------------------
# FOOTER
# -------------------------
st.markdown("---")
st.markdown("Built with ❤️ for AI Governance Project")