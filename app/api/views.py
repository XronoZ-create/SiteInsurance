from . import api
from flask import render_template, redirect, url_for, request, jsonify
from flask_login import current_user
import requests
import time

from config import Config

from app.databases.models_insurance import Base as Base, Role, User
from app.databases.models_insurance import SessionLocal as SessionLocal
from app.databases.database_insurance import engine as Engine

from app.databases.models_insurance import OsagoOsk, VoditelOsk, StatusOsago

from functools import wraps

from app.databases import db_bot_methods

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated != True:
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def check_key(func):
    @wraps(func)
    def run():
        key = Config.API_KEY
        if request.get_json()['KEY'] == key:
            return func()
        else:
            return jsonify(exception="Failed"), 400
    return run

@api.route('/check_task', methods=['post'])
@check_key
def check_task():
    ip_address = request.remote_addr
    resp = db_bot_methods.check_task_server(server_address=ip_address)
    print(resp)
    return jsonify(resp)

@api.route('/set_status_bot', methods=['post'])
@check_key
def set_status_bot():
    ip_address = request.remote_addr
    db_bot_methods.set_status_bot(server_address=ip_address, status_bot=request.json["status_bot"])
    return jsonify(200)

@api.route('/add_server_bot', methods=['post'])
@check_key
def add_server():
    db_bot_methods.add_server_bot(server_address=request.json["server_address"])
    return jsonify(200)

@api.route('/set_value', methods=['post'])
@check_key
def set_value():
    data = db_bot_methods.set_value(name=request.json["name"], value=request.json["value"], type=request.json["type"], id=request.json["id"])
    return jsonify(data)

@api.route('/stop_osago', methods=['post'])
@check_key
def stop_osago():
    db_bot_methods.stop_osago(type_osago=request.json["type_osago"], osago_id=request.json["osago_id"])
    return jsonify(200)

@api.route('/stop_hook', methods=['post'])
@check_key
def stop_hook():
    db_bot_methods.stop_hook(hook_id=request.json["hook_id"])
    return jsonify(200)

@api.route('/telephone_service', methods=['post'])
@check_key
def telephone_service():
    telephone_service = db_bot_methods.get_telephone_service()
    return jsonify({"telephone_service": telephone_service})

@api.route('/change_email_address', methods=['post'])
@check_key
def change_email_address():
    data = db_bot_methods.change_email_address(type=request.json["type"], id=request.json["id"])
    return jsonify(data)

@api.route('/dadata_address', methods=['post'])
@login_required
def dadata_address():
    data = db_bot_methods.dadata_address(text_address=request.json["text_address"])
    return jsonify(data)



@api.route('/vsk_city', methods=['post'])
@login_required
def vsk_city():
    data = db_bot_methods.vsk_city(text_city=request.json["text_city"])
    return jsonify(data)

@api.route('/vsk_street', methods=['post'])
@login_required
def vsk_street():
    data = db_bot_methods.vsk_street(text_street=request.json["text_street"], fias_city=request.json["fias_city"])
    return jsonify(data)



# @api.route('/alfa_region', methods=['post'])
# @login_required
# def alfa_region():
#     data = db_bot_methods.alfa_region(text_region=request.json["text_region"])
#     return jsonify(data)
#
# @api.route('/alfa_city', methods=['post'])
# @login_required
# def alfa_city():
#     data = db_bot_methods.alfa_city(text_city=request.json["text_city"], kladr_id=request.json["kladr_id"])
#     return jsonify(data)
#
# @api.route('/alfa_street', methods=['post'])
# @login_required
# def alfa_street():
#     data = db_bot_methods.alfa_street(text_street=request.json["text_street"])
#     return jsonify(data)

