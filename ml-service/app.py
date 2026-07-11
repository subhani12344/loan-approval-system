import os
import pickle
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Load Classification Model Pipeline (For Express API Integration)
MODEL_PATH = os.getenv('MODEL_PATH', '../models/hdi_prediction_model.pkl')
model_pipeline = None

# Load Regression Model Pipeline (For HTML Web Interface)
REGRESSION_MODEL_PATH = os.getenv('REGRESSION_MODEL_PATH', '../models/hdi_regression_model.pkl')
regression_pipeline = None

try:
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, 'rb') as f:
            model_pipeline = pickle.load(f)
        print(f"Loaded ML classification model from: {os.path.abspath(MODEL_PATH)}")
    else:
        print(f"Warning: Classification model file not found at {os.path.abspath(MODEL_PATH)}")
except Exception as e:
    print(f"Error loading classification model: {e}")

try:
    if os.path.exists(REGRESSION_MODEL_PATH):
        with open(REGRESSION_MODEL_PATH, 'rb') as f:
            regression_pipeline = pickle.load(f)
        print(f"Loaded ML regression model from: {os.path.abspath(REGRESSION_MODEL_PATH)}")
    else:
        print(f"Warning: Regression model file not found at {os.path.abspath(REGRESSION_MODEL_PATH)}")
except Exception as e:
    print(f"Error loading regression model: {e}")

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/predict-form', methods=['GET'])
def predict_form():
    return render_template('indexnew.html', prediction=None)

@app.route('/health', methods=['GET'])
def health():
    classification_status = 'loaded' if model_pipeline is not None else 'not_loaded'
    regression_status = 'loaded' if regression_pipeline is not None else 'not_loaded'
    return jsonify({
        'status': 'healthy',
        'service': 'loan-approval-ml-service',
        'classification_model_status': classification_status,
        'regression_model_status': regression_status
    }), 200

@app.route('/predict', methods=['POST'])
def predict():
    # If request is from the HTML prediction form
    if request.form:
        try:
            country = float(request.form.get('country', 0))
            life_expectancy = float(request.form.get('life_expectancy', 70))
            mean_schooling = float(request.form.get('mean_schooling', 10))
            expected_schooling = float(request.form.get('expected_schooling', 12))
            gni_capita = float(request.form.get('gni_capita', 10000))
            
            if regression_pipeline is None:
                return render_template('indexnew.html', prediction="Error: ML regression model not loaded on server")
                
            input_data = pd.DataFrame([{
                'Country': country,
                'Life Expectancy': life_expectancy,
                'Mean Years of Schooling': mean_schooling,
                'Expected Years of Schooling': expected_schooling,
                'GNI per Capita': gni_capita
            }])
            
            model = regression_pipeline['model']
            # Run inference
            pred_hdi = float(model.predict(input_data)[0])
            pred_hdi_rounded = round(pred_hdi, 4)
            pred_hdi_rounded = max(min(pred_hdi_rounded, 1.0), 0.0)
            
            print(f"Regression prediction computed: hdi={pred_hdi_rounded:.4f}")
            return render_template('indexnew.html', prediction=pred_hdi_rounded)
            
        except Exception as e:
            print(f"Regression prediction failed: {e}")
            return render_template('indexnew.html', prediction=f"Error: {e}")

    # Otherwise, handle JSON API POST request (For Express dashboard predictions)
    if model_pipeline is None:
        return jsonify({'message': 'ML Classification Model not loaded on server'}), 500
        
    try:
        data = request.get_json()
        
        # Extract features
        borrower_name = data.get('borrowerName', 'Unknown')
        income = float(data.get('income'))
        credit_score = float(data.get('creditScore'))
        loan_amount = float(data.get('loanAmount'))
        loan_term = float(data.get('loanTerm'))
        hdi_index = float(data.get('hdiIndex'))
        age = float(data.get('age'))
        
        # Format features into DataFrame matching the model's training columns
        input_data = pd.DataFrame([{
            'income': income,
            'credit_score': credit_score,
            'loan_amount': loan_amount,
            'loan_term': loan_term,
            'hdi_index': hdi_index,
            'age': age
        }])
        
        # Load scaler and model
        scaler = model_pipeline['scaler']
        model = model_pipeline['model']
        
        # Preprocess features
        input_scaled = scaler.transform(input_data)
        
        # Run prediction
        probabilities = model.predict_proba(input_scaled)[0]
        prob_approved = float(probabilities[1])
        
        # Determine status
        status = 'APPROVED' if prob_approved >= 0.6 else 'REJECTED'
        
        # Determine risk rating
        risk_rating = 'MEDIUM'
        if prob_approved > 0.8:
            risk_rating = 'LOW'
        elif prob_approved > 0.6:
            risk_rating = 'MEDIUM'
        elif prob_approved > 0.45:
            risk_rating = 'HIGH'
        else:
            risk_rating = 'CRITICAL'
            
        print(f"Classification prediction computed for {borrower_name}: status={status}, prob={prob_approved:.4f}")
        
        return jsonify({
            'probability': prob_approved,
            'status': status,
            'riskRating': risk_rating
        }), 200
        
    except (TypeError, ValueError) as val_err:
        return jsonify({'message': f'Invalid parameter formats: {val_err}'}), 400
    except Exception as e:
        print(f"Classification prediction failed: {e}")
        return jsonify({'message': f'Error computing prediction: {e}'}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
