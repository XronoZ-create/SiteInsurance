from . import main
from flask import render_template, redirect, url_for, request
from flask_login import current_user

from functools import wraps



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated != True:
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@main.route('/')
@login_required
def index():
    return render_template('index.html')