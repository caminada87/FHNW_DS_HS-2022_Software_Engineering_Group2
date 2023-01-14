from flask import(
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from werkzeug.exceptions import abort

from frontend.auth import login_required
from frontend.db import get_db

import json
import urlfetch

bp = Blueprint('prediction', __name__)

@bp.route('/', methods=('GET', 'POST'))
@login_required
def index()->str:
    if request.method == 'POST':
        params: dict = {'longitude':request.form['longitude'],
                'latitude':request.form['latitude'],
                'postal_code':request.form['postal_code'],
                'city':request.form['city'],
                'bulding_category':request.form['bulding_category'],
                'build_year':request.form['build_year'],
                'living_area':request.form['living_area'],
                'num_rooms':request.form['num_rooms'],
                'user_id':g.user['id']
        }

        response = urlfetch.fetch(
            url= f"{current_app.config['BASE_URL']}/HousePricePrediction",
            params=params,
            method=urlfetch.GET,
            validate_certificate=True
        )

        if response.status_code == 204:
            response = urlfetch.fetch(
                url=f"{current_app.config['BASE_URL']}/HousePricePrediction",
                contentType="application/json",
                params=params,
                method=urlfetch.PUT,
                validate_certificate=True
            )
        else:
            print('bereits geschätzt!')
        return redirect(url_for('prediction.recent'))
    else:
        return render_template('prediction/index.html', base_url=current_app.config['BASE_URL'])

@bp.route('/recent')
@login_required
def recent()->str:
    db = get_db()
    #list of tuples
    if g.user['permission_id'] >= 2:
        recent_predictions = db.execute(
            'SELECT id, user_id, query_data, predicted_price FROM predictions ORDER BY id DESC LIMIT 50'
        ).fetchall()
    else:
        recent_predictions = db.execute(
            f'SELECT id, user_id, query_data, predicted_price FROM predictions WHERE  ORDER BY id DESC LIMIT 50'
        ).fetchall()
    predictions: list = []
    for prediction in recent_predictions:
        query_data = json.loads(prediction['query_data'])
        prediction_data = json.loads(prediction['predicted_price'])

        predictions.append({'id': prediction['id'], 
                            'user_id': prediction['user_id'],
                            'long': query_data['long'],
                            'lat': query_data['lat'], 
                            'zipcode': query_data['zipcode'], 
                            'municipality_name': query_data['municipality_name'],
                            'object_type_name': query_data['object_type_name'],
                            'build_year': query_data['build_year'],
                            'living_area': query_data['living_area'],
                            'num_rooms': query_data['num_rooms'],
                            'prediction': prediction_data['predicted_price']
                          })
    return render_template('prediction/recent.html', recent_predictions=predictions)