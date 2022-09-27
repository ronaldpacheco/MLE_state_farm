import pandas as pd
from flask import request, jsonify, Blueprint
import pickle
from data_prep import prep_data

# Create Flask Blueprint
prediction_api = Blueprint('prediction_api', __name__)

# Load model
with open('./model/model.pkl','rb') as mod:
    model = pickle.load(mod)


@prediction_api.route('/predict', methods=['POST'])
def predict():

    # Request json data
    data = pd.DataFrame(request.json)

    # Prepare the data for model
    data = prep_data(data)

    # Make prediction
    prediction = model.predict(data)
    # Create labels based on predictions (assuming threshold of 0.5)
    label = [1 if i >= 0.5 else 0 for i in prediction]
    # Return the required result
    return jsonify({'Probability': list(prediction), 'Label': list(label), 'Variables': list(data.columns)})
