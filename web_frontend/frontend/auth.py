import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,
    jsonify, current_app
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
                # This way SQL-Lite3 DB driver takes over sanitizing User Inputs
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
            'SELECT id, email, password, permission_id FROM user WHERE id = ?',
            (user_id,)
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