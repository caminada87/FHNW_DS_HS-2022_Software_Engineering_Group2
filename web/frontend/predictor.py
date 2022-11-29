from flask import(
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from frontend.auth import login_required
from frontend.db import get_db

from requests import get

import json

bp = Blueprint('predictor', __name__)

@bp.route('/', methods=('GET', 'POST'))
def index()->str:
    if request.method == 'POST':
        land_area: int = request.form['land_area']
        n_bathrooms: int = request.form['n_bathrooms']
        response: str = get('http://localhost:5001/', params={'land_area':str(land_area), 'n_bathrooms':str(n_bathrooms)}, headers={'Content-Type': 'application/json'}).json()
        response_json = json.dumps(response) 
        db = get_db()
        db.execute(f"INSERT INTO prediction_query (user_data, query_data) VALUES ('{str(request.remote_addr)}', '{response_json}')")
        db.commit()
        return redirect(url_for('predictor.recent'))
        #return f"{response['land_area']}"
    else:
        return render_template('predictor/index.html')

@bp.route('/recent')
def recent()->str:
    db = get_db()
    #list of tuples
    recent_predictions = db.execute(
        'SELECT id, user_data, query_data FROM prediction_query ORDER BY id DESC LIMIT 50'
    ).fetchall()
    predictions: list = []
    for prediction in recent_predictions:
        query_data = json.loads(prediction['query_data'])
        import locale
        locale.setlocale(locale.LC_ALL, 'en_US')
        predictions.append({'id': str(prediction['id']), 'user_ip': prediction['user_data'], 'land_area': query_data['land_area'], 'n_bathrooms': query_data['n_bathrooms'], 'prediction': f"{query_data['prediction']:n}.- CHF".replace(',', '\'')})
    return render_template('predictor/recent.html', recent_predictions=predictions)