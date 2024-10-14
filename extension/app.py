from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# Load trained models
random_forest_model = joblib.load('random_forest_model.pkl')
lgbm_model = joblib.load('LGBM_model.pkl')
xgboost_model = joblib.load('xgBoost_model.pkl')

@app.route('/detect-threat', methods=['POST'])
def detect_threat():
    # Get website features from the request
    website_features = request.json['website_features']
    
    # Perform inference using the loaded models
    rf_prediction = random_forest_model.predict([website_features])
    lgbm_prediction = lgbm_model.predict([website_features])
    xgboost_prediction = xgboost_model.predict([website_features])
    
    # Determine the threat based on model predictions
    if rf_prediction == 1:
        threat = 'Ransomware'
    elif lgbm_prediction == 1:
        threat = 'Phishing'
    elif xgboost_prediction == 1:
        threat = 'Trojan'
    else:
        threat = 'No Threat'
    
    return jsonify({'threat': threat})

if __name__ == '__main__':
    app.run(debug=True)
