import os
import pandas as pd
from sklearn.model_selection import train_test_split

X_PATH = 'X_cleaned.csv'
Y_PATH = 'Y_cleaned.csv'

def split_dataset():
    print(f"Loading cleaned features from: {os.path.abspath(X_PATH)}")
    print(f"Loading cleaned target from: {os.path.abspath(Y_PATH)}")
    
    X = pd.read_csv(X_PATH)
    y = pd.read_csv(Y_PATH)
    
    # 1. Use sklearn's train_test_split to separate into training (80%) and testing (20%) sets
    # Setting random_state=42 for reproducibility
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("\n================ DATASET SPLIT SUMMARY ================")
    print(f"Full Dataset Shape  : X={X.shape}, y={y.shape}")
    print(f"Training Split Shape: X_train={X_train.shape}, y_train={y_train.shape} (80%)")
    print(f"Testing Split Shape : X_test={X_test.shape}, y_test={y_test.shape} (20%)")
    print("=======================================================\n")
    
    # Save the splits
    X_train.to_csv('X_train.csv', index=False)
    X_test.to_csv('X_test.csv', index=False)
    y_train.to_csv('y_train.csv', index=False)
    y_test.to_csv('y_test.csv', index=False)
    
    print(f"Saved X_train.csv to: {os.path.abspath('X_train.csv')}")
    print(f"Saved X_test.csv to: {os.path.abspath('X_test.csv')}")
    print(f"Saved y_train.csv to: {os.path.abspath('y_train.csv')}")
    print(f"Saved y_test.csv to: {os.path.abspath('y_test.csv')}")

def main():
    split_dataset()

if __name__ == '__main__':
    main()
