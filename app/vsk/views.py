from . import vsk
from flask import render_template, redirect, url_for, request, jsonify
from flask_login import current_user

from .mark import mark_dict
from .category import category_dict
from .target import target_dict

import requests
import time
from app.strah_comps import list_strah_comps

from app.databases.models_insurance import Base
from app.databases.database_insurance import SessionLocal
from app.databases.database_insurance import engine as Engine
from app.databases.models_insurance import OsagoVsk, VoditelVsk, StatusOsago, User, Config

from app.databases.models_email import Base as BaseEmail
from app.databases.database_email import SessionLocal as SessionLocalEmail
from app.databases.database_email import engine as EngineEmail
from app.databases.models_email import Email

from functools import wraps

from urllib.parse import quote

from app.databases.db_bot_methods import control_child_osago

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated != True:
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@vsk.route('add', methods=['post', 'get'])
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
        new_osago = OsagoVsk(
            is_main_osago=True,

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
            city_strah=request.form["city_strah"],
            street_strah=request.form["street_strah"],
            building_strah=request.form["building_strah"],
            house_strah=request.form["house_strah"],
            apartment_strah=request.form["apartment_strah"],
            postal_code_strah=request.form["postal_code_strah"],

            sobstv_yavl_strah=sobstv_yavl_strah,

            sobstv_surname=request.form["sobstv_surname"],
            sobstv_name=request.form["sobstv_name"],
            sobstv_otchestvo=request.form["sobstv_otchestvo"],
            sobstv_birthday=request.form["sobstv_birthday"],
            sobstv_pass_seriya=request.form["sobstv_pass_seriya"],
            sobstv_pass_number=request.form["sobstv_pass_number"],
            sobstv_pass_vidach=request.form["sobstv_pass_vidach"],
            city_sobstv=request.form["city_sobstv"],
            street_sobstv=request.form["street_sobstv"],
            building_sobstv=request.form["building_sobstv"],
            house_sobstv=request.form["house_sobstv"],
            apartment_sobstv=request.form["apartment_sobstv"],
            postal_code_sobstv=request.form["postal_code_sobstv"],

            target=request.form["target"],
            category=request.form["category"],
            year=request.form["year"],
            powers=request.form["powers"],
            mark=request.form["mark"],
            model=request.form["model"],
            mark_name_other=request.form["mark_name_other"],
            model_name_other=request.form["model_name_other"],
            mark_id=request.form["mark_id"],
            model_id=request.form["model_id"],

            max_mass=request.form["max_mass"],
            count_pass_mest=request.form["count_pass_mest"],
            pricep=pricep,

            type_document=request.form["type_document"],

            ctc_ptc_seriya=request.form["ctc_ptc_seriya"],
            ctc_ptc_number=request.form["ctc_ptc_number"],
            ctc_ptc_vidach=request.form["ctc_ptc_vidach"],
            ctc_ptc_reg_znak=request.form["ctc_ptc_reg_znak"],
            ctc_ptc_vin=request.form["ctc_ptc_vin"],
            ctc_ptc_nomer_shassi=request.form["ctc_ptc_nomer_shassi"],
            ctc_ptc_nomer_cusov=request.form["ctc_ptc_nomer_cusov"],

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
            new_voditel = VoditelVsk(
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

        control_child_osago(type_osago=new_osago.type_osago, osago_id=new_osago.id)

        return redirect(url_for("request_insurance.table_request", status_request="active"))
    else:
        db = SessionLocal()
        all_users = db.query(User).filter_by(role_id=2).all()
        return render_template('vsk/add.html', marks=mark_dict, strah_comps=list_strah_comps, all_users=all_users)

@vsk.route('load_models', methods=['post', 'get'])
def load_models():
    category_dict = {
        'Мотоциклы и мотороллеры': 1,
        'Легковые автомобили': 2,
        'Грузовые автомобили': 3,
        'Автобусы': 4,
        'Тракторы и иные машины': 7
    }

    if request.method == 'POST':
        dict_model = {}
        category_id = category_dict[request.json["category_name"]]
        mark_id = request.json["mark_id"]
        url = f'https://shop.vsk.ru/osago/ajax/calculation/models/{category_id}/{mark_id}'
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,zh;q=0.5',
            'referer': 'https://shop.vsk.ru/osago/calculation/?',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
            'host': 'shop.vsk.ru',
        }
        r = requests.get(url, headers=headers)
        r_json = r.json()
        for model in r_json["result"]:
            dict_model[model['NAME']] = {
                'mark_id': model['MARK_ID'],
                'model_id': model['ID']
            }
        print(dict_model)


        return jsonify(
            {"data": dict_model}
        )

@vsk.route('redact_request', methods=['post', 'get'])
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

        edit_osago = db.query(OsagoVsk).filter_by(id=request.form['id'])

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
                'city_strah': request.form["city_strah"],
                'street_strah': request.form["street_strah"],
                'building_strah': request.form["building_strah"],
                'house_strah': request.form["house_strah"],
                'apartment_strah': request.form["apartment_strah"],
                'postal_code_strah': request.form["postal_code_strah"],

                'sobstv_yavl_strah': sobstv_yavl_strah,

                'sobstv_surname': request.form["sobstv_surname"],
                'sobstv_name': request.form["sobstv_name"],
                'sobstv_otchestvo': request.form["sobstv_otchestvo"],
                'sobstv_birthday': request.form["sobstv_birthday"],
                'sobstv_pass_seriya': request.form["sobstv_pass_seriya"],
                'sobstv_pass_number': request.form["sobstv_pass_number"],
                'sobstv_pass_vidach': request.form["sobstv_pass_vidach"],
                'city_sobstv': request.form["city_sobstv"],
                'street_sobstv': request.form["street_sobstv"],
                'building_sobstv': request.form["building_sobstv"],
                'house_sobstv': request.form["house_sobstv"],
                'apartment_sobstv': request.form["apartment_sobstv"],
                'postal_code_sobstv': request.form["postal_code_sobstv"],

                'target': request.form["target"],
                'category': request.form["category"],
                'year': request.form["year"],
                'powers': request.form["powers"],
                'mark': request.form["mark"],
                'model': request.form["model"],
                'mark_name_other': request.form["mark_name_other"],
                'model_name_other': request.form["model_name_other"],
                'mark_id': request.form["mark_id"],
                'model_id': request.form["model_id"],

                'max_mass': request.form["max_mass"],
                'count_pass_mest': request.form["count_pass_mest"],
                'pricep': pricep,

                'type_document': request.form["type_document"],

                'ctc_ptc_seriya': request.form["ctc_ptc_seriya"],
                'ctc_ptc_number': request.form["ctc_ptc_number"],
                'ctc_ptc_vidach': request.form["ctc_ptc_vidach"],
                'ctc_ptc_reg_znak': request.form["ctc_ptc_reg_znak"],
                'ctc_ptc_vin': request.form["ctc_ptc_vin"],
                'ctc_ptc_nomer_shassi': request.form["ctc_ptc_nomer_shassi"],
                'ctc_ptc_nomer_cusov': request.form["ctc_ptc_nomer_cusov"],

                'c_ogr_or_not': c_ogr_or_not,

                'OSAGO_start': request.form["OSAGO_start"],
                'OSAGO_count_mouth': request.form["OSAGO_count_mouth"],

                'strah_comp': ",".join(strah_comp),

                'trans_num': request.form["trans_num"],
                'est_price_policy': request.form["est_price_policy"],
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
            edit_voditel = db.query(VoditelVsk).filter_by(id=edit_voditel_id)
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

        control_child_osago(type_osago=edit_osago.first().type_osago, osago_id=edit_osago.first().id)

        return redirect(url_for('request_insurance.table_request', status_request="active"))
    else:
        db = SessionLocal()
        all_users = db.query(User).filter_by(role_id=2).all()
        osago_ugsk = db.query(OsagoVsk).filter_by(id=request.args["id"]).first()

        return render_template('vsk/edit.html', osago_ugsk=osago_ugsk, marks=mark_dict, strah_comps=list_strah_comps, all_users=all_users)

