from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('land_area', type=int, location='args')
parser.add_argument('n_bathrooms', type=int, location='args')

class Predictor(Resource):
    ##self.model = load_model(....)
    def get(self):
        args = parser.parse_args()
        land_area: int = args['land_area']
        n_bathrooms: int = args['n_bathrooms']
        print(n_bathrooms)
        #prediction = model.predict(land_area, n_bathrooms)
        #--FAKE MODEL-----------------------
        import random
        prediction: int = random.randint(400000, 2000000)
        #-----------------------------------
        return {'prediction': prediction,'land_area': land_area,'n_bathrooms': n_bathrooms}

api.add_resource(Predictor, '/')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)