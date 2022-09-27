from flask import Flask
from endpoints.prediction import prediction_api

app = Flask(__name__)
# Register prediction Blueprint
app.register_blueprint(prediction_api)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='1313')
