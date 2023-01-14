import functools

from flask import(
    Blueprint, flash, g , redirect, render_template, request, session, url_for, jsonify, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash
from frontend.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None

        if not email:
            error = 'Die Email Adresse muss angegeben werden.'
        elif not password:
            error = 'Bitte ein Passwort eingeben.'
        
        if error is None:
            try:
                #This way SQL-Lite3 DB driver takes over sanitizing User Inputs
                db.execute(
                    "INSERT INTO user (email, password, permission_id) VALUES (?, ?, ?)",
                    (email, generate_password_hash(password), -1),
                )
                db.commit()
            except db.IntegrityError:
                error = f"Die Email {email} ist bereits registriert."
            else:
                return redirect(url_for('auth.login'))
        flash(error)
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT id, email, password FROM user WHERE email = ?', (email,)
        ).fetchone()

        if user is None:
            error = 'Diese Email ist noch nicht bei uns registriert.'
        elif not check_password_hash(user['password'], password):
            error = 'Das eingegebene Passwort ist falsch.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)
    
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT id, email, password, permission_id FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    """Decorator for other views (not in this blueprint) which require to be logged in..."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    
    return wrapped_view

@bp.route('/accounts')
@login_required
def accounts():
    #nur admins!
    if g.user['permission_id'] >= 2:
        db = get_db()
        #list of tuples
        accounts = db.execute(
            'SELECT T_User.id, T_User.email, T_User.password, T_User.permission_id, T_Permission.id, T_Permission.permission_name FROM user T_User INNER JOIN permission T_Permission ON T_User.permission_id = T_Permission.id ORDER BY T_User.id'
        ).fetchall()
        permissions = db.execute(
            'SELECT id, permission_name FROM permission ORDER BY id'
        ).fetchall()
        return render_template('auth/accounts.html', accounts=accounts, permissions=permissions, base_url=current_app.config['BASE_URL'])
    else:
        return redirect(url_for('auth.login'))

@bp.route('/account', methods=['GET', 'POST', 'DELETE'])
@login_required
def account():
    #nur admins!
    #print('test1')
    if g.user['permission_id'] >= 2:
        user_form_id: int = int(request.args.get('id'))
        if request.method == 'GET':
            db = get_db()
            user_form_id: int = int(request.args.get('id'))
            user_form_mail: str = request.args.get('email')
            user_form_permission_id: int = int(request.args.get('permId'))

            account = db.execute(
                f'SELECT id, email, permission_id FROM user WHERE id = {user_form_id}'
            ).fetchone()
            return jsonify({'id':account['id'], 'email':account['email'], 'permission_id':account['permission_id']})
        elif request.method == 'POST':
            user_form_mail: str = request.args.get('email')
            user_form_permission_id: int = int(request.args.get('permId'))
            try:
                db = get_db()
                db.execute(f"UPDATE user SET email = '{user_form_mail}', permission_id = {user_form_permission_id} WHERE id = {user_form_id}")
                db.commit()
                return jsonify({'update_successful':True})
            except db.IntegrityError:
                return jsonify({'update_successful':False})
        elif request.method == 'DELETE':
            try:
                db = get_db()
                db.execute(f"DELETE FROM user WHERE id = {user_form_id}")
                db.commit()
                return jsonify({'delete_successful':True})
            except db.IntegrityError:
                return jsonify({'delete_successful':False})
    else:
        return redirect(url_for('auth.login'))