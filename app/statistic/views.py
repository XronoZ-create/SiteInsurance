from . import statistic
from flask import render_template, redirect, url_for, request, jsonify
from flask_login import current_user
import requests
import time

from app.databases.models_insurance import Base as BaseSite, Role, User, Config, OsagoOsk, Osago21, OsagoUGSK, StatusOsago
from app.databases.database_insurance import SessionLocal
from app.databases.database_insurance import engine as Engine
from app.strah_comps import list_strah_comps
from datetime import datetime, timedelta

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

@statistic.route('info', methods=['post', 'get'])
@admin_login_required
def info():
    if request.method == 'POST':
        print(request.form)
        db = SessionLocal()

        all_doc_users = db.query(User).filter_by(role_id=2).all()
        all_users = db.query(User).filter_by().all()
        all_osago = db.query(StatusOsago).filter_by(id=4).first().osago

        post_args = {}
        all_osago_filter = list(all_osago)
        if request.form["date_start"] != "":
            post_args["selected_date"] = f'{request.form["date_start"]} - {request.form["date_end"]}'
            good_osagos = []
            for osago in all_osago_filter:
                if (datetime.strptime(osago.success_date, "%d.%m.%Y") - datetime.strptime(request.form["date_start"], "%d %b, %Y")) >= timedelta(minutes=0) and \
                    (datetime.strptime(request.form["date_end"], "%d %b, %Y") - datetime.strptime(osago.success_date, "%d.%m.%Y")) >= timedelta(minutes=0):
                    good_osagos.append(osago)
            all_osago_filter = good_osagos
        if request.form["oformitel"] != "":
            post_args["selected_oformitel"] = request.form["oformitel"]
            good_osagos = []
            for osago in all_osago_filter:
                if osago.oformitel_name == request.form["oformitel"]:
                    good_osagos.append(osago)
            all_osago_filter = good_osagos
        if request.form["CK_name"] != "":
            post_args["selected_CK"] = request.form["CK_name"]
            good_osagos = []
            for osago in all_osago_filter:
                if osago.type_osago == request.form["CK_name"]:
                    good_osagos.append(osago)
            all_osago_filter = good_osagos
        strah_comp = []
        for key_form in request.form.keys():
            if key_form in list_strah_comps:
                strah_comp.append(key_form)
        print(strah_comp)
        if len(strah_comp) != 0:
            post_args["selected_strah_comp"] = ", ".join(strah_comp)
            good_osagos = []
            for osago in all_osago_filter:
                if strah_comp.count(osago.strah_comp) != 0:
                    good_osagos.append(osago)
            all_osago_filter = good_osagos

        return render_template('statistic/info.html', all_doc_users=all_doc_users, strah_comps=list_strah_comps, all_osago=all_osago_filter, all_users=all_users,
                               **post_args)
    else:
        db = SessionLocal()

        all_doc_users = db.query(User).filter_by(role_id=2).all()
        all_users = db.query(User).filter_by().all()
        all_osago = db.query(StatusOsago).filter_by(id=4).first().osago

        date_start = f"01 {datetime.now().strftime('%b')}, {datetime.now().year}"
        date_end = f"{datetime.now().day} {datetime.now().strftime('%b')}, {datetime.now().year}"
        all_osago_filter = list(all_osago)
        post_args = {}
        post_args["selected_date"] = f'{date_start} - {date_end}'
        good_osagos = []
        for osago in all_osago_filter:
            if (datetime.strptime(osago.success_date, "%d.%m.%Y") - datetime.strptime(date_start, "%d %b, %Y")) >= timedelta(minutes=0) and \
                    (datetime.strptime(date_end, "%d %b, %Y") - datetime.strptime(osago.success_date, "%d.%m.%Y")) >= timedelta(minutes=0):
                good_osagos.append(osago)
        all_osago_filter = good_osagos

    return render_template('statistic/info.html', all_doc_users=all_doc_users, strah_comps=list_strah_comps, all_osago=all_osago_filter, all_users=all_users,
                           **post_args)