#importing various modules
import flask
from flask import jsonify, request
from flask_restful import Resource, Api

# Import model libraries
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle


#loading the model
loaded_model = None
with open('basic_classifier.pkl', 'rb') as fid:
    loaded_model = pickle.load(fid)
    
vectorizer = None
with open('count_vectorizer.pkl', 'rb') as vd:
    vectorizer = pickle.load(vd)


################################
#                              #
#                              #
#           API                #
#                              #
#                              # 
#                              #
# #############################
# Writing the api in falsk
application = flask.Flask(__name__)
api = Api(application)

class FakeNewsDetector(Resource):
    def get(self):
        if request.is_json:
            json_data = request.get_json(silent=True)
            if json_data:
                for key in json_data:
                    if not isinstance(key, str):
                        response = jsonify({'Error 400': 'Key is not valid!'})
                        response.status_code = 400
                        return response
                    if not isinstance(json_data[key], str):
                        response = jsonify({'Error 400': 'Value is not valid!'})
                        response.status_code = 400
                        return response
            else:
                ep = jsonify({'Error 400': 'json_data not fetched'})
                response.status_code = 400
                return response

            prediction_res = {}
            for key in json_data:
                if not loaded_model.predict(vectorizer.transform([json_data[key]]))[0] == 'REAL':
                    prediction_res[key] = 0
                else:
                    prediction_res[key] = 1
           
            
            response = jsonify(prediction_res)
            response.status_code = 200
            return response
            
        else:
            response = jsonify({'Error 400': 'NO Request'})
            response.status_code = 400
            return response

#The application will also work with /predict           
@application.route('/predict', methods=['GET'])
def predict():
    """ Predict whether the payload data is a fake news (1) or not (0)"""
    data = request.args.get('text')

    if data is None:
        response = jsonify({'error': 'No input data specified to predict result.'})
        response.status_code = 400
        return response
    
    # Do the prediction
    prediction = FakeNewsDetector.predict(data)
    result = {
        "prediction": prediction,
        "status_code": 200
    }
api.add_resource(FakeNewsDetector, '/')

if __name__ == '__main__':
    application.run()