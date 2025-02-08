import os
import xgboost as xgb
import pandas as pd
import shap
import matplotlib.pyplot as plt

# Ensure the "results" folder exists
results_folder = r""
os.makedirs(results_folder, exist_ok=True)

# Initialize the model with GPU settings (if available).
model = xgb.XGBClassifier(
    tree_method="gpu_hist",        # Uncomment if GPU is available.
    predictor="gpu_predictor",      # Uncomment if GPU is available.
    use_label_encoder=False,
    eval_metric="mlogloss"
)
model_path = r""
model.load_model(model_path)

# Load processed data.
data_path = r""
try:
    df = pd.read_csv(data_path)
except FileNotFoundError:
    raise Exception("Processed data not found. Run feature_engineering.py first.")

# Strip whitespace from column names.
df.columns = df.columns.str.strip()

# Define the feature columns.
features = ["SMA_50", "SMA_200", "RSI", "MACD"]

# Verify that the required features exist.
if not all(feature in df.columns for feature in features):
    raise Exception("Not all required features are present in the processed data.")

# Ensure feature columns are numeric.
for col in features:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Drop rows with missing feature values.
df = df.dropna(subset=features)

# Prepare the SHAP explainer.
explainer = shap.Explainer(model, df[features])
shap_values = explainer(df[features])

# If the model is multi-class, shap_values.values will be 3D.
# For a 2D summary plot, select one class (e.g., class index 1).
if hasattr(shap_values, "values") and shap_values.values.ndim == 3:
    shap_vals_to_plot = shap_values.values[:, 1, :]
else:
    shap_vals_to_plot = shap_values.values

# Generate and save the SHAP summary plot.
plt.figure()
shap.summary_plot(shap_vals_to_plot, df[features], show=False)
plt.tight_layout()
save_path = os.path.join(results_folder, "shap_summary.png")
plt.savefig(save_path)
plt.close()
print(f"SHAP summary plot saved to '{save_path}'.")
