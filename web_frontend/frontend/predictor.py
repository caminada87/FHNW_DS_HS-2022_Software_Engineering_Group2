import os
import pickle
import pandas as pd
from flask import jsonify
from flask_restful import Resource, reqparse
from flask import current_app
from .auth import login_required

class HousePricePrediction(Resource):
    def __init__(self):
        self.filename: str = current_app.config['MODEL']
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

        #print(self.filename)

        longitude: float = float(args['longitude'])
        latitude: float = float(args['latitude'])
        postal_code: int = int(args['postal_code'])
        city: str = str(args['city'])
        bulding_category: str = str(args['bulding_category'])
        build_year: int = int(args['build_year'])
        living_area: float = float(args['living_area'])
        num_rooms: float = float(args['num_rooms'])

        request_dict = {'long': longitude, 
                        'lat': latitude, 
                        'zipcode': postal_code, 
                        'municipality_name': city,
                        'object_type_name': bulding_category, 
                        'build_year': build_year,
                        'living_area': living_area, 
                        'num_rooms': num_rooms}

        data_frame= pd.DataFrame(data=request_dict, index=[0])
        prediction: int = int(self.model.predict(data_frame)[0])
        print ('Antwort:')
        print (prediction)
        answer = jsonify({'predicted_price': prediction})
        return answer