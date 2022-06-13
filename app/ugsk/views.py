from . import ugsk
from flask import render_template, redirect, url_for, request, jsonify
from flask_login import current_user
from .mark import list_mark
import requests
import time
from app.strah_comps import list_strah_comps

from app.databases.models_insurance import Base
from app.databases.database_insurance import SessionLocal
from app.databases.database_insurance import engine as Engine
from app.databases.models_insurance import OsagoUGSK, VoditelUGSK, StatusOsago, User, Config

from app.databases.models_email import Base as BaseEmail
from app.databases.database_email import SessionLocal as SessionLocalEmail
from app.databases.database_email import engine as EngineEmail
from app.databases.models_email import Email

from functools import wraps



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated != True:
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@ugsk.route('add', methods=['post', 'get'])
@login_required
def add():
    if request.method == 'POST':
        print(request.form)
        db = SessionLocal()

        user_id = db.query(User).filter_by(username=current_user.username).first().id
        if request.form.get("oformitel") != None and request.form["oformitel"] != "":
            oformitel_id = db.query(User).filter_by(username=request.form["oformitel"]).first().id
        else:
            oformitel_id = None

        db_email = SessionLocalEmail()
        email = db_email.query(Email).filter_by(user_id=user_id).first()
        email_address = email.email_address
        email_password = email.email_password
        db_email.delete(email)
        db_email.commit()
        db_email.close()

        strah_comp = []
        for key_form in request.form.keys():
            if key_form in list_strah_comps:
                strah_comp.append(key_form)
        print(strah_comp)

        dict_data_voditel = {}
        for key_form, value_form in request.form.items():
            if key_form.find("vod") != -1:
                split_key = key_form.split("_")
                if dict_data_voditel.get(split_key[1]) == None:
                    dict_data_voditel[split_key[1]] = {}
                dict_data_voditel[split_key[1]][split_key[2]] = value_form
        print(dict_data_voditel)

        if request.form.get("sobstv_yavl_strah") != None:
            sobstv_yavl_strah = "\"+\""
        else:
            sobstv_yavl_strah = ""

        if request.form.get("c_ogr_or_not") != None:
            c_ogr_or_not = "С ограничением"
        else:
            c_ogr_or_not = "Без ограничений"

        if request.form.get("pricep") != None:
            pricep = "Есть прицеп"
        else:
            pricep = ""

        telephone_service = db.query(Config).filter_by(name="telephone_service").first().value
        new_osago = OsagoUGSK(
            user_id=user_id,
            email_login=email_address,
            email_password=email_password,

            surname=request.form["surname"],
            name=request.form["name"],
            otchestvo=request.form["otchestvo"],
            birthday=request.form["birthday"],
            pass_seriya=request.form["pass_seriya"],
            pass_number=request.form["pass_number"],
            pass_vidach=request.form["pass_vidach"],
            pass_address=request.form["pass_address"],

            sobstv_yavl_strah=sobstv_yavl_strah,

            sobstv_surname=request.form["sobstv_surname"],
            sobstv_name=request.form["sobstv_name"],
            sobstv_otchestvo=request.form["sobstv_otchestvo"],
            sobstv_birthday=request.form["sobstv_birthday"],
            sobstv_pass_seriya=request.form["sobstv_pass_seriya"],
            sobstv_pass_number=request.form["sobstv_pass_number"],
            sobstv_pass_vidach=request.form["sobstv_pass_vidach"],
            sobstv_pass_address=request.form["sobstv_pass_address"],

            target=request.form["target"],
            mark=request.form["mark"],
            model=request.form["model"],
            category=request.form["category"],
            other_mark=request.form["other_mark"],
            year=request.form["year"],
            powers=request.form["powers"],
            type_engine=request.form["type_engine"],
            type_cusov=request.form["type_cusov"],
            transmission=request.form["transmission"],
            modification=request.form["modification"],

            max_mass=request.form["max_mass"],
            pricep=pricep,

            count_pass_mest=request.form["count_pass_mest"],

            type_document=request.form["type_document"],

            ctc_ptc_seriya=request.form["ctc_ptc_seriya"],
            ctc_ptc_number=request.form["ctc_ptc_number"],
            ctc_ptc_vidach=request.form["ctc_ptc_vidach"],
            ctc_ptc_reg_znak=request.form["ctc_ptc_reg_znak"],
            ctc_ptc_vin=request.form["ctc_ptc_vin"],
            ctc_ptc_nomer_shassi=request.form["ctc_ptc_nomer_shassi"],
            ctc_ptc_nomer_cusov=request.form["ctc_ptc_nomer_cusov"],

            nomer_dk=request.form["nomer_dk"],
            data_TO=request.form["data_TO"],

            c_ogr_or_not=c_ogr_or_not,

            OSAGO_start=request.form["OSAGO_start"],
            OSAGO_count_mouth=request.form["OSAGO_count_mouth"],

            strah_comp=",".join(strah_comp),

            trans_num=request.form["trans_num"],
            est_price_policy=request.form["est_price_policy"],
            num_group_wa=request.form["num_group_wa"],
            oformitel_id=oformitel_id,

            telephone_service=telephone_service
        )
        db.add(new_osago)

        for voditel in dict_data_voditel.values():
            if voditel.get("foreigndl") != None:
                foreign_dl = True
            else:
                foreign_dl = False
            if voditel.get("tr") != None:
                tr = True
            else:
                tr = False
            new_voditel = VoditelUGSK(
                surname=voditel["surname"],
                name=voditel["name"],
                otchestvo=voditel["otchestvo"],
                birthday=voditel["birthday"],
                seriya_vu=voditel["seriya"],
                nomer_vu=voditel["nomer"],
                data_vidachi_vu=voditel["data"],
                nachalo_staga=voditel["nachalo"],
                osago=new_osago,
                foreign_dl=foreign_dl,
                tr=tr
            )
            db.add(new_voditel)

        db.commit()
        return redirect(url_for("request_insurance.table_request", status_request="active"))
    else:
        db = SessionLocal()
        all_users = db.query(User).filter_by(role_id=2).all()
        return render_template('ugsk/add.html', marks=list_mark, strah_comps=list_strah_comps, all_users=all_users)

@ugsk.route('load_models', methods=['post', 'get'])
def load_models():
    if request.method == 'POST':
        data = """{"markId":"%s","useModification":true,"method":"getVehicleModels"}""" % (request.json["mark"])
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
        }
        r = requests.post("https://e-osago.ugsk.ru/local/tools/webslon/elpolis.api/", data=data.encode("utf-8"), headers=headers)
        r_json = r.json()

        dict_mark_category = {}
        for one_mark in r_json["data"]:
            dict_mark_category[one_mark["text"]] = one_mark["category"]
        # print(dict_mark_category)
        r_json["categoryes"] = dict_mark_category

        return jsonify(r_json)

@ugsk.route('load_modification', methods=['post', 'get'])
def load_modification():
    if request.method == 'POST':
        data = """{"markId":"%s","useModification":true,"method":"GetMarkModelModifications", "modelId": "%s"}""" % (request.json["mark"], request.json["model"])
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
        }
        r = requests.post("https://e-osago.ugsk.ru/local/tools/webslon/elpolis.api/", data=data.encode("utf-8"),
                          headers=headers)
        r_json = r.json()
        print(r_json)

        dict_data = {}
        dict_mod_powers = {}
        list_mod = []
        year = int(request.json["year"])
        for one_mod in r_json["data"]:
            if year <= int(one_mod["LastYearRelease"]) and year >= int(one_mod["FirstYearRelease"]):
                list_mod.append(one_mod["modificationname"])
                dict_mod_powers[one_mod["modificationname"]] = one_mod["Power"]
        dict_data["list_mod"] = list_mod
        dict_data["powers"] = dict_mod_powers

        return jsonify(dict_data)

@ugsk.route('redact_request', methods=['post', 'get'])
@login_required
def redact_request():

    if request.method == 'POST':
        print(request.form)
        db = SessionLocal()

        if request.form.get("oformitel") != None and request.form["oformitel"] != "":
            oformitel_id = db.query(User).filter_by(username=request.form["oformitel"]).first().id
        else:
            oformitel_id = None

        strah_comp = []
        for key_form in request.form.keys():
            if key_form in list_strah_comps:
                strah_comp.append(key_form)
        print(strah_comp)

        dict_data_voditel = {}
        for key_form, value_form in request.form.items():
            if key_form.find("vod") != -1:
                split_key = key_form.split("_")
                if dict_data_voditel.get(split_key[1]) == None:
                    dict_data_voditel[split_key[1]] = {}
                dict_data_voditel[split_key[1]][split_key[2]] = value_form
        print(dict_data_voditel)

        if request.form.get("sobstv_yavl_strah") != None:
            sobstv_yavl_strah = "\"+\""
        else:
            sobstv_yavl_strah = ""

        if request.form.get("c_ogr_or_not") != None:
            c_ogr_or_not = "С ограничением"
        else:
            c_ogr_or_not = "Без ограничений"

        if request.form.get("pricep") != None:
            pricep = "Есть прицеп"
        else:
            pricep = ""

        edit_osago = db.query(OsagoUGSK).filter_by(id=request.form['id'])

        edit_osago.update(
            {
                'email_login': request.form["email_login"],
                'email_password': request.form["email_password"],

                'surname': request.form["surname"],
                'name': request.form["name"],
                'otchestvo': request.form["otchestvo"],
                'birthday': request.form["birthday"],
                'pass_seriya': request.form["pass_seriya"],
                'pass_number': request.form["pass_number"],
                'pass_vidach': request.form["pass_vidach"],
                'pass_address': request.form["pass_address"],

                'sobstv_yavl_strah': sobstv_yavl_strah,

                'sobstv_surname': request.form["sobstv_surname"],
                'sobstv_name': request.form["sobstv_name"],
                'sobstv_otchestvo': request.form["sobstv_otchestvo"],
                'sobstv_birthday': request.form["sobstv_birthday"],
                'sobstv_pass_seriya': request.form["sobstv_pass_seriya"],
                'sobstv_pass_number': request.form["sobstv_pass_number"],
                'sobstv_pass_vidach': request.form["sobstv_pass_vidach"],
                'sobstv_pass_address': request.form["sobstv_pass_address"],

                'target': request.form["target"],
                'mark': request.form["mark"],
                'model': request.form["model"],
                'category':request.form["category"],
                'other_mark': request.form["other_mark"],
                'year': request.form["year"],
                'powers': request.form["powers"],
                'type_engine': request.form["type_engine"],
                'type_cusov': request.form["type_cusov"],
                'transmission': request.form["transmission"],
                'modification': request.form["modification"],

                'max_mass': request.form["max_mass"],
                'pricep': pricep,

                'count_pass_mest': request.form["count_pass_mest"],

                'type_document': request.form["type_document"],

                'ctc_ptc_seriya': request.form["ctc_ptc_seriya"],
                'ctc_ptc_number': request.form["ctc_ptc_number"],
                'ctc_ptc_vidach': request.form["ctc_ptc_vidach"],
                'ctc_ptc_reg_znak': request.form["ctc_ptc_reg_znak"],
                'ctc_ptc_vin': request.form["ctc_ptc_vin"],
                'ctc_ptc_nomer_shassi': request.form["ctc_ptc_nomer_shassi"],
                'ctc_ptc_nomer_cusov': request.form["ctc_ptc_nomer_cusov"],

                'nomer_dk': request.form["nomer_dk"],
                'data_TO': request.form["data_TO"],

                'c_ogr_or_not': c_ogr_or_not,

                'OSAGO_start': request.form["OSAGO_start"],
                'OSAGO_count_mouth': request.form["OSAGO_count_mouth"],

                'strah_comp': ",".join(strah_comp),

                'trans_num': request.form["trans_num"],
                'est_price_policy': request.form["est_price_policy"],
                'real_price_policy': request.form["real_price_policy"],
                'num_group_wa': request.form["num_group_wa"],
                'oformitel_id': oformitel_id
            }
        )
        db.commit()

        index_voditel = 0
        for voditel in dict_data_voditel.values():
            if voditel.get("foreigndl") != None:
                foreign_dl = True
            else:
                foreign_dl = False
            if voditel.get("tr") != None:
                tr = True
            else:
                tr = False
            edit_voditel_id = edit_osago.first().voditeli[index_voditel].id
            edit_voditel = db.query(VoditelUGSK).filter_by(id=edit_voditel_id)
            edit_voditel.update(
                {
                    'surname': voditel["surname"],
                    'name': voditel["name"],
                    'otchestvo': voditel["otchestvo"],
                    'birthday': voditel["birthday"],
                    'seriya_vu': voditel["seriya"],
                    'nomer_vu': voditel["nomer"],
                    'data_vidachi_vu': voditel["data"],
                    'nachalo_staga': voditel["nachalo"],
                    'foreign_dl': foreign_dl,
                    'tr': tr
                }

            )
            db.commit()
            index_voditel += 1

        return redirect(url_for('request_insurance.table_request', status_request="active"))
    else:
        db = SessionLocal()
        all_users = db.query(User).filter_by(role_id=2).all()
        osago_ugsk = db.query(OsagoUGSK).filter_by(id=request.args["id"]).first()

        return render_template('ugsk/edit.html', osago_ugsk=osago_ugsk, marks=list_mark, strah_comps=list_strah_comps, all_users=all_users)

