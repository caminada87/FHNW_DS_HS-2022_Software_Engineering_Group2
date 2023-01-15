
from geopy.geocoders import Nominatim
from flask import jsonify
from flask_restful import Resource, reqparse
from .auth import login_required

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

        # print(answer)
        return answer