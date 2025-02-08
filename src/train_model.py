import os
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Ensure the "models" folder exists
model_folder = r""
os.makedirs(model_folder, exist_ok=True)

# Load processed data
data_path = r""
try:
    df = pd.read_csv(data_path)
except FileNotFoundError:
    raise Exception(f"File '{data_path}' not found. Run feature_engineering.py first.")

# Strip any whitespace from column names.
df.columns = df.columns.str.strip()

# Define a function to compute a risk label based on technical indicators.
def compute_risk_label(row):
    risk_score = 0
    if row["RSI"] < 30 or row["RSI"] > 70:
        risk_score += 1
    if row["SMA_50"] < row["SMA_200"]:
        risk_score += 1
    if abs(row["MACD"]) > 1:
        risk_score += 1

    if risk_score == 0:
        return 0  # Low risk
    elif risk_score == 1:
        return 1  # Medium risk
    else:
        return 2  # High risk

# Ensure necessary columns exist.
required_cols = ["SMA_50", "SMA_200", "RSI", "MACD"]
if not all(col in df.columns for col in required_cols):
    raise Exception("Processed data does not contain all required feature columns.")

df["Risk_Label"] = df.apply(compute_risk_label, axis=1)

# Define features and target.
X = df[required_cols]
y = df["Risk_Label"]

# Split into training and testing sets.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the XGBoost classifier.
model_params = {
    "use_label_encoder": False,
    "eval_metric": "mlogloss",
    # Uncomment the GPU options if you have a compatible GPU:
    # "tree_method": "gpu_hist",
    # "predictor": "gpu_predictor"
}
model = xgb.XGBClassifier(**model_params)
model.fit(X_train, y_train)

# Evaluate the model.
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")

# Save the trained model.
model_save_path = os.path.join(model_folder, "financial_risk_model.json")
model.save_model(model_save_path)
print("Model training complete. Model saved in the 'models' folder.")
