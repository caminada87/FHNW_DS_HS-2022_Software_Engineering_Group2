from flask import (
    Blueprint,
    g,
    redirect,
    render_template,
    request,
    url_for,
    jsonify,
    current_app,
)

from frontend.auth import login_required
from frontend.db import get_db
from werkzeug import Response

bp = Blueprint("accounts", __name__, url_prefix="/accounts")


@bp.route("/accounts")
@login_required
def accounts() -> str | Response:
    """
    Load account site.
    @rtype: object
    """
    # only for administrator
    if g.user["permission_id"] >= 2:
        db = get_db()
        # list of tuples
        ad_accounts = db.execute(
            "SELECT T_User.id, T_User.email, T_User.password, "
            "T_User.permission_id, T_Permission.id, "
            "T_Permission.permission_name "
            "FROM user T_User "
            "INNER JOIN permission T_Permission "
            "ON T_User.permission_id = T_Permission.id ORDER BY T_User.id"
        ).fetchall()
        permissions = db.execute(
            "SELECT id, permission_name FROM permission ORDER BY id"
        ).fetchall()
        return render_template(
            "auth/accounts.html",
            accounts=ad_accounts,
            permissions=permissions,
            base_url=current_app.config["BASE_URL"],
        )
    else:
        return redirect(url_for("auth.login"))


@bp.route("/account", methods=["GET", "POST", "DELETE"])
@login_required
def account() -> Response | Response:
    """
    Enable user management.
    @return:None
    """
    # only for administrators
    if g.user["permission_id"] >= 2:
        user_form_id: int = int(request.args.get("id"))
        if request.method == "GET":
            db = get_db()
            user_form_id: int = int(request.args.get("id"))
            user_form_mail: str = request.args.get("email")
            user_form_permission_id: int = int(request.args.get("permId"))

            ad_account = db.execute(
                f"SELECT id, email, permission_id "
                f"FROM user "
                f"WHERE id = {user_form_id} "
            ).fetchone()
            return jsonify(
                {
                    "id": ad_account["id"],
                    "email": ad_account["email"],
                    "permission_id": ad_account["permission_id"],
                }
            )
        elif request.method == "POST":
            user_form_mail: str = request.args.get("email")
            user_form_permission_id: int = int(request.args.get("permId"))
            try:
                db = get_db()
                db.execute(
                    f"UPDATE user SET email = '{user_form_mail}', "
                    f"permission_id = {user_form_permission_id} "
                    f"WHERE id = {user_form_id}"
                )
                db.commit()
                return jsonify({"update_successful": True})
            except db.IntegrityError:
                return jsonify({"update_successful": False})
        elif request.method == "DELETE":
            try:
                db = get_db()
                db.execute(f"DELETE FROM user WHERE id = {user_form_id}")
                db.commit()
                return jsonify({"delete_successful": True})
            except db.IntegrityError:
                return jsonify({"delete_successful": False})
        else:
            pass
    else:
        return redirect(url_for("auth.login"))
