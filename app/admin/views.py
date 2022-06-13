from . import admin
from flask import render_template, redirect, url_for, request, jsonify
from flask_login import current_user
import requests
import time

from app.databases.models_insurance import Base as BaseSite, Role, User, Config
from app.databases.database_insurance import SessionLocal
from app.databases.database_insurance import engine as Engine

from app.databases.database_email import SessionLocal as SessionLocalEmail
from app.admin.generate_email_address import generate_email_address
from app.databases.models_email import Email

from functools import wraps

def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated != True:
            return redirect(url_for('auth.login', next=request.url))
        elif current_user.role.name != "Админ":
            return render_template("admin/access_denied.html")
        return f(*args, **kwargs)
    return decorated_function

@admin.route('add_user', methods=['post', 'get'])
@admin_login_required
def add_user():
    if request.method == 'POST':
        print(request.form)
        db = SessionLocal()
        db_email = SessionLocalEmail()

        new_user = User(
            username=request.form["login"],
            password_hash=request.form["password"],

            surname=request.form["surname"],
            name=request.form["name"],
            otchestvo=request.form["otchestvo"],
            role_id=db.query(Role).filter_by(name=request.form["role"]).first().id,

            email_address=request.form["email_address"],
            email_password=request.form["email_password"]
        )
        db.add(new_user)
        db.commit()


        for one_address in generate_email_address(email_address=request.form["email_address"]):
            new_email = Email(
                email_address=one_address,
                email_password=request.form["email_password"],
                user_id=new_user.id
            )
            db_email.add(new_email)
        db.commit()
        db_email.commit()

        return render_template('admin/user_success_add.html')
    else:
        return render_template('admin/add_user.html')

@admin.route('users', methods=['post', 'get'])
@admin_login_required
def users():
    db = SessionLocal()
    db_email = SessionLocalEmail()

    if request.method == 'POST':
        print(request.form)

        if request.form["type_action"] == "edit":
            return redirect(url_for("admin.edit_user", **request.form))
        elif request.form["type_action"] == "delete":
            del_user = db.query(User).filter_by(id=request.form["id"]).first()
            for one_email in db_email.query(Email).filter_by(user_id=request.form["id"]).all():
                db_email.delete(one_email)
            db.delete(del_user)
            db.commit()
            db_email.commit()

    all_user = db.query(User).filter_by().all()

    return render_template('admin/users.html', all_user=all_user)

@admin.route('edit_user', methods=['post', 'get'])
@admin_login_required
def edit_user():
    if request.method == 'POST':
        print(request.form)
        db = SessionLocal()
        db_email = SessionLocalEmail()

        edit_user = db.query(User).filter_by(id=request.form['id'])

        if request.form["email_address"] != edit_user.first().email_address:
            for one_email in db_email.query(Email).filter_by(user_id=request.form["id"]).all():
                db_email.delete(one_email)
            for one_address in generate_email_address(email_address=request.form["email_address"])[:5000]:
                new_email = Email(
                    email_address=one_address,
                    email_password=request.form["email_password"],
                    user_id=request.form['id']
                )
                db_email.add(new_email)

        edit_user.update(
            {
                'username': request.form["login"],
                'password_hash': request.form["password"],
                'surname': request.form["surname"],
                'name': request.form["name"],
                'otchestvo': request.form["otchestvo"],
                'role_id': db.query(Role).filter_by(name=request.form["role"]).first().id,
                'email_address': request.form["email_address"],
                'email_password': request.form["email_password"]
            }
        )
        db.commit()
        db_email.commit()

        return render_template('admin/user_success_edit.html')
    else:
        db = SessionLocal()
        user = db.query(User).filter_by(id=request.args["id"]).first()

        return render_template('admin/edit_user.html', user=user)

@admin.route('config', methods=['post', 'get'])
@admin_login_required
def config():
    if request.method == 'POST':
        print(request.form)
        db = SessionLocal()
        db.query(Config).filter_by(name="telephone_service").first().value = request.form["telephone_service"]
        db.commit()
        return redirect(url_for('admin.config'))
    else:
        db = SessionLocal()
        telephone_service = db.query(Config).filter_by(name="telephone_service").first().value

        return render_template("admin/config.html", telephone_service=telephone_service)