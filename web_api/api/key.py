from flask import(
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from functools import wraps
from werkzeug.exceptions import abort

from api.auth import login_required
from api.db import get_db

import json
import uuid

bp = Blueprint('key', __name__, url_prefix='/key')

@bp.route('/', methods=('GET', 'POST'))
@login_required
def index()->str:
    db = get_db()

    if request.method == 'POST':
        app_name = request.form['app_name']
        try:
            db.execute(
                "INSERT INTO api_key (consumer_name, api_key, developer_id) VALUES (?, ?, ?)",
                (app_name, uuid.uuid4().hex, g.user['id']),
            )
            db.commit()
        except db.IntegrityError:
            error = f"Eine App mit dem Namen {app_name} ist bereits registriert."
        
    #Developer sees just his keys
    if g.user['permission_id'] == 0:
        api_keys = db.execute(
            f"SELECT T_api_key.id, T_api_key.consumer_name, T_api_key.api_key, T_developer.email FROM api_key T_api_key INNER JOIN developer T_developer ON T_api_key.developer_id = T_Developer.id WHERE developer_id = { g.user['id'] } ORDER BY T_api_key.id DESC"
        ).fetchall()
    #Admin sees every key
    elif  g.user['permission_id'] == 1:
        api_keys = db.execute(
            f"SELECT T_api_key.id, T_api_key.consumer_name, T_api_key.api_key, T_developer.email FROM api_key T_api_key INNER JOIN developer T_developer ON T_api_key.developer_id = T_Developer.id ORDER BY T_api_key.id DESC"
        ).fetchall()
    
    return render_template('key/index.html', api_keys=api_keys)

# The actual decorator function
def api_key_required(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        if request.headers.get('app-name') and request.headers.get('api-key'):
            db = get_db()
            requested_app_name = request.headers.get('app-name')
            api_key = db.execute(
                f'SELECT api_key from api_key WHERE consumer_name = ?',
                (requested_app_name,)
            ).fetchone()
            if request.headers.get('api-key') == api_key['api_key']:
                return view_function(*args, **kwargs)
            else:
                abort(401)
        else:
            print(f"hallo2: {request.headers.get('app-name')}")
            abort(401)
    return decorated_function