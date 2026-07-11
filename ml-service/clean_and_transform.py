import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

CSV_PATH = 'HumanDevelopmentIndex.csv'

def clean_and_transform():
    print(f"Loading raw dataset from: {os.path.abspath(CSV_PATH)}")
    df = pd.read_csv(CSV_PATH)
    
    print("\nOriginal DataFrame Columns and Indices:")
    for idx, col in enumerate(df.columns):
        if idx < 10 or idx == len(df.columns) - 1: # Print first few and last to avoid clutter
            print(f"Index {idx}: {col}")
    if len(df.columns) > 10:
        print("...")
        
    # 1. Select Target (Y) and Features (X) by Index
    # Dependent Variable (Y) is HDI Score (column index 1 in fallback, but index 4 in user prompt)
    # We will look for index 4, or fallback to 'HDI Score' column index
    hdi_score_col_idx = 4
    if hdi_score_col_idx < len(df.columns) and df.columns[hdi_score_col_idx] == 'HDI Score':
        Y = df.iloc[:, hdi_score_col_idx]
        print(f"\nTarget Variable (Y) selected from index {hdi_score_col_idx}: '{Y.name}'")
    else:
        # Check if 'HDI Score' is in columns
        if 'HDI Score' in df.columns:
            Y = df['HDI Score']
            hdi_score_col_idx = df.columns.get_loc('HDI Score')
            print(f"\nTarget Variable (Y) selected: '{Y.name}' (Index {hdi_score_col_idx})")
        else:
            Y = df.iloc[:, 1]
            hdi_score_col_idx = 1
            print(f"\nTarget Variable (Y) selected from index 1: '{Y.name}'")

    # Independent Variables (X) - we select core human development indicators
    core_features = ['Country', 'Life Expectancy', 'Mean Years of Schooling', 'Expected Years of Schooling', 'GNI per Capita']
    selected_features = [col for col in core_features if col in df.columns]
    X = df[selected_features]
    print(f"Independent Variables (X) shape: {X.shape[0]} rows, {X.shape[1]} columns")
    
    # 2. Count Null Values in X
    print("\nCounting Null Values in selected independent columns (first 10 shown):")
    null_counts = X.isnull().sum()
    for col, count in list(null_counts.items())[:10]:
        print(f"Column '{col}': {count} nulls")
        
    # 3. Fill Null Values in X using column mean (numeric only)
    print("\nFilling null values in independent columns with the column mean...")
    numeric_cols = X.select_dtypes(include=[np.number]).columns
    X[numeric_cols] = X[numeric_cols].fillna(X[numeric_cols].mean())
    
    # For categorical columns, fill with mode or placeholder
    categorical_cols = X.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        X[col] = X[col].fillna(X[col].mode()[0] if not X[col].mode().empty else 'Unknown')
        
    print("Null values count after cleaning (first 10 shown):")
    null_counts_after = X.isnull().sum()
    for col, count in list(null_counts_after.items())[:10]:
        print(f"Column '{col}': {count} nulls")
        
    # 4. Converting Categorical Text Labels into Numerical Values
    print("\nConverting categorical text labels to numerical values...")
    le = LabelEncoder()
    for col in categorical_cols:
        original_unique = X[col].unique()[:5]
        X[col] = le.fit_transform(X[col].astype(str))
        encoded_unique = X[col].unique()[:5]
        print(f"Encoded '{col}': {original_unique} -> {encoded_unique}")
        
    # Display preview of transformed features
    print("\n================ CLEANED AND TRANSFORMED X PREVIEW ================")
    print(X.head())
    print("===================================================================\n")
    
    # Save the cleaned datasets
    X.to_csv('X_cleaned.csv', index=False)
    Y.to_csv('Y_cleaned.csv', index=False)
    print(f"Cleaned X saved to: {os.path.abspath('X_cleaned.csv')}")
    print(f"Cleaned Y saved to: {os.path.abspath('Y_cleaned.csv')}")

def main():
    clean_and_transform()

if __name__ == '__main__':
    main()
