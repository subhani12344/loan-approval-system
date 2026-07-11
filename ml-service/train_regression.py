import os
import pickle
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

X_TRAIN_PATH = 'X_train.csv'
X_TEST_PATH = 'X_test.csv'
Y_TRAIN_PATH = 'y_train.csv'
Y_TEST_PATH = 'y_test.csv'
PLOTS_DIR = '../models/plots'
os.makedirs(PLOTS_DIR, exist_ok=True)

def train_linear_regression():
    print(f"Loading split datasets...")
    X_train = pd.read_csv(X_TRAIN_PATH)
    X_test = pd.read_csv(X_TEST_PATH)
    y_train = pd.read_csv(Y_TRAIN_PATH).values.ravel()
    y_test = pd.read_csv(Y_TEST_PATH).values.ravel()
    
    # 1. Instantiate and train the Linear Regression Model
    print("Instantiating and fitting Linear Regression model...")
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # 2. Testing the test field from the split
    print("Running predictions on the test dataset...")
    y_pred = model.predict(X_test)
    
    # 3. Evaluate Performance Metrics
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    print("\n================ REGRESSION PERFORMANCE METRICS ================")
    print(f"Mean Absolute Error (MAE)   : {mae:.6f}")
    print(f"Mean Squared Error (MSE)    : {mse:.6f}")
    print(f"Root Mean Squared Error(RMSE): {rmse:.6f}")
    print(f"R^2 Score (R-squared)        : {r2:.6f}")
    print("================================================================\n")
    
    # 4. Generate and save prediction plots
    print("Generating prediction analysis plots...")
    
    # Plot 1: Actual vs Predicted Scatter
    plt.figure(figsize=(8, 6))
    plt.scatter(y_test, y_pred, color='blue', alpha=0.6, edgecolors='k')
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2) # Diagonal line
    plt.title('Linear Regression: Actual vs. Predicted HDI Scores')
    plt.xlabel('Actual HDI Scores')
    plt.ylabel('Predicted HDI Scores')
    plt.grid(True)
    plt.tight_layout()
    scatter_path = os.path.join(PLOTS_DIR, 'regression_actual_vs_predicted.png')
    plt.savefig(scatter_path)
    plt.close()
    
    # Plot 2: Residuals Plot
    residuals = y_test - y_pred
    plt.figure(figsize=(8, 6))
    plt.scatter(y_pred, residuals, color='purple', alpha=0.6, edgecolors='k')
    plt.axhline(y=0, color='r', linestyle='--', lw=2)
    plt.title('Linear Regression: Residuals vs. Predicted Values')
    plt.xlabel('Predicted HDI Scores')
    plt.ylabel('Residuals (Actual - Predicted)')
    plt.grid(True)
    plt.tight_layout()
    residuals_path = os.path.join(PLOTS_DIR, 'regression_residuals.png')
    plt.savefig(residuals_path)
    plt.close()
    
    print(f"Regression plots saved successfully to: {os.path.abspath(PLOTS_DIR)}")
    
    # Save the trained model pipeline
    model_dir = '../models'
    os.makedirs(model_dir, exist_ok=True)
    model_save_path = os.path.join(model_dir, 'hdi_regression_model.pkl')
    
    payload = {
        'model': model,
        'feature_names': list(X_train.columns)
    }
    
    with open(model_save_path, 'wb') as f:
        pickle.dump(payload, f)
    print(f"Regression model serialized and saved to: {os.path.abspath(model_save_path)}")

def main():
    train_linear_regression()

if __name__ == '__main__':
    main()
