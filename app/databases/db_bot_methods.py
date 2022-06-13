from app.databases.models_insurance import Base
from app.databases.database_insurance import SessionLocal
from app.databases.database_email import SessionLocal as SessionLocalEmail
from app.databases.database_insurance import engine as Engine
from app.databases.models_insurance import OsagoOsk, Hook, VoditelOsk, StatusOsago, Server, StatusServer, OsagoUGSK, Config, Osago21, Voditel21, VoditelUGSK, User, OsagoArm, VoditelArm, OsagoAlfa, VoditelAlfa, VoditelVsk, OsagoVsk
from app.databases.models_email import Email
from app.databases.json.pydantic_models import PydanticHook, PydanticOsagoOsk, PydanticOsagoUGSK, PydanticOsago21, PydanticOsagoArm, PydanticVoditeliArm, PydanticVoditeliAlfa, PydanticOsagoAlfa, PydanticVoditeliVsk, PydanticOsagoVsk
from sqlalchemy import or_

from datetime import datetime, timedelta
import random
from app import socketio

from config import Config as ConfigSite
import requests
from contextlib import suppress
import json

def start_osago(type_osago, osago_id):
    db = SessionLocal()
    main_osago = db.query(get_exemp_by_type_osago(type_osago=type_osago)).filter_by(id=osago_id).first()
    free_servers = db.query(StatusServer).filter_by(name="Свободен").first().servers

    if len(free_servers) < len(main_osago.list_child_osago):
        raise NoFreeServer

    select_server = random.choice(free_servers)
    set_value(name="status_bot", value=f'{datetime.now().strftime("%d.%m %H:%M")} Зарегистрировано задание для бота', type=main_osago.type_osago, id=main_osago.id)
    getattr(select_server, main_osago.type_osago).append(main_osago)
    select_server.status_server = db.query(StatusServer).filter_by(name="Активен").first()

    for osago in main_osago.list_child_osago:
        select_server = random.choice(free_servers)

        set_value(name="status_bot", value=f'{datetime.now().strftime("%d.%m %H:%M")} Зарегистрировано задание для бота', type=osago.type_osago, id=osago.id)
        getattr(select_server, osago.type_osago).append(osago)

        select_server.status_server = db.query(StatusServer).filter_by(name="Активен").first()

    db.commit()

def stop_osago_for_change_status(type_osago, osago_id):
    db = SessionLocal()
    main_osago = db.query(get_exemp_by_type_osago(type_osago=type_osago)).filter_by(id=osago_id).first()

    server = main_osago.server
    if server != None:
        server.status_server = db.query(StatusServer).filter_by(name='Свободен').first()
        main_osago.server = None

    for osago in main_osago.list_child_osago:
        server = osago.server
        if server != None:
            server.status_server = db.query(StatusServer).filter_by(name='Свободен').first()
            osago.server = None

    db.commit()

def transit_to_success(type_osago, osago_id):
    stop_osago_for_change_status(type_osago, osago_id)
    db = SessionLocal()
    osago = db.query(get_exemp_by_type_osago(type_osago=type_osago)).filter_by(id=osago_id).first()

    osago.status_osago_id = 4
    osago.success_date = datetime.now().strftime("%d.%m.%Y")
    set_value(name="status_bot", value='УСПЕШНО РЕАЛИЗОВАННО', type=type_osago, id=osago_id)
    db.commit()

    del_child_osago(type_osago=type_osago, osago_id=osago_id)

def transit_to_delete(type_osago, osago_id):
    stop_osago_for_change_status(type_osago, osago_id)
    db = SessionLocal()
    osago = db.query(get_exemp_by_type_osago(type_osago=type_osago)).filter_by(id=osago_id).first()
    osago.status_osago_id = 5
    db.commit()

    del_child_osago(type_osago=type_osago, osago_id=osago_id)

def transit_to_active(type_osago, osago_id):
    stop_osago_for_change_status(type_osago, osago_id)
    db = SessionLocal()
    osago = db.query(get_exemp_by_type_osago(type_osago=type_osago)).filter_by(id=osago_id).first()
    osago.status_osago_id = 1
    db.commit()

    control_child_osago(type_osago=type_osago, osago_id=osago_id)

def stop_osago(type_osago, osago_id):
    db = SessionLocal()

    main_osago = db.query(get_exemp_by_type_osago(type_osago=type_osago)).filter_by(id=osago_id).first()
    set_value(name="status_bot", value=f'{datetime.now().strftime("%d.%m %H:%M")} Бот остановлен', type=main_osago.type_osago, id=main_osago.id)
    server = main_osago.server
    server.status_server = db.query(StatusServer).filter_by(name='Свободен').first()
    main_osago.server = None

    # for osago in main_osago.list_child_osago:
    #     set_value(name="status_bot", value=f'{datetime.now().strftime("%d.%m %H:%M")} Бот остановлен', type=osago.type_osago, id=osago.id)
    #     server = osago.server
    #     server.status_server = db.query(StatusServer).filter_by(name='Свободен').first()
    #     osago.server = None

    db.commit()


def power_osago(type_osago, osago_id):
    db = SessionLocal()
    osago = db.query(get_exemp_by_type_osago(type_osago=type_osago)).filter_by(id=osago_id).first()
    if osago.server == None:
        start_osago(type_osago=type_osago, osago_id=osago_id)
    else:
        stop_osago(type_osago=type_osago, osago_id=osago_id)

def start_hook(hook_id):
    db = SessionLocal()
    hook = db.query(Hook).filter_by(id=hook_id).first()

    free_servers = db.query(StatusServer).filter_by(name="Свободен").first().servers
    if free_servers != []:
        select_server = random.choice(free_servers)
        select_server.hook.append(hook)
    else:
        raise NoFreeServer

    select_server.status_server = db.query(StatusServer).filter_by(name="Активен").first()

    set_value(name="status_bot", value=f'{datetime.now().strftime("%d.%m %H:%M")} Зарегистрировано задание для бота', type="hook", id=hook_id)

    db.commit()

def stop_hook(hook_id):
    db = SessionLocal()
    hook = db.query(Hook).filter_by(id=hook_id).first()
    server = hook.server

    server.status_server = db.query(StatusServer).filter_by(name='Свободен').first()
    set_value(name="status_bot", value=f'{datetime.now().strftime("%d.%m %H:%M")} Бот остановлен', type="hook", id=hook_id)
    hook.server = None

    db.commit()

def power_hook(hook_id):
    db = SessionLocal()
    hook = db.query(Hook).filter_by(id=hook_id).first()

    if hook.server == None:
        start_hook(hook_id=hook_id)
    else:
        stop_hook(hook_id=hook_id)


def check_status_server(server_address):
    db = SessionLocal()
    if db.query(Server).filter_by(server_address=server_address).first() == 'Активен':
        return True
    else:
        return False

def check_task_server(server_address):
    db = SessionLocal()
    server = db.query(Server).filter_by(server_address=server_address).first()

    if server.status_server.name == 'Активен' and server.hook != []:
        return {"status": True, "type": "hook", "data": PydanticHook.from_orm(server.hook[0]).dict()}
    elif server.status_server.name == "Активен" and server.osago != []:
        return {"status": True, "type": server.osago[0].type_osago, "data": get_exemp_by_type_osago_pydantic(type_osago=server.osago[0].type_osago).from_orm(server.osago[0]).dict()}
    elif server.status_server.name == "Свободен":
        return {"status": False, "type": None, "data": None}

def create_task(type_task, id_task):
    if type_task == 'osago_osk':
        start_osago(type_osago="osago_osk", osago_id=id_task)
    elif type_task == "Hook":
        start_hook(hook_id=id_task)

def add_server_bot(server_address):
    db = SessionLocal()
    server = Server(
        server_address=server_address
    )
    db.add(server)
    db.commit()

def set_value(name, value, type, id):
    db = SessionLocal()
    osago = db.query(get_exemp_by_type_osago(type_osago=type)).filter_by(id=id)
    if name == "status_bot":
        if value.find("Завершено") != -1:
            name_room = osago.first().user.username
            socketio.emit('success_osago', {'data': 42}, to=name_room)
            if osago.first().oformitel_id != None:
                name_room_oformitel = db.query(User).filter_by(id=osago.first().oformitel_id).first().username
                socketio.emit('success_osago', {'data': 42}, to=name_room_oformitel)
            osago.first().status_osago_id = 2
            osago.first().reg_date = datetime.now().strftime("%d.%m.%Y %H:%M")
        elif value.lower().find("ошибка") != -1:
            osago.first().status_osago_id = 6
        status_bot_split = osago.first().status_bot.split(',')
        if len(status_bot_split) < 10:
            osago.first().status_bot += f',{value}'
        else:
            status_bot_split.pop(0)
            status_bot_split.append(value)
            osago.first().status_bot = ",".join(status_bot_split)
    else:
        osago.update({
            name: value
        })
    db.commit()
    return {"update_data": get_exemp_by_type_osago_pydantic(type_osago=type).from_orm(osago.first()).dict(), "type": type}

def get_telephone_service():
    db = SessionLocal()
    return db.query(Config).filter_by(name="telephone_service").first().value

def duplicate_osago(osago_id, count, type_osago):
    db = SessionLocal()
    osago = db.query(get_exemp_by_type_osago(type_osago=type_osago)).filter_by(id=osago_id).first()
    voditeli = osago.voditeli

    if type_osago == "osago_ugsk":
        print("Пененосим 21 в Югорию")
        copy_osago = OsagoUGSK(
            user_id=osago.user_id,
            email_login=osago.email_login,
            email_password=osago.email_password,

            surname=osago.surname,
            name=osago.name,
            otchestvo=osago.otchestvo,
            birthday=osago.birthday,
            pass_seriya=osago.pass_seriya,
            pass_number=osago.pass_number,
            pass_vidach=osago.pass_vidach,
            pass_address=osago.pass_address,

            sobstv_yavl_strah=osago.sobstv_yavl_strah,

            sobstv_surname=osago.sobstv_surname,
            sobstv_name=osago.sobstv_name,
            sobstv_otchestvo=osago.sobstv_otchestvo,
            sobstv_birthday=osago.sobstv_birthday,
            sobstv_pass_seriya=osago.sobstv_pass_seriya,
            sobstv_pass_number=osago.sobstv_pass_number,
            sobstv_pass_vidach=osago.sobstv_pass_vidach,
            sobstv_pass_address=osago.sobstv_pass_address,

            target=osago.target,
            mark=osago.mark,
            model=osago.model,
            category=osago.category,
            other_mark=osago.other_mark,
            year=osago.year,
            powers=osago.powers,
            type_engine=osago.type_engine,
            type_cusov=osago.type_cusov,
            transmission=osago.transmission,
            modification=osago.modification,

            max_mass=osago.max_mass,
            pricep=osago.pricep,

            count_pass_mest=osago.count_pass_mest,

            type_document=osago.type_document,

            ctc_ptc_seriya=osago.ctc_ptc_seriya,
            ctc_ptc_number=osago.ctc_ptc_number,
            ctc_ptc_vidach=osago.ctc_ptc_vidach,
            ctc_ptc_reg_znak=osago.ctc_ptc_reg_znak,
            ctc_ptc_vin=osago.ctc_ptc_vin,
            ctc_ptc_nomer_shassi=osago.ctc_ptc_nomer_shassi,
            ctc_ptc_nomer_cusov=osago.ctc_ptc_nomer_cusov,

            nomer_dk=osago.nomer_dk,
            data_TO=osago.data_TO,

            c_ogr_or_not=osago.c_ogr_or_not,

            OSAGO_start=osago.OSAGO_start,
            OSAGO_count_mouth=osago.OSAGO_count_mouth,

            strah_comp=osago.strah_comp,

            trans_num=osago.trans_num,
            est_price_policy=osago.est_price_policy,
            num_group_wa=osago.num_group_wa,

            status_bot=osago.status_bot,
            priority_application=osago.priority_application,
            reg_date=osago.reg_date,
            oformitel_id=osago.oformitel_id,
            success_date=osago.success_date

        )
        db.add(copy_osago)

        for one_vod in voditeli:
            copy_vod = VoditelUGSK(
                surname=one_vod.surname,
                name=one_vod.name,
                otchestvo=one_vod.otchestvo,
                birthday=one_vod.birthday,
                seriya_vu=one_vod.seriya_vu,
                nomer_vu=one_vod.nomer_vu,
                data_vidachi_vu=one_vod.data_vidachi_vu,
                nachalo_staga=one_vod.nachalo_staga,
                osago=copy_osago,
                foreign_dl=one_vod.foreign_dl
            )
            db.add(copy_vod)
        db.commit()
    elif type_osago == "osago_21":
        copy_osago = Osago21(
            user_id=osago.user_id,
            email_login=osago.email_login,
            email_password=osago.email_password,

            surname=osago.surname,
            name=osago.name,
            otchestvo=osago.otchestvo,
            birthday=osago.birthday,
            pass_seriya=osago.pass_seriya,
            pass_number=osago.pass_number,
            pass_vidach=osago.pass_vidach,
            pass_address=osago.pass_address,
            strah_type_document=osago.strah_type_document,

            sobstv_yavl_strah=osago.sobstv_yavl_strah,

            sobstv_surname=osago.sobstv_surname,
            sobstv_name=osago.sobstv_name,
            sobstv_otchestvo=osago.sobstv_otchestvo,
            sobstv_birthday=osago.sobstv_birthday,
            sobstv_pass_seriya=osago.sobstv_pass_seriya,
            sobstv_pass_number=osago.sobstv_pass_number,
            sobstv_pass_vidach=osago.sobstv_pass_vidach,
            sobstv_pass_address=osago.sobstv_pass_address,
            sobstv_type_document=osago.sobstv_type_document,

            target=osago.target,
            mark=osago.mark,
            model=osago.model,
            category=osago.category,
            other_mark=osago.other_mark,
            year=osago.year,
            powers=osago.powers,
            type_engine=osago.type_engine,
            type_cusov=osago.type_cusov,
            transmission=osago.transmission,
            modification=osago.modification,

            max_mass=osago.max_mass,
            pricep=osago.pricep,

            count_pass_mest=osago.count_pass_mest,

            type_document=osago.type_document,

            ctc_ptc_seriya=osago.ctc_ptc_seriya,
            ctc_ptc_number=osago.ctc_ptc_number,
            ctc_ptc_vidach=osago.ctc_ptc_vidach,
            ctc_ptc_reg_znak=osago.ctc_ptc_reg_znak,
            ctc_ptc_vin=osago.ctc_ptc_vin,
            ctc_ptc_nomer_shassi=osago.ctc_ptc_nomer_shassi,
            ctc_ptc_nomer_cusov=osago.ctc_ptc_nomer_cusov,

            nomer_dk=osago.nomer_dk,
            data_TO=osago.data_TO,

            c_ogr_or_not=osago.c_ogr_or_not,

            OSAGO_start=osago.OSAGO_start,
            OSAGO_count_mouth=osago.OSAGO_count_mouth,

            strah_comp=osago.strah_comp,

            trans_num=osago.trans_num,
            est_price_policy=osago.est_price_policy,
            num_group_wa=osago.num_group_wa,

            status_bot=osago.status_bot,
            priority_application=osago.priority_application,
            reg_date=osago.reg_date,
            oformitel_id=osago.oformitel_id,
            success_date=osago.success_date
        )
        db.add(copy_osago)

        for one_vod in voditeli:
            copy_vod = Voditel21(
                surname=one_vod.surname,
                name=one_vod.name,
                otchestvo=one_vod.otchestvo,
                birthday=one_vod.birthday,
                seriya_vu=one_vod.seriya_vu,
                nomer_vu=one_vod.nomer_vu,
                data_vidachi_vu=one_vod.data_vidachi_vu,
                nachalo_staga=one_vod.nachalo_staga,
                osago=copy_osago,
                foreign_dl=one_vod.foreign_dl
            )
            db.add(copy_vod)
        db.commit()
    elif type_osago == "osago_arm":
        copy_osago = OsagoArm(
            user_id=osago.user_id,
            email_login=osago.email_login,
            email_password=osago.email_password,

            surname=osago.surname,
            name=osago.name,
            otchestvo=osago.otchestvo,
            birthday=osago.birthday,
            pass_seriya=osago.pass_seriya,
            pass_number=osago.pass_number,
            pass_vidach=osago.pass_vidach,
            pass_address=osago.pass_address,

            sobstv_yavl_strah=osago.sobstv_yavl_strah,

            sobstv_surname=osago.sobstv_surname,
            sobstv_name=osago.sobstv_name,
            sobstv_otchestvo=osago.sobstv_otchestvo,
            sobstv_birthday=osago.sobstv_birthday,
            sobstv_pass_seriya=osago.sobstv_pass_seriya,
            sobstv_pass_number=osago.sobstv_pass_number,
            sobstv_pass_vidach=osago.sobstv_pass_vidach,
            sobstv_pass_address=osago.sobstv_pass_address,

            target=osago.target,
            mark=osago.mark,
            model=osago.model,
            category=osago.category,
            other_mark=osago.other_mark,
            year=osago.year,
            powers=osago.powers,
            type_engine=osago.type_engine,
            type_cusov=osago.type_cusov,
            transmission=osago.transmission,
            modification=osago.modification,

            max_mass=osago.max_mass,
            pricep=osago.pricep,

            count_pass_mest=osago.count_pass_mest,

            type_document=osago.type_document,

            ctc_ptc_seriya=osago.ctc_ptc_seriya,
            ctc_ptc_number=osago.ctc_ptc_number,
            ctc_ptc_vidach=osago.ctc_ptc_vidach,
            ctc_ptc_reg_znak=osago.ctc_ptc_reg_znak,
            ctc_ptc_vin=osago.ctc_ptc_vin,
            ctc_ptc_nomer_shassi=osago.ctc_ptc_nomer_shassi,
            ctc_ptc_nomer_cusov=osago.ctc_ptc_nomer_cusov,

            nomer_dk=osago.nomer_dk,
            data_TO=osago.data_TO,

            c_ogr_or_not=osago.c_ogr_or_not,

            OSAGO_start=osago.OSAGO_start,
            OSAGO_count_mouth=osago.OSAGO_count_mouth,

            strah_comp=osago.strah_comp,

            trans_num=osago.trans_num,
            est_price_policy=osago.est_price_policy,
            num_group_wa=osago.num_group_wa,

            status_bot=osago.status_bot,
            priority_application=osago.priority_application,
            reg_date=osago.reg_date,
            oformitel_id=osago.oformitel_id,
            success_date=osago.success_date
        )
        db.add(copy_osago)

        for one_vod in voditeli:
            copy_vod = VoditelArm(
                surname=one_vod.surname,
                name=one_vod.name,
                otchestvo=one_vod.otchestvo,
                birthday=one_vod.birthday,
                seriya_vu=one_vod.seriya_vu,
                nomer_vu=one_vod.nomer_vu,
                data_vidachi_vu=one_vod.data_vidachi_vu,
                nachalo_staga=one_vod.nachalo_staga,
                osago=copy_osago,
                foreign_dl=one_vod.foreign_dl
            )
            db.add(copy_vod)
        db.commit()
    elif type_osago == "osago_alfa":
        copy_osago = OsagoAlfa(
            is_main_osago=osago.is_main_osago,

            user_id=osago.user_id,
            email_login=osago.email_login,
            email_password=osago.email_password,

            surname=osago.surname,
            name=osago.name,
            otchestvo=osago.otchestvo,
            birthday=osago.birthday,
            pass_seriya=osago.pass_seriya,
            pass_number=osago.pass_number,
            pass_vidach=osago.pass_vidach,
            pass_address=osago.pass_address,

            sobstv_yavl_strah=osago.sobstv_yavl_strah,

            sobstv_surname=osago.sobstv_surname,
            sobstv_name=osago.sobstv_name,
            sobstv_otchestvo=osago.sobstv_otchestvo,
            sobstv_birthday=osago.sobstv_birthday,
            sobstv_pass_seriya=osago.sobstv_pass_seriya,
            sobstv_pass_number=osago.sobstv_pass_number,
            sobstv_pass_vidach=osago.sobstv_pass_vidach,
            sobstv_pass_address=osago.sobstv_pass_address,

            target=osago.target,
            category=osago.category,
            year=osago.year,
            powers=osago.powers,
            auto_region=osago.auto_region,
            auto_type=osago.auto_type,
            brand_name=osago.brand_name,
            brand=osago.brand,
            brand_name_other=osago.brand_name_other,
            model=osago.model,
            model_name_other=osago.model_name_other,
            model_name=osago.model_name,
            modification=osago.modification,
            modification_name=osago.modification_name,

            max_mass=osago.max_mass,
            pricep=osago.pricep,

            count_pass_mest=osago.count_pass_mest,

            type_document=osago.type_document,

            ctc_ptc_seriya=osago.ctc_ptc_seriya,
            ctc_ptc_number=osago.ctc_ptc_number,
            ctc_ptc_vidach=osago.ctc_ptc_vidach,
            ctc_ptc_reg_znak=osago.ctc_ptc_reg_znak,
            ctc_ptc_vin=osago.ctc_ptc_vin,
            ctc_ptc_nomer_shassi=osago.ctc_ptc_nomer_shassi,
            ctc_ptc_nomer_cusov=osago.ctc_ptc_nomer_cusov,

            nomer_dk=osago.nomer_dk,
            data_TO=osago.data_TO,

            c_ogr_or_not=osago.c_ogr_or_not,

            OSAGO_start=osago.OSAGO_start,
            OSAGO_count_mouth=osago.OSAGO_count_mouth,

            strah_comp=osago.strah_comp,

            trans_num=osago.trans_num,
            est_price_policy=osago.est_price_policy,
            num_group_wa=osago.num_group_wa,

            status_bot=osago.status_bot,
            priority_application=osago.priority_application,
            reg_date=osago.reg_date,
            oformitel_id=osago.oformitel_id,
            success_date=osago.success_date
        )
        db.add(copy_osago)

        for one_vod in voditeli:
            copy_vod = VoditelAlfa(
                surname=one_vod.surname,
                name=one_vod.name,
                otchestvo=one_vod.otchestvo,
                birthday=one_vod.birthday,
                seriya_vu=one_vod.seriya_vu,
                nomer_vu=one_vod.nomer_vu,
                data_vidachi_vu=one_vod.data_vidachi_vu,
                nachalo_staga=one_vod.nachalo_staga,
                osago=copy_osago,
                foreign_dl=one_vod.foreign_dl
            )
            db.add(copy_vod)
        db.commit()
    elif type_osago == "osago_vsk":
        copy_osago = OsagoVsk(
            is_main_osago=osago.is_main_osago,

            user_id=osago.user_id,
            email_login=osago.email_login,
            email_password=osago.email_password,

            surname=osago.surname,
            name=osago.name,
            otchestvo=osago.otchestvo,
            birthday=osago.birthday,
            pass_seriya=osago.pass_seriya,
            pass_number=osago.pass_number,
            pass_vidach=osago.pass_vidach,
            city_strah=osago.city_strah,
            street_strah=osago.street_strah,
            building_strah=osago.building_strah,
            house_strah=osago.house_strah,
            apartment_strah=osago.apartment_strah,
            postal_code_strah=osago.postal_code_strah,
            strah_type_document=osago.strah_type_document,

            sobstv_yavl_strah=osago.sobstv_yavl_strah,

            sobstv_surname=osago.sobstv_surname,
            sobstv_name=osago.sobstv_name,
            sobstv_otchestvo=osago.sobstv_otchestvo,
            sobstv_birthday=osago.sobstv_birthday,
            sobstv_pass_seriya=osago.sobstv_pass_seriya,
            sobstv_pass_number=osago.sobstv_pass_number,
            sobstv_pass_vidach=osago.sobstv_pass_vidach,
            city_sobstv=osago.city_sobstv,
            street_sobstv=osago.street_sobstv,
            building_sobstv=osago.building_sobstv,
            house_sobstv=osago.house_sobstv,
            apartment_sobstv=osago.apartment_sobstv,
            postal_code_sobstv=osago.postal_code_sobstv,
            sobstv_type_document=osago.sobstv_type_document,

            target=osago.target,
            category=osago.category,
            year=osago.year,
            powers=osago.powers,
            mark=osago.mark,
            model=osago.model,
            mark_name_other=osago.mark_name_other,
            model_name_other=osago.model_name_other,
            mark_id=osago.mark_id,
            model_id=osago.model_id,

            max_mass=osago.max_mass,
            pricep=osago.pricep,

            count_pass_mest=osago.count_pass_mest,

            type_document=osago.type_document,

            ctc_ptc_seriya=osago.ctc_ptc_seriya,
            ctc_ptc_number=osago.ctc_ptc_number,
            ctc_ptc_vidach=osago.ctc_ptc_vidach,
            ctc_ptc_reg_znak=osago.ctc_ptc_reg_znak,
            ctc_ptc_vin=osago.ctc_ptc_vin,
            ctc_ptc_nomer_shassi=osago.ctc_ptc_nomer_shassi,
            ctc_ptc_nomer_cusov=osago.ctc_ptc_nomer_cusov,

            nomer_dk=osago.nomer_dk,
            data_TO=osago.data_TO,

            c_ogr_or_not=osago.c_ogr_or_not,

            OSAGO_start=osago.OSAGO_start,
            OSAGO_count_mouth=osago.OSAGO_count_mouth,

            strah_comp=osago.strah_comp,

            trans_num=osago.trans_num,
            est_price_policy=osago.est_price_policy,
            num_group_wa=osago.num_group_wa,

            status_bot=osago.status_bot,
            priority_application=osago.priority_application,
            reg_date=osago.reg_date,
            oformitel_id=osago.oformitel_id,
            success_date=osago.success_date
        )
        db.add(copy_osago)

        for one_vod in voditeli:
            copy_vod = VoditelVsk(
                surname=one_vod.surname,
                name=one_vod.name,
                otchestvo=one_vod.otchestvo,
                birthday=one_vod.birthday,
                seriya_vu=one_vod.seriya_vu,
                nomer_vu=one_vod.nomer_vu,
                data_vidachi_vu=one_vod.data_vidachi_vu,
                nachalo_staga=one_vod.nachalo_staga,
                osago=copy_osago,
                foreign_dl=one_vod.foreign_dl
            )
            db.add(copy_vod)
        db.commit()

    return copy_osago.id

def change_email_address(type, id):
    db = SessionLocal()
    db_email = SessionLocalEmail()

    osago = db.query(get_exemp_by_type_osago(type_osago=type)).filter_by(id=id)

    email = db_email.query(Email).filter_by(user_id=osago.first().user_id).first()
    email_address = email.email_address
    email_password = email.email_password
    db_email.delete(email)
    db_email.commit()
    db_email.close()

    osago.first().email_login = email_address
    osago.first().email_password = email_password
    db.commit()

    update_data = get_exemp_by_type_osago_pydantic(type_osago=type).from_orm(osago.first()).dict()

    return {"update_data": update_data, "type": type}

def add_favorites(type_osago, osago_id):
    db = SessionLocal()

    osago = db.query(get_exemp_by_type_osago(type_osago=type_osago)).filter_by(id=osago_id).first()
    osago.priority_application = True
    db.commit()

def del_favorites(type_osago, osago_id):
    db = SessionLocal()
    if type_osago == "osago_osk":
        osago = db.query(OsagoOsk).filter_by(id=osago_id).first()
    elif type_osago == "osago_ugsk":
        osago = db.query(OsagoUGSK).filter_by(id=osago_id).first()
    elif type_osago == "osago_21":
        osago = db.query(Osago21).filter_by(id=osago_id).first()
    elif type_osago == "osago_arm":
        osago = db.query(OsagoArm).filter_by(id=osago_id).first()
    elif type_osago == "osago_alfa":
        osago = db.query(OsagoAlfa).filter_by(id=osago_id).first()
    elif type_osago == "osago_vsk":
        osago = db.query(OsagoVsk).filter_by(id=osago_id).first()
    osago.priority_application = False
    db.commit()

def transit_osago(type_osago, osago_id, type_osago_to):
    print(type_osago, type_osago_to)
    db = SessionLocal()
    osago = db.query(get_exemp_by_type_osago(type_osago=type_osago)).filter_by(id=osago_id).first()
    voditeli = osago.voditeli

    if type_osago_to == "osago_alfa":
        copy_osago = OsagoAlfa(
            user_id=osago.user_id,
            email_login=osago.email_login,
            email_password=osago.email_password,

            surname=osago.surname,
            name=osago.name,
            otchestvo=osago.otchestvo,
            birthday=osago.birthday,
            pass_seriya=osago.pass_seriya,
            pass_number=osago.pass_number,
            pass_vidach=osago.pass_vidach,

            sobstv_yavl_strah=osago.sobstv_yavl_strah,

            sobstv_surname=osago.sobstv_surname,
            sobstv_name=osago.sobstv_name,
            sobstv_otchestvo=osago.sobstv_otchestvo,
            sobstv_birthday=osago.sobstv_birthday,
            sobstv_pass_seriya=osago.sobstv_pass_seriya,
            sobstv_pass_number=osago.sobstv_pass_number,
            sobstv_pass_vidach=osago.sobstv_pass_vidach,

            max_mass=osago.max_mass,
            pricep=osago.pricep,

            count_pass_mest=osago.count_pass_mest,

            ctc_ptc_seriya=osago.ctc_ptc_seriya,
            ctc_ptc_number=osago.ctc_ptc_number,
            ctc_ptc_vidach=osago.ctc_ptc_vidach,
            ctc_ptc_vin=osago.ctc_ptc_vin,
            ctc_ptc_nomer_shassi=osago.ctc_ptc_nomer_shassi,
            ctc_ptc_nomer_cusov=osago.ctc_ptc_nomer_cusov,

            nomer_dk=osago.nomer_dk,
            data_TO=osago.data_TO,

            c_ogr_or_not=osago.c_ogr_or_not,

            OSAGO_start=osago.OSAGO_start,
            OSAGO_count_mouth=osago.OSAGO_count_mouth,

            strah_comp=osago.strah_comp,

            trans_num=osago.trans_num,
            est_price_policy=osago.est_price_policy,
            num_group_wa=osago.num_group_wa,

            priority_application=osago.priority_application,
            reg_date=osago.reg_date,
            oformitel_id=osago.oformitel_id,
            success_date=osago.success_date

        )
    elif type_osago_to == "osago_vsk":
        copy_osago = OsagoVsk(
            user_id=osago.user_id,
            email_login=osago.email_login,
            email_password=osago.email_password,

            surname=osago.surname,
            name=osago.name,
            otchestvo=osago.otchestvo,
            birthday=osago.birthday,
            pass_seriya=osago.pass_seriya,
            pass_number=osago.pass_number,
            pass_vidach=osago.pass_vidach,

            sobstv_yavl_strah=osago.sobstv_yavl_strah,

            sobstv_surname=osago.sobstv_surname,
            sobstv_name=osago.sobstv_name,
            sobstv_otchestvo=osago.sobstv_otchestvo,
            sobstv_birthday=osago.sobstv_birthday,
            sobstv_pass_seriya=osago.sobstv_pass_seriya,
            sobstv_pass_number=osago.sobstv_pass_number,
            sobstv_pass_vidach=osago.sobstv_pass_vidach,

            max_mass=osago.max_mass,
            pricep=osago.pricep,

            count_pass_mest=osago.count_pass_mest,

            ctc_ptc_seriya=osago.ctc_ptc_seriya,
            ctc_ptc_number=osago.ctc_ptc_number,
            ctc_ptc_vidach=osago.ctc_ptc_vidach,
            ctc_ptc_vin=osago.ctc_ptc_vin,
            ctc_ptc_nomer_shassi=osago.ctc_ptc_nomer_shassi,
            ctc_ptc_nomer_cusov=osago.ctc_ptc_nomer_cusov,

            nomer_dk=osago.nomer_dk,
            data_TO=osago.data_TO,

            c_ogr_or_not=osago.c_ogr_or_not,

            OSAGO_start=osago.OSAGO_start,
            OSAGO_count_mouth=osago.OSAGO_count_mouth,

            strah_comp=osago.strah_comp,

            trans_num=osago.trans_num,
            est_price_policy=osago.est_price_policy,
            num_group_wa=osago.num_group_wa,

            priority_application=osago.priority_application,
            reg_date=osago.reg_date,
            oformitel_id=osago.oformitel_id,
            success_date=osago.success_date

        )

    db.add(copy_osago)
    if osago.server != None:
        osago.server.status_server = db.query(StatusServer).filter_by(name='Свободен').first()
    db.delete(osago)
    for one_vod in voditeli:
        copy_vod = get_exemp_by_type_vod(type_osago=type_osago_to)(
            surname=one_vod.surname,
            name=one_vod.name,
            otchestvo=one_vod.otchestvo,
            birthday=one_vod.birthday,
            seriya_vu=one_vod.seriya_vu,
            nomer_vu=one_vod.nomer_vu,
            data_vidachi_vu=one_vod.data_vidachi_vu,
            nachalo_staga=one_vod.nachalo_staga,
            osago=copy_osago,
            foreign_dl=one_vod.foreign_dl
        )
        db.add(copy_vod)
        db.delete(one_vod)
    db.commit()

    return copy_osago.id

def check_reg_date():
    db = SessionLocal()
    osago_osk = db.query(OsagoOsk).filter_by(status_osago_id=2).all()
    osago_ugsk = db.query(OsagoUGSK).filter_by(status_osago_id=2).all()
    osago_21 = db.query(Osago21).filter_by(status_osago_id=2).all()
    osago_arm = db.query(OsagoArm).filter_by(status_osago_id=2).all()
    osago_alfa = db.query(OsagoAlfa).filter_by(status_osago_id=2).all()
    osago_vsk = db.query(OsagoVsk).filter_by(status_osago_id=2).all()
    osago_all = osago_osk + osago_ugsk + osago_21 + osago_arm + osago_alfa +osago_vsk
    for osago in osago_all:
        print(datetime.now() - datetime.strptime(osago.reg_date, "%d.%m.%Y %H:%M"))
        if osago.reg_date != "" and ((datetime.now() - datetime.strptime(osago.reg_date, "%d.%m.%Y %H:%M")) > timedelta(minutes=15)):
            osago.status_osago_id = 6
    db.commit()

def set_in_job(type_osago, osago_id):
    db = SessionLocal()
    if type_osago == "osago_osk":
        osago = db.query(OsagoOsk).filter_by(id=osago_id).first()
    elif type_osago == "osago_ugsk":
        osago = db.query(OsagoUGSK).filter_by(id=osago_id).first()
    elif type_osago == "osago_21":
        osago = db.query(Osago21).filter_by(id=osago_id).first()
    elif type_osago == "osago_arm":
        osago = db.query(OsagoArm).filter_by(id=osago_id).first()
    elif type_osago == "osago_alfa":
        osago = db.query(OsagoAlfa).filter_by(id=osago_id).first()
    elif type_osago == "osago_vsk":
        osago = db.query(OsagoVsk).filter_by(id=osago_id).first()
    osago.status_osago_id = 3
    db.commit()

def set_selected_oformitel(user_id, oformitel_name):
    db = SessionLocal()
    db.query(User).filter_by(id=user_id).first().selected_oformitel_name = oformitel_name
    db.commit()

def set_selected_otv(user_id, otv_name):
    db = SessionLocal()
    db.query(User).filter_by(id=user_id).first().selected_otv_name = otv_name
    db.commit()


def dadata_address(text_address):
    params = {
        "count": 7,
        "query": text_address,
        "token": ConfigSite.token_dadata,
        "type": "ADDRESS"
    }
    headers = {
        'accept': 'application/json, text/plain, */*', 'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7', 'origin': 'https://eosago21-vek.ru/',
        'referer': 'https://eosago21-vek.ru/',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors', 'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    session = requests.Session()
    r = session.get("https://dadata.ru/api/v2/suggest/address/", params=params, headers=headers)
    r_json = r.json()

    list_address = []
    for one_address in r_json["suggestions"]:
        list_address.append(one_address['value'])
    print(list_address)
    return {'data': list_address}


def vsk_city(text_city):
    params = {
        "q": text_city.split(',')[0]
    }
    headers = {
        'accept': 'application/json, text/plain, */*', 'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7', 'origin': 'https://eosago21-vek.ru/',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors', 'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    session = requests.Session()
    r = session.get("https://shop.vsk.ru/osago/ajax/kladr/search/", params=params, headers=headers)
    r_json = r.json()

    dict_address = {}
    for one_address in r_json:
        dict_address[one_address['value']] = {'fias': one_address['fias']}
    print(dict_address)
    return {'data': dict_address}

def vsk_street(text_street, fias_city):
    params = {
        "q": text_street.split(',')[0],
        "city": fias_city
    }
    headers = {
        'accept': 'application/json, text/plain, */*', 'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7', 'origin': 'https://eosago21-vek.ru/',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors', 'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    session = requests.Session()
    r = session.get("https://shop.vsk.ru/osago/ajax/kladr/search/", params=params, headers=headers)
    r_json = r.json()

    list_address = []
    for one_address in r_json:
        list_address.append(one_address['value'])
    print(list_address)
    return {'data': list_address}


# def alfa_region(text_region):
#     data = {
#         "from_bound": {
#           "value": "region"
#         },
#         "to_bound": {
#           "value": "area"
#         },
#         "query": text_region,
#         "count": 5
#     }
#     headers = {
#         'Accept': 'application/json, text/javascript, */*; q=0.01',
#         'Accept-Encoding': 'gzip, deflate, br',
#         'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,zh;q=0.5',
#         'Connection': 'keep-alive',
#         'Content-Type': 'application/json',
#         'Host': 'dadata.alfastrah.ru:8443',
#         'Origin': 'https://www.alfastrah.ru',
#         'Referer': 'https://www.alfastrah.ru/',
#         'Sec-Fetch-Dest': 'empty',
#         'Sec-Fetch-Mode': 'cors',
#         'Sec-Fetch-Site': 'same-site',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
#         'X-Version': '16.6.3',
#         'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
#         'sec-ch-ua-mobile': '?0',
#         'sec-ch-ua-platform': '"Windows"',
#     }
#     r = requests.post('https://dadata.alfastrah.ru:8443/suggestions/api/4_1/rs/suggest/address', headers=headers,
#                       data=json.dumps(data).encode('utf-8'))
#     print(r.json())
#     dict_region = []
#     for one_region in r.json()['suggestions']:
#         dict_region[one_region['value']] = one_region['data']['kladr_id']
#     return {'data': dict_region}
#
# def alfa_city(text_city, kladr_id):
#     data = {
#         "locations":[
#           {
#              "kladr_id": kladr_id
#           }
#         ],
#         "restrict_value": True,
#         "from_bound": {
#           "value": "city"
#         },
#         "to_bound": {
#           "value": "settlement"
#         },
#         "query": text_city,
#         "count": 5
#     }
#     headers = {
#         'Accept': 'application/json, text/javascript, */*; q=0.01',
#         'Accept-Encoding': 'gzip, deflate, br',
#         'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,zh;q=0.5',
#         'Connection': 'keep-alive',
#         'Content-Type': 'application/json',
#         'Host': 'dadata.alfastrah.ru:8443',
#         'Origin': 'https://www.alfastrah.ru',
#         'Referer': 'https://www.alfastrah.ru/',
#         'Sec-Fetch-Dest': 'empty',
#         'Sec-Fetch-Mode': 'cors',
#         'Sec-Fetch-Site': 'same-site',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
#         'X-Version': '16.6.3',
#         'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
#         'sec-ch-ua-mobile': '?0',
#         'sec-ch-ua-platform': '"Windows"',
#     }
#     r = requests.post('https://dadata.alfastrah.ru:8443/suggestions/api/4_1/rs/suggest/address', headers=headers,
#                       data=json.dumps(data).encode('utf-8'))
#     print(r.json())
#     list_city = []
#     for one_region in r.json()['suggestions']:
#         list_city.append(one_region['value'])
#     return {'data': list_city}
#
# def alfa_street(text_street, kladr_id):
#     data = {
#        "locations": [
#           {
#              "kladr_id": kladr_id
#           }
#        ],
#        "restrict_value": True,
#        "from_bound": {
#           "value": "street"
#        },
#        "to_bound": {
#           "value": "street"
#        },
#        "query": text_street,
#        "count": 5
#     }
#     headers = {
#         'Accept': 'application/json, text/javascript, */*; q=0.01',
#         'Accept-Encoding': 'gzip, deflate, br',
#         'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,zh;q=0.5',
#         'Connection': 'keep-alive',
#         'Content-Type': 'application/json',
#         'Host': 'dadata.alfastrah.ru:8443',
#         'Origin': 'https://www.alfastrah.ru',
#         'Referer': 'https://www.alfastrah.ru/',
#         'Sec-Fetch-Dest': 'empty',
#         'Sec-Fetch-Mode': 'cors',
#         'Sec-Fetch-Site': 'same-site',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
#         'X-Version': '16.6.3',
#         'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
#         'sec-ch-ua-mobile': '?0',
#         'sec-ch-ua-platform': '"Windows"',
#     }
#     r = requests.post('https://dadata.alfastrah.ru:8443/suggestions/api/4_1/rs/suggest/address', headers=headers,
#                       data=json.dumps(data).encode('utf-8'))
#     print(r.json())
#     list_street = []
#     for one_region in r.json()['suggestions']:
#         list_street.append(one_region['value'])
#     return {'data': list_street}


def control_child_osago(type_osago, osago_id):
    dict_strah_comp = {'ВСК': 'osago_vsk', 'АльфаСтрахование': 'osago_alfa'}
    db = SessionLocal()
    osago = db.query(get_exemp_by_type_osago(type_osago=type_osago)).filter_by(id=osago_id).first()
    list_child_osago_type = []
    for child_osago in osago.list_child_osago:
        list_child_osago_type.append(child_osago.type_osago)


    for strah_comp in osago.strah_comp.split(','):
        if strah_comp != '' and list_child_osago_type.count(dict_strah_comp[strah_comp]) == 0 and type_osago != dict_strah_comp[strah_comp]:
            print(dict_strah_comp[strah_comp])
            id_duplicate_osago = duplicate_osago(osago_id=osago_id, type_osago=type_osago, count=1)
            id_transit_osago = transit_osago(type_osago=type_osago, osago_id=id_duplicate_osago, type_osago_to=dict_strah_comp[strah_comp])
            exemp_transit_osago = db.query(get_exemp_by_type_osago(type_osago=dict_strah_comp[strah_comp])).filter_by(id=id_transit_osago).first()
            exemp_transit_osago.is_main_osago = False
            exemp_transit_osago.main_osago_id = osago.id
            exemp_transit_osago.main_osago_type = osago.type_osago


    osago_strah_comp_type = []
    for strah_comp in osago.strah_comp.split(','):
        if strah_comp != '':
            osago_strah_comp_type.append(dict_strah_comp[strah_comp])
    for child_osago_type in list_child_osago_type:
        if osago_strah_comp_type.count(child_osago_type) == 0:
            del_osago = db.query(get_exemp_by_type_osago(type_osago=child_osago_type)).filter_by(main_osago_id=osago_id, main_osago_type=type_osago).first()
            for vod in del_osago.voditeli:
                db.delete(vod)
            db.delete(del_osago)
    db.commit()

def get_exemp_by_type_osago(type_osago):
    if type_osago == 'osago_vsk':
        return OsagoVsk
    elif type_osago == 'osago_alfa':
        return OsagoAlfa

def get_exemp_by_type_vod(type_osago):
    if type_osago == 'osago_vsk':
        return VoditelVsk
    elif type_osago == 'osago_alfa':
        return VoditelAlfa

def get_exemp_by_type_osago_pydantic(type_osago):
    if type_osago == 'osago_vsk':
        return PydanticOsagoVsk
    elif type_osago == 'osago_alfa':
        return PydanticOsagoAlfa

def del_child_osago(type_osago, osago_id):
    db = SessionLocal()
    main_osago = db.query(get_exemp_by_type_osago(type_osago=type_osago)).filter_by(id=osago_id).first()

    for osago in main_osago.list_child_osago:
        with suppress(Exception):
            server = osago.server
            server.status_server = db.query(StatusServer).filter_by(name='Свободен').first()
        for vod in osago.voditeli:
            db.delete(vod)
        db.delete(osago)
    db.commit()

def deep_delete_osago(type_osago, osago_id):
    db = SessionLocal()

    osago = db.query(get_exemp_by_type_osago(type_osago=type_osago)).filter_by(id=osago_id).first()
    with suppress(Exception):
        server = osago.server
        server.status_server = db.query(StatusServer).filter_by(name='Свободен').first()
    for vod in osago.voditeli:
        db.delete(vod)
    db.delete(osago)
    db.commit()


class NoFreeServer(Exception):
    pass