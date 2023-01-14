import os
import sys
import pickle
import pandas as pd
import json
from flask import jsonify, g
from flask_restful import Resource, reqparse
from flask import current_app
from .auth import login_required
from frontend.db import get_db


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
        self.parser.add_argument('user_id', type=int, location='args', default=0)

        with open(self.filename, 'rb') as pickle_file:
            self.model = pickle.load(pickle_file)

    def get(self):
        predictions = []
        args = self.parser.parse_args()
        
        request_dict = {'long': float(args['longitude']),
                        'lat': float(args['latitude']),
                        'zipcode': int(args['postal_code']),
                        'municipality_name': str(args['city']),
                        'object_type_name': str(args['bulding_category']),
                        'build_year': int(args['build_year']),
                        'living_area': float(args['living_area']),
                        'num_rooms':  float(args['num_rooms'])}
        
        request_json = json.dumps(request_dict)
        
        db = get_db()
        predictions_db = db.execute(
            'SELECT id, user_id, query_data, predicted_price FROM predictions WHERE query_data = ?', (request_json,)
        ).fetchall()

        for prediction in predictions_db:
            prediction_dict = {'id': int(prediction['id']),
                'user_id': int(prediction['user_id']),
                'query_data': str(prediction['query_data']),
                'predicted_price': str(prediction['predicted_price'])
            }
            predictions.append(prediction_dict)
        print(len(predictions))
        if len(predictions) == 0:
            return '', 204
        return jsonify(predictions), 200

    def put(self):
        args = self.parser.parse_args()
        
        request_dict = {'long': float(args['longitude']),
                        'lat': float(args['latitude']),
                        'zipcode': int(args['postal_code']),
                        'municipality_name': str(args['city']),
                        'object_type_name': str(args['bulding_category']),
                        'build_year': int(args['build_year']),
                        'living_area': float(args['living_area']),
                        'num_rooms':  float(args['num_rooms'])}

        data_frame = pd.DataFrame(data=request_dict, index=[0])
        prediction: int = int(self.model.predict(data_frame)[0])
        request_json = json.dumps(request_dict)
        response_json = json.dumps({'predicted_price': prediction})

        db = get_db()
        db.execute(f"INSERT INTO predictions (user_id, query_data, predicted_price) VALUES (?,?,?)",
            (args['user_id'], request_json, response_json,)
        )
        db.commit()

        answer = jsonify( {'predicted_price': prediction} )
        return answer
