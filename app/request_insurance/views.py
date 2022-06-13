from . import request_insurance
from flask import render_template, redirect, url_for, request, jsonify
from flask_login import current_user

import requests
import time

from app.databases.models_insurance import Base as BaseMech
from app.databases.database_insurance import SessionLocal as SessionLocal
from app.databases.database_insurance import engine as Engine
from app.databases.models_insurance import OsagoOsk, VoditelOsk, StatusOsago, StatusServer, OsagoUGSK, User, Osago21, Voditel21, OsagoArm, OsagoAlfa, VoditelAlfa, OsagoVsk, VoditelVsk

from functools import wraps
from app.databases.db_bot_methods import power_osago, duplicate_osago, add_favorites, del_favorites, transit_osago, stop_osago_for_change_status, transit_to_success, \
    check_reg_date, set_in_job, set_selected_oformitel, set_selected_otv, transit_to_active, transit_to_delete, deep_delete_osago, get_exemp_by_type_osago
from contextlib import suppress
from app import socketio
from flask_socketio import join_room, leave_room, send, emit
from sqlalchemy.orm import joinedload
from sqlalchemy import or_, and_


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated != True:
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@request_insurance.route('table_request', methods=['post', 'get'])
@login_required
def table_request():
    db = SessionLocal()

    if request.method == 'POST':
        print(request.form)

        if request.form["type_action"] == "edit":
            return redirect(url_for(f"{request.form['type_osago'].replace('osago_', '')}.redact_request", **request.form))
        elif request.form["type_action"] == "success":
            transit_to_success(type_osago=request.form["type_osago"], osago_id=request.form["id"])
        elif request.form["type_action"] == "delete":
            transit_to_delete(type_osago=request.form["type_osago"], osago_id=request.form["id"])
        elif request.form["type_action"] == "active":
            transit_to_active(type_osago=request.form["type_osago"], osago_id=request.form["id"])
        elif request.form["type_action"] == "deep_delete":
            deep_delete_osago(type_osago=request.form["type_osago"], osago_id=request.form["id"])
        elif request.form["type_action"] == "power":
            power_osago(type_osago=request.form["type_osago"], osago_id=request.form["id"])
        elif request.form["type_action"] == "add_favorites":
            add_favorites(type_osago=request.form["type_osago"], osago_id=request.form["id"])
        elif request.form["type_action"] == "del_favorites":
            del_favorites(type_osago=request.form["type_osago"], osago_id=request.form["id"])
        elif request.form["type_action"].find("to_") != -1:
            transit_osago(type_osago=request.form["type_osago"], osago_id=request.form["id"], type_osago_to=f"osago_{request.form['type_action'].replace('to_', '')}")
        elif request.form["type_action"] == "duplicate":
            duplicate_osago(type_osago=request.form["type_osago"], osago_id=request.form["id"], count=1)
        # ---------------------------------Set in job ------------------------------------------------------------------
        elif request.form["type_action"] == "set_in_job":
            set_in_job(type_osago=request.form["type_osago"], osago_id=request.form["id"])
        # ---------------------------------Multiply---------------------------------------------------------------------
        if request.json != None and request.json.get("type_action") == "multiply_power":
            for a in request.json["ids"]:
                with suppress(Exception):
                    power_osago(type_osago=a["type_osago"], osago_id=a["id"])
        elif request.form["type_action"] == "start_multiply_osago":
            for osago in request.form.keys():
                if osago.find("checkbox_osago_") != -1:
                    type_osago = "_".join(osago.replace("checkbox_osago_", "").split("_")[0:2])
                    osago_id = osago.replace("checkbox_osago_", "").split("_")[-1]
                    power_osago(type_osago=type_osago, osago_id=osago_id)
        return redirect(url_for('request_insurance.table_request', **request.args))

    count_free_servers = len(db.query(StatusServer).filter_by(id=2).first().servers)
    if request.args["status_request"] == "active":
        check_reg_date()
        all_osago = []
        if current_user.role_id == 1 or current_user.role_id == 3:
            for osago in \
                    db.query(OsagoVsk).filter(and_(OsagoVsk.is_main_osago, and_(OsagoVsk.status_osago_id != 4, OsagoVsk.status_osago_id != 5))).all() + \
                    db.query(OsagoAlfa).filter(and_(OsagoAlfa.is_main_osago, and_(OsagoAlfa.status_osago_id != 4, OsagoAlfa.status_osago_id != 5))).all():
                all_osago.append(osago)
        else:
            for osago in db.query(OsagoVsk).filter(and_(OsagoVsk.is_main_osago, and_(OsagoVsk.status_osago_id != 4, OsagoVsk.status_osago_id != 5))).filter_by(user_id=current_user.id).all() + \
                         db.query(OsagoAlfa).filter(and_(OsagoAlfa.is_main_osago, and_(OsagoAlfa.status_osago_id != 4, OsagoAlfa.status_osago_id != 5))).filter_by(user_id=current_user.id).all():
                all_osago.append(osago)
        print(all_osago)
        all_users = db.query(User).filter_by().all()
        return render_template('request_insurance/active_request.html', all_osago=all_osago, count_free_servers=count_free_servers, all_users=all_users)
    elif request.args["status_request"] == "success":
        if current_user.role_id == 1 or current_user.role_id == 3:
            all_osago = db.query(StatusOsago).filter_by(id=4).first().osago
        else:
            all_osago = db.query(User).filter_by(username=current_user.username).first().osago_success
        return render_template('request_insurance/success_request.html', all_osago=all_osago)
    elif request.args["status_request"] == "delete":
        if current_user.role_id == 1 or current_user.role_id == 3:
            all_osago = db.query(StatusOsago).filter_by(id=5).first().osago
        else:
            all_osago = db.query(User).filter_by(username=current_user.username).first().osago_delete
        return render_template('request_insurance/deleted_request.html', all_osago=all_osago)

@request_insurance.route('load_osago', methods=['post', 'get'])
@login_required
def load_osago():
    db = SessionLocal()
    osago = db.query(get_exemp_by_type_osago(type_osago=request.json["osago_type"])).filter_by(id=request.json["osago_id"]).first()

    dict_data = {}
    dict_data["login_parea"] = osago.login_parea
    dict_data["password_parea"] = osago.password_parea
    dict_data["strah_comp"] = osago.strah_comp
    try:
        dict_data["server_address"] = osago.server.server_address
    except:
        dict_data["server_address"] = ""
    dict_data["status_bot"] = osago.status_bot

    return jsonify(dict_data)

@socketio.on('join')
def on_join():
    join_room(current_user.username)
    emit("message_server", {"message": current_user.username + ' has entered the room.'}, to=current_user.username)

@socketio.on('selected_oformitel')
def selected_oformitel(data):
    print(data)
    set_selected_oformitel(user_id=current_user.id, oformitel_name=data['oformitel_name'])

@socketio.on('selected_otv')
def selected_otv(data):
    print(data)
    set_selected_otv(user_id=current_user.id, otv_name=data['otv_name'])

