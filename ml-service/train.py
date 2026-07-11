import os
import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

def generate_synthetic_data(num_samples=2500):
    np.random.seed(42)
    
    # Generate features
    income = np.random.normal(65000, 25000, num_samples).clip(15000, 250000)
    credit_score = np.random.normal(660, 80, num_samples).clip(300, 850)
    loan_amount = np.random.normal(25000, 15000, num_samples).clip(2000, 150000)
    loan_term = np.random.choice([12, 24, 36, 60, 120], size=num_samples, p=[0.1, 0.2, 0.4, 0.2, 0.1])
    hdi_index = np.random.uniform(0.35, 0.98, num_samples)
    age = np.random.normal(38, 12, num_samples).clip(18, 75)
    
    df = pd.DataFrame({
        'income': income,
        'credit_score': credit_score,
        'loan_amount': loan_amount,
        'loan_term': loan_term,
        'hdi_index': hdi_index,
        'age': age
    })
    
    # Define realistic target classification rules
    # Credit Score has the highest weight, followed by DTI (Debt-to-Income) and HDI
    annual_payment = (df['loan_amount'] / df['loan_term']) * 12
    dti = annual_payment / df['income']
    
    # Calculate a score probability
    score = (
        ((df['credit_score'] - 300) / 550) * 0.50 +
        (dti.apply(lambda x: 0.25 if x < 0.15 else (0.15 if x < 0.30 else (0.05 if x < 0.45 else 0.0)))) +
        (df['hdi_index'] * 0.15) +
        (df['age'].apply(lambda x: 0.10 if 25 <= x <= 55 else 0.05))
    )
    
    # Convert score to probability (0 to 1)
    prob = score.clip(0, 1)
    
    # Apply forced exclusions (FICO < 450 or extreme DTI)
    prob = np.where(df['credit_score'] < 450, prob * 0.4, prob)
    prob = np.where(dti > 0.6, prob * 0.3, prob)
    
    # Convert to binary target
    df['approved'] = (prob >= 0.58).astype(int)
    
    return df

def main():
    print("Generating synthetic credit risk dataset...")
    df = generate_synthetic_data(3000)
    
    # Split into features and target
    X = df.drop(columns=['approved'])
    y = df['approved']
    
    # Split into train and test sets BEFORE fitting scaler to prevent data leakage
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print(f"Dataset split completed: Train={len(X_train)} samples, Test={len(X_test)} samples")
    
    # Preprocessing: Scale the numerical features
    scaler = StandardScaler()
    
    # Fit the scaler ONLY on the training features
    X_train_scaled = scaler.fit_transform(X_train)
    # Transform test features based on training scaler
    X_test_scaled = scaler.transform(X_test)
    
    # Train the Classifier
    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # Predictions
    y_pred = model.predict(X_test_scaled)
    
    # Evaluate
    accuracy = accuracy_score(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)
    class_report = classification_report(y_test, y_pred)
    
    print("\n================ MODEL EVALUATION SUMMARY ================")
    print(f"Accuracy: {accuracy * 100:.2f}%")
    print("\nConfusion Matrix:")
    print(conf_matrix)
    print("\nClassification Report:")
    print(class_report)
    print("==========================================================")
    
    # Save the scaler and model pipeline
    model_dir = '../models'
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, 'hdi_prediction_model.pkl')
    
    payload = {
        'model': model,
        'scaler': scaler,
        'feature_names': list(X.columns)
    }
    
    with open(model_path, 'wb') as f:
        pickle.dump(payload, f)
        
    print(f"\nModel pipeline successfully serialized and saved to: {os.path.abspath(model_path)}")

if __name__ == '__main__':
    main()
