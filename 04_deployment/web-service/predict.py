import pickle
from flask import Flask, request, jsonify

# Load the model and the dictionary vectorizer from the pickle file
with open('lin_reg.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)

# Prepare features for the model input
def prepare_features(ride):
    features = {}
    features['PU_DO'] = '%s_%s' % (ride['PULocationID'], ride['DOLocationID'])
    features['trip_distance'] = ride['trip_distance']
    return features

# Predict the duration based on the features
def predict(features):
    X = dv.transform(features)
    preds = model.predict(X)
    return preds[0]

# Create the Flask instance
app = Flask('duration_prediction')

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    ride = request.get_json()
    features = prepare_features(ride)
    pred = predict(features)
    
    result = {
        'duration': pred
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)
