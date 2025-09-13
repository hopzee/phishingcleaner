import joblib 
import pandas as pd
from extract_features import extract_features

model = joblib.load("phishing_model.pkl")

test_urls = [
    "https://www.google.com",
    "https://g00gle.com",
    "https://facebook.com",
    "https://faceb00k-login.com",
    "https://paypal.com",
    "https://paypa1.com"
]

for url in test_urls:
    feats = extract_features(url)
    X = pd.DataFrame([feats])[model.feature_names_in_]

    if feats["has_homoglyph"]:
        prediction = 1
    else:
        prediction = model.predict(X)[0]

    label = "Phishing ❌" if prediction == 1 else "Legitimate ✅"
    homoglyph = "⚠️ Homoglyph detected" if feats["has_homoglyph"] else "✔️ Normal"
    print(f"{url} → {label} ({homoglyph})")
