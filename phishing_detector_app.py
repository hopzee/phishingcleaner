import streamlit as st
import joblib
import pandas as pd
from extract_features import extract_features

model = joblib.load("phishing_model.pkl")

st.title("🔒 Anti-Phishing URL Checker")

url_input = st.text_input("Enter a URL to check", "")

if url_input:
    features = extract_features(url_input)
    df = pd.DataFrame([features])[model.feature_names_in_]

    if features["has_homoglyph"]:
        prediction = 1
    else:
        prediction = model.predict(df)[0]

    result = "Phishing ❌" if prediction == 1 else "Legitimate ✅"
    st.write(f"Prediction: **{result}**")
