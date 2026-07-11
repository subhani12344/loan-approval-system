# Loan Approval Prediction & HDI Estimation System

A sophisticated, AI-powered financial risk assessment platform and Human Development Index (HDI) estimation portal. This system is designed around a modern full-stack architecture combining a TypeScript/Express backend serving a dynamic SPA dashboard with a Python Flask machine learning microservice.

---

## 🏗️ Architecture & Project Structure

The project separates the web server and database logging layer from the machine learning inference services, ensuring high scalability and modularity.

```text
loan-approval-system/
├── ml-service/                 # Python Machine Learning microservice
│   ├── .venv/                  # Python 3.11 Virtual Environment
│   ├── templates/              # HTML Templates for Flask app
│   │   ├── home.html           # Introduction page
│   │   └── indexnew.html       # Estimator form interface
│   ├── app.py                  # Flask Web API & template router
│   ├── clean_and_transform.py  # Missing values & Categorical Label Encoding script
│   ├── download_and_explore.py  # HDI Dataset downloader and visualizer (Matplotlib/Seaborn)
│   ├── generate_predictions.py # Validation test set prediction arrays script
│   ├── split_data.py           # 80/20 train/test splitter script
│   ├── train.py                # RandomForest classification training script
│   ├── train_regression.py     # LinearRegression model training script
│   └── requirements.txt        # Pinned packages (scikit-learn, pandas, numpy, seaborn, etc.)
├── models/                     # Serialized Model Pipelines (Pickle format)
│   ├── hdi_prediction_model.pkl# RandomForest classification pipeline
│   ├── hdi_regression_model.pkl# LinearRegression model
│   └── plots/                  # Generated correlation and distribution plots
├── src/                        # Express Backend & SPA Frontend
│   ├── config/
│   │   └── db.ts               # Mongoose database connector
│   ├── models/
│   │   └── Loan.ts             # Loan Mongo database Schema definition
│   ├── public/                 # Static web client (served by Express)
│   │   ├── app.js              # Client dashboard script controller
│   │   ├── index.css           # Glassmorphism dark mode stylesheet
│   │   └── index.html          # Semantic HTML dashboard template
│   └── server/
│       ├── routes/
│       │   └── loanRoutes.ts   # Express prediction & statistics routes
│       └── index.ts            # Entrypoint file for Express backend
├── .env                        # Local environment variables
├── .gitignore                  # Git ignore files configuration
├── package.json                # Node/NPM package configuration
├── tsconfig.json               # TypeScript compiler config
└── README.md                   # This document
```

---

## 📈 Machine Learning Performance & Metrics

### 1. Classification (Random Forest Model)
- **Objective**: Classify loan applications into `APPROVED` or `REJECTED` categories.
- **Features Used**: `income`, `credit_score`, `loan_amount`, `loan_term`, `hdi_index`, `age`.
- **Accuracy**: **94.50%** on the validation set.

### 2. Regression (Linear Regression Model)
- **Objective**: Estimate the continuous Human Development Index (HDI) Score based on social development metrics.
- **Features Used**: `Country`, `Life Expectancy`, `Mean Years of Schooling`, `Expected Years of Schooling`, `GNI per Capita`.
- **R² Score (R-squared)**: **96.38%** (96.38% of index variance is explained by input features).
- **Mean Absolute Error (MAE)**: **0.028979**
- **Root Mean Squared Error (RMSE)**: **0.034141**

---

## 🚀 Execution & Setup Instructions

### Prerequisites
- Node.js (v18+)
- Python 3.11
- MongoDB (optional, fallback in-memory cache is fully operational)

### 1. Launch Python Flask ML Service
```powershell
cd ml-service
# Activate the virtual environment
.\.venv\Scripts\activate
# Start the web app
python app.py
```
*The Flask app runs on `http://localhost:5000`.*
- Navigate to `http://localhost:5000/` in your browser to launch the HDI Predictor form interface.
- Navigating to `/predict-form` displays the input form templates serving the Linear Regression predictions.

### 2. Launch Express Backend & Dashboard
```powershell
# In the project root directory
npm install
npm run dev
```
*The Express server runs on `http://localhost:3000`.*
- Open `http://localhost:3000/` to submit credit applications and view live predictions and aggregate statistical charts.

---

## 📊 Summary: A Comprehensive Measure of Well-Being

A Comprehensive Measure of Well-Being provides a holistic view of quality of life by evaluating multiple dimensions that influence an individual's overall welfare, rather than relying solely on traditional economic indicators such as income or GDP. It encompasses a wide range of factors, including physical and mental health, educational attainment, financial stability, employment opportunities, social relationships, environmental quality, personal safety, and overall life satisfaction.

By integrating these diverse aspects, a comprehensive well-being framework offers a more accurate and meaningful assessment of how individuals and communities are truly thriving. It helps uncover hidden challenges that may not be reflected through economic measures alone, while also highlighting strengths and opportunities for growth.

This multidimensional approach enables policymakers, researchers, healthcare professionals, and organizations to make informed decisions, design effective interventions, and allocate resources more efficiently. It also supports the development of strategies aimed at improving public health, reducing inequalities, enhancing social cohesion, and promoting sustainable development.

Ultimately, measuring well-being in a comprehensive manner contributes to building healthier, happier, and more resilient societies. By focusing on the factors that genuinely impact people's lives, it encourages balanced progress and helps create inclusive communities where individuals have the opportunity to achieve their full potential and enjoy a higher quality of life.

---

## 🔗 Live Deployments
* **GitHub Repository**: [https://github.com/subhani12344/loan-approval-system](https://github.com/subhani12344/loan-approval-system)
* **Express Backend & SPA Client Dashboard (Render)**: [https://loan-approval-system-ethi.onrender.com](https://loan-approval-system-ethi.onrender.com)