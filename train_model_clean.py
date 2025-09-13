import pandas as pd 
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
from extract_features import extract_features

df = pd.read_csv("verified_urls.csv")
df.dropna(inplace=True)

X = df["url"].apply(extract_features).apply(pd.Series)
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier()
model.fit(X_train, y_train)

joblib.dump(model, "phishing_model.pkl")
print("✅ Model trained and saved as phishing_model.pkl")
