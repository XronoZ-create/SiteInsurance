from . import hooker
from flask import render_template, redirect, url_for, request, jsonify
from flask_login import current_user
import requests
import time

from app.databases.models_insurance import Base
from app.databases.database_insurance import SessionLocal
from app.databases.database_insurance import engine
from app.databases.models_insurance import Hook, StatusServer, User

from app.strah_comps import list_strah_comps

from functools import wraps

from app.databases.db_bot_methods import power_hook
from contextlib import suppress

from app import socketio
from flask_socketio import join_room, leave_room, send, emit

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated != True:
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@hooker.route('add', methods=['post', 'get'])
@login_required
def add():
    if request.method == 'POST':
        print(request.form)
        db = SessionLocal()

        strah_comp = []
        for key_form in request.form.keys():
            if key_form in list_strah_comps:
                strah_comp.append(key_form)
        print(strah_comp)

        user_id = db.query(User).filter_by(username=current_user.username).first().id
        new_hook = Hook(
            user_id=user_id,
            input_url=request.form["input_url"],
            strah_comp=",".join(strah_comp),
            name=request.form["name"]
        )
        db.add(new_hook)
        db.commit()
        return redirect(url_for('hooker.table_request', status_request="active"))
    else:
        return render_template('hooker/add.html', strah_comps=list_strah_comps)

@hooker.route('table_request', methods=['post', 'get'])
@login_required
def table_request():
    db = SessionLocal()

    if request.method == 'POST':
        print(request.form)
        if request.form["type_action"] == "edit":
            return redirect(url_for("hooker.redact_request", **request.form))
        elif request.form["type_action"] == "delete":
            hook = db.query(Hook).filter_by(id=request.form["id"]).first()

            with suppress(Exception):
                server = hook.server
                server.status_server = db.query(StatusServer).filter_by(name='Свободен').first()

            db.delete(hook)
            db.commit()
        elif request.form["type_action"] == "power":
            power_hook(hook_id=request.form["id"])
        return redirect(url_for('hooker.table_request', **request.args))

    if request.args["status_request"] == "active":
        count_free_servers = len(db.query(StatusServer).filter_by(id=2).first().servers)
        if current_user.username == "admin":
            all_hook = db.query(Hook).filter_by().all()
        else:
            all_hook = db.query(User).filter_by(username=current_user.username).first().hook
        return render_template('hooker/active_request.html', all_hook=all_hook, count_free_servers=count_free_servers)

@hooker.route('redact_request', methods=['post', 'get'])
@login_required
def redact_request():
    if request.method == 'POST':
        print(request.form)
        db = SessionLocal()

        strah_comp = []
        for key_form in request.form.keys():
            if key_form in list_strah_comps:
                strah_comp.append(key_form)
        print(strah_comp)

        edit_hook = db.query(Hook).filter_by(id=request.form['id'])

        edit_hook.update({
            'name': request.form["name"],
            'input_url': request.form["input_url"],
            'strah_comp': ",".join(strah_comp),
        })
        db.commit()
        return redirect(url_for('hooker.table_request', status_request="active"))
    else:
        db = SessionLocal()
        hook = db.query(Hook).filter_by(id=request.args["id"]).first()

        return render_template('hooker/edit.html', hook=hook, strah_comps=list_strah_comps)

@socketio.on('join')
def on_join():
    join_room(current_user.username)
    emit("message_server", {"message": current_user.username + ' has entered the room.'}, to=current_user.username)