from flask import *
from functools import wraps

main = Blueprint("main", __name__, template_folder='templates')


@main.route("/")
def test():
    return redirect(url_for('main.login_page'))


@main.route("/login", methods=['GET'])
def login_page():
    next_page = request.args.get('next', None)

    if next_page:
        session['next_page'] = next_page

    return render_template("main/login.html")


@main.route("/logout")
def logout_page():
    session.clear()

    return redirect(url_for('main.login_page'))
