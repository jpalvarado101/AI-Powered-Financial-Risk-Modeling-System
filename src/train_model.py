import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# Load processed dataset
df = pd.read_csv("J:\John Alvarado\Documents\projects\AI-Powered Financial Risk Modeling System\AI-Powered-Financial-Risk-Modeling-System\data\processed_data.csv")


# Define a function to compute a risk label based on technical indicators
def compute_risk_label(row):
    """
    Heuristic to compute a risk label:
      - If RSI is in an extreme region (<30 or >70), add 1 point.
      - If SMA_50 is below SMA_200 (suggesting a bearish trend), add 1 point.
      - If the absolute MACD is greater than 1 (indicating significant momentum), add 1 point.
    
    Risk label mapping:
      - 0 points: Low Risk (0)
      - 1 point : Medium Risk (1)
      - 2 or more points: High Risk (2)
    """
    risk_score = 0
    
    # RSI-based risk
    if row["RSI"] < 30 or row["RSI"] > 70:
        risk_score += 1

    # Trend-based risk: if SMA_50 is below SMA_200, this might indicate a downward trend.
    if row["SMA_50"] < row["SMA_200"]:
        risk_score += 1

    # MACD-based risk: significant momentum indicated by |MACD| > 1
    if abs(row["MACD"]) > 1:
        risk_score += 1

    # Map risk_score to risk label: 0 = Low, 1 = Medium, 2 = High
    if risk_score == 0:
        return 0   # Low risk
    elif risk_score == 1:
        return 1   # Medium risk
    else:
        return 2   # High risk

# Apply the risk labeling function to each row of the DataFrame
df["Risk_Label"] = df.apply(compute_risk_label, axis=1)

# Define features & target
X = df[["SMA_50", "SMA_200", "RSI", "MACD"]]
y = df["Risk_Label"]  # Risk classification: 0 = Low, 1 = Medium, 2 = High

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train a GPU-enabled XGBoost model
model = xgb.XGBClassifier(
    use_label_encoder=False,
    eval_metric="mlogloss",
    tree_method="gpu_hist",       # GPU-accelerated training
    predictor="gpu_predictor"     # GPU-accelerated inference
)

model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")

# Save model
model.save_model("J:/John Alvarado/Documents/projects/AI-Powered Financial Risk Modeling System/AI-Powered-Financial-Risk-Modeling-System/models/financial_risk_model.json")
