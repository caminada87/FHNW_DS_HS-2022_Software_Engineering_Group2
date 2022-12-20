import pickle
import pandas as pd
from geopy.geocoders import Nominatim

from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)

class GeoLocation(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('postal_code', type=int, location='args', default=5420)
        self.parser.add_argument('city', type=str, location='args', default='Ehrendingen')
        self.parser.add_argument('street_address', type=str, location='args', default='Hauptstrasse')
        self.parser.add_argument('street_num', type=str, location='args', default='1A')
    def get(self):
        args = self.parser.parse_args()

        postal_code: int = int(args['postal_code'])
        city: str = str(args['city'])
        street_address: str = str(args['street_address'])
        street_num: str = str(args['street_num'])
        geolocator = Nominatim(user_agent="housprice_agent")
        loc = geolocator.geocode(f'{street_num}, {street_address}, {city}, {postal_code}, Schweiz')
        answer = jsonify({'latitude': loc.latitude, 'longitude': loc.longitude})
        print(answer)
        return answer

class Predictor(Resource):
    def __init__(self):
        self.filename: str = r'.\data_science\model\decision_tree_model.sav'
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('longitude', type=float, location='args', default=0.0)
        self.parser.add_argument('latitude', type=float, location='args', default=0.0)
        self.parser.add_argument('postal_code', type=int, location='args', default=5420)
        self.parser.add_argument('city', type=str, location='args', default='Ehrendingen')
        self.parser.add_argument('bulding_category', type=str, location='args', default='Einfamilienhaus')
        self.parser.add_argument('build_year', type=int, location='args', default=2000)
        self.parser.add_argument('living_area', type=float, location='args', default=200.0)
        self.parser.add_argument('num_rooms', type=float, location='args', default=7)

        with open(self.filename, 'rb') as pickle_file:
            self.model = pickle.load(pickle_file)

    def get(self):
        args = self.parser.parse_args()

        long: float = float(args['longitude'])
        lat: float = float(args['latitude'])
        zipcode: int = int(args['postal_code'])
        municipality_name: str = str(args['city'])
        object_type_name: str = str(args['bulding_category'])
        build_year: int = int(args['build_year'])
        living_area: float = float(args['living_area'])
        num_rooms: float = float(args['num_rooms'])

        request_dict = {'long': long, 
                        'lat': lat, 
                        'zipcode': zipcode, 
                        'municipality_name': municipality_name,
                        'object_type_name': object_type_name, 
                        'build_year': build_year,
                        'living_area': living_area, 
                        'num_rooms': num_rooms}

        data_frame= pd.DataFrame(data=request_dict, index=[0])
        prediction: float = self.model.predict(data_frame)[0]
        request_dict['prediction']=prediction
        answer = jsonify(request_dict)

        #print (request_dict)
        return answer

api.add_resource(Predictor, '/')
api.add_resource(GeoLocation, '/GeoLocation')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)