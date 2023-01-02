from flask import(
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from frontend.auth import login_required
from frontend.db import get_db

from requests import get

import json

bp = Blueprint('prediction', __name__)

@bp.route('/', methods=('GET', 'POST'))
def index()->str:
    if request.method == 'POST':
        longitude: float = request.form['longitude']
        latitude: float = request.form['latitude']
        postal_code: int = request.form['postal_code']
        city: str = request.form['city']
        bulding_category: str = request.form['bulding_category']
        build_year: int = request.form['build_year']
        living_area: float = request.form['living_area']
        num_rooms: float = request.form['num_rooms']

        params: dict = {'longitude':longitude,
                'latitude':latitude,
                'postal_code':postal_code,
                'city':city,
                'bulding_category':bulding_category,
                'build_year':build_year,
                'living_area':living_area,
                'num_rooms':num_rooms
        }

        params_json: str = json.dumps(params)
        #Doesn't work in Docker container:
        #response: dict = get('http://localhost:5000/HousePricePrediction', params=params, headers={'Content-Type': 'application/json'}).json()
        response: dict = get('http://0.0.0.0:5000/HousePricePrediction', params=params, headers={'Content-Type': 'application/json'}).json()
        response_json: str = json.dumps(response)
        db = get_db()
        db.execute(f"INSERT INTO predictions (user_ip, query_data, predicted_price) VALUES ('{str(request.remote_addr)}', '{params_json}', '{response_json}')")
        db.commit()
        return redirect(url_for('prediction.recent'))
    else:
        return render_template('prediction/index.html')

@bp.route('/recent')
def recent()->str:
    db = get_db()
    #list of tuples
    recent_predictions = db.execute(
        'SELECT id, user_ip, query_data, predicted_price FROM predictions ORDER BY id DESC LIMIT 50'
    ).fetchall()
    predictions: list = []
    for prediction in recent_predictions:
        query_data = json.loads(prediction['query_data'])
        prediction_data = json.loads(prediction['predicted_price'])
        import locale
        #Doesn't work in Docker container:
        #locale.setlocale(locale.LC_ALL, 'en_US.utf8')
        predictions.append({'id': str(prediction['id']), 
                            'user_ip': prediction['user_ip'],
                            'longitude': query_data['longitude'],
                            'latitude': query_data['latitude'], 
                            'postal_code': query_data['postal_code'], 
                            'city': query_data['city'],
                            'building_category': query_data['bulding_category'],
                            'build_year': query_data['build_year'],
                            'living_area': query_data['living_area'],
                            'num_rooms': query_data['num_rooms'],
                            #'prediction': f"{int(prediction_data['predicted_price']):n}.- CHF".replace(',', '\'')
                            'prediction' : prediction_data['predicted_price']
                          })
    return render_template('prediction/recent.html', recent_predictions=predictions)