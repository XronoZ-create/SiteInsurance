from flask import render_template, redirect, request, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app.databases.models_insurance import User
from . import auth
from .forms import LoginForm

from app.databases.models_insurance import Base as BaseSite
from app.databases.database_insurance import SessionLocal
from app.databases.database_insurance import engine as EngineSite

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form)
        db = SessionLocal()
        user = db.query(User).filter_by(username=request.form["username"]).first()
        if user is not None and user.verify_password(request.form["password"]):
            if request.form.get("remember") != None:
                remember = True
            else:
                remember = False
            login_user(user, remember)
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('Неправильный пароль или имя.')
            db.close()
    return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли.')
    return redirect(url_for('auth.login'))

