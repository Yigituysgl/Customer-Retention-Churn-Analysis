import streamlit as st
import pandas as pd
import numpy as np
import joblib, json
from pathlib import Path

# ----------------------
# App configuration
# ----------------------
st.set_page_config(page_title="Churn Risk Dashboard", page_icon="📉", layout="wide")
st.title("📉 Customer Churn Risk Dashboard")

st.markdown(
    """
This app predicts churn probability for telecom customers and highlights key drivers.

**How to use**
- Choose **Single customer** to try values.
- Or use **Batch (CSV upload)** with the *exact 5 columns*:  
  `tenure, MonthlyCharges, TotalCharges, Contract, OnlineSecurity`
"""
)

# ----------------------
# Load pipeline & schema
# ----------------------
ART = Path(__file__).resolve().parent.parent / "app_artifacts"
PIPELINE_PATH = ART / "rf_pipeline.joblib"
SCHEMA_PATH   = ART / "raw_input_columns.json"

pipeline = joblib.load(PIPELINE_PATH)
raw_cols = json.load(open(SCHEMA_PATH))

# ----------------------
# Sidebar mode selector
# ----------------------
mode = st.sidebar.radio("Prediction Mode", ["🔹 Single customer", "📄 Batch (CSV upload)"])

# ----------------------
# Single-customer mode (5 inputs only)
# ----------------------
if mode.startswith("🔹"):
    st.subheader("Enter customer attributes (top 5 drivers)")

    col1, col2, col3 = st.columns(3)
    with col1:
        tenure = st.number_input("tenure (months)", min_value=0, max_value=120, value=12, step=1)
        monthly = st.number_input("MonthlyCharges", min_value=0.0, max_value=200.0, value=70.0, step=1.0)
    with col2:
        total = st.number_input("TotalCharges", min_value=0.0, max_value=20000.0, value=840.0, step=10.0)
        contract = st.selectbox("Contract", ["Month-to-month","One year","Two year"])
    with col3:
        online_sec = st.selectbox("OnlineSecurity", ["No","Yes","No internet service"])

    # Build row in the exact order expected by pipeline
    row = pd.DataFrame([{
        "tenure": tenure,
        "MonthlyCharges": monthly,
        "TotalCharges": total,
        "Contract": contract,
        "OnlineSecurity": online_sec
    }])[raw_cols]

    if st.button("Predict churn"):
        prob = float(pipeline.predict_proba(row)[0, 1])
        label = "High risk" if prob >= 0.6 else ("Medium risk" if prob >= 0.4 else "Low risk")

        st.metric("Churn probability", f"{prob:.2%}")
        st.success(f"Risk level: **{label}**")
        st.caption("Tip: focus retention offers on high-probability customers.")

# ----------------------
# Batch mode
# ----------------------
else:
    st.subheader("Upload a CSV with columns:")
    st.code(", ".join(raw_cols))
    file = st.file_uploader("Choose a CSV file", type=["csv"])

    if file:
        df_raw = pd.read_csv(file)

        # Keep only the expected columns; add defaults if missing
        df_app = pd.DataFrame(columns=raw_cols)
        for c in raw_cols:
            if c in df_raw.columns:
                df_app[c] = df_raw[c]
            else:
                df_app[c] = 0 if c in ["tenure","MonthlyCharges","TotalCharges"] else "No"

        probs = pipeline.predict_proba(df_app)[:, 1]
        out = df_raw.copy()
        out["churn_probability"] = np.round(probs, 4)
        out["risk_label"] = pd.cut(out["churn_probability"],
                                   bins=[-1, 0.4, 0.6, 1.0],
                                   labels=["Low","Medium","High"])

        st.subheader("Predictions (top 20 rows)")
        st.dataframe(out.head(20))

        st.download_button(
            "Download predictions as CSV",
            data=out.to_csv(index=False).encode("utf-8"),
            file_name="churn_predictions.csv",
            mime="text/csv"
        )
