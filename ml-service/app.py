import os
import pickle
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Load Model Pipeline
MODEL_PATH = os.getenv('MODEL_PATH', '../models/hdi_prediction_model.pkl')
model_pipeline = None

try:
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, 'rb') as f:
            model_pipeline = pickle.load(f)
        print(f"Loaded ML model from: {os.path.abspath(MODEL_PATH)}")
    else:
        print(f"Warning: Model file not found at {os.path.abspath(MODEL_PATH)}")
except Exception as e:
    print(f"Error loading model: {e}")

@app.route('/health', methods=['GET'])
def health():
    model_status = 'loaded' if model_pipeline is not None else 'not_loaded'
    return jsonify({
        'status': 'healthy',
        'service': 'loan-approval-ml-service',
        'model_status': model_status
    }), 200

@app.route('/predict', methods=['POST'])
def predict():
    if model_pipeline is None:
        return jsonify({'message': 'ML Model not loaded on server'}), 500
        
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
        # predict_proba returns [prob_class_0, prob_class_1]
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
            
        print(f"Prediction computed for {borrower_name}: status={status}, prob={prob_approved:.4f}")
        
        return jsonify({
            'probability': prob_approved,
            'status': status,
            'riskRating': risk_rating
        }), 200
        
    except (TypeError, ValueError) as val_err:
        return jsonify({'message': f'Invalid parameter formats: {val_err}'}), 400
    except Exception as e:
        print(f"Prediction failed: {e}")
        return jsonify({'message': f'Error computing prediction: {e}'}), 500

if __name__ == '__main__':
    # Host on port 5000 by default (matching docker-compose)
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
