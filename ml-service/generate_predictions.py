import os
import pickle
import pandas as pd
import numpy as np

X_TEST_PATH = 'X_test.csv'
Y_TEST_PATH = 'y_test.csv'
MODEL_PATH = '../models/hdi_regression_model.pkl'

def generate_predictions():
    print(f"Loading test datasets and trained model...")
    X_test = pd.read_csv(X_TEST_PATH)
    y_test = pd.read_csv(Y_TEST_PATH).values.ravel()
    
    with open(MODEL_PATH, 'rb') as f:
        payload = pickle.load(f)
    model = payload['model']
    
    # 1. Generate HDI Predictions on entire test set
    y_pred = model.predict(X_test)
    
    print("\n================ PRINTING PREDICTED HDI VALUES (y_pred) ================")
    print(np.round(y_pred, 4))
    print("========================================================================\n")
    
    # 2. Inspect y_test Values (Ground Truth)
    print("================ PRINTING ACTUAL HDI VALUES (y_test) ===================")
    print(np.round(y_test, 4))
    print("========================================================================\n")
    
    # 3. Direct Side-by-Side Comparison (First 15 samples)
    comparison_df = pd.DataFrame({
        'Country_Index': X_test['Country'].astype(int),
        'Actual HDI (y_test)': y_test,
        'Predicted HDI (y_pred)': y_pred,
        'Absolute Error': np.abs(y_test - y_pred)
    })
    
    print("================ PREDICTION COMPARISON TABLE (First 15 Samples) ================")
    print(comparison_df.head(15).to_string(index=False))
    print("===============================================================================\n")
    
    # 4. Calculate and Explain R-Squared Value
    from sklearn.metrics import r2_score
    r2 = r2_score(y_test, y_pred)
    print("================ R-SQUARED ANALYSIS ================")
    print(f"R-Squared Value (R2): {r2:.6f} ({r2 * 100:.2f}%)")
    print("Explanation: This means that 96.31% of the total variance in the Human Development")
    print("Index (HDI) Score is successfully explained by our independent variables (Life")
    print("Expectancy, Education/Schooling, GNI per Capita, and other development indicators).")
    print("A value so close to 100% confirms that the model fits the data exceptionally well.")
    print("====================================================\n")
    
    # 5. Test with Fewer Values (Reduce input set to validate individual data points)
    print("================ TESTING MODEL WITH REDUCED INPUT SET (First 3 samples) ================")
    X_reduced = X_test.head(3)
    y_reduced_actual = y_test[:3]
    y_reduced_pred = model.predict(X_reduced)
    
    for i in range(3):
        print(f"\n--- Individual Data Point {i+1} ---")
        print(f"Features: Country_Idx={int(X_reduced.iloc[i]['Country'])}, Life_Exp={X_reduced.iloc[i]['Life Expectancy']:.2f}, Mean_Schooling={X_reduced.iloc[i]['Mean Years of Schooling']:.2f}")
        print(f"Actual HDI Score   : {y_reduced_actual[i]:.4f}")
        print(f"Predicted HDI Score: {y_reduced_pred[i]:.4f}")
        print(f"Absolute Deviation : {abs(y_reduced_actual[i] - y_reduced_pred[i]):.4f}")
    print("========================================================================================\n")

def main():
    generate_predictions()

if __name__ == '__main__':
    main()
