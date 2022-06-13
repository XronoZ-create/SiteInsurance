from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database_insurance import Base, SessionLocal
import random
from app import login_manager
from flask_login import UserMixin
from app import login_manager
from datetime import datetime, timedelta

class OsagoOsk(Base):
    __tablename__ = 'osago_osk'
    id = Column(Integer, primary_key=True)

    type_osago = Column(String, default="osago_osk")

    url_rca = Column(String, default="")
    login_rca = Column(String, default="")
    password_rca = Column(String, default="")

    login_osk = Column(String, default="")
    password_osk = Column(String, default="")

    email_login = Column(String, default="")
    email_password = Column(String, default="")

    surname = Column(String, default="")
    name = Column(String, default="")
    otchestvo = Column(String, default="")
    birthday = Column(String, default="")
    pass_seriya = Column(String, default="")
    pass_number = Column(String, default="")
    pass_vidach = Column(String, default="")
    pass_address = Column(String, default="")

    sobstv_yavl_strah = Column(String, default="")
    sobstv_surname = Column(String, default="")
    sobstv_name = Column(String, default="")
    sobstv_otchestvo = Column(String, default="")
    sobstv_birthday = Column(String, default="")
    sobstv_pass_seriya = Column(String, default="")
    sobstv_pass_number = Column(String, default="")
    sobstv_pass_vidach = Column(String, default="")
    sobstv_pass_address = Column(String, default="")

    target = Column(String, default="")
    mark = Column(String, default="")
    model = Column(String, default="")
    category = Column(String, default="")
    other_mark = Column(String, default="")
    year = Column(String, default="")
    powers = Column(String, default="")
    type_engine = Column(String, default="")
    type_cusov = Column(String, default="")
    transmission = Column(String, default="")
    modification = Column(String, default="")

    max_mass = Column(String, default="")
    pricep = Column(String, default="")

    count_pass_mest = Column(String, default="")

    type_document = Column(String, default="")

    ctc_ptc_seriya = Column(String, default="")
    ctc_ptc_number = Column(String, default="")
    ctc_ptc_vidach = Column(String, default="")
    ctc_ptc_reg_znak = Column(String, default="")
    ctc_ptc_vin = Column(String, default="")
    ctc_ptc_nomer_shassi = Column(String, default="")
    ctc_ptc_nomer_cusov = Column(String, default="")

    nomer_dk = Column(String, default="")
    data_TO = Column(String, default="")

    c_ogr_or_not = Column(String, default="")

    voditeli = relationship("VoditelOsk", backref="osago")

    OSAGO_start = Column(String, default="")
    OSAGO_count_mouth = Column(String, default="")

    strah_comp = Column(String, default="")

    server_id = Column(Integer, ForeignKey("server.id"))
    user_id = Column(Integer, ForeignKey("user.id"))

    trans_num = Column(String, default="")
    est_price_policy = Column(String, default="")
    real_price_policy = Column(String, default="")
    num_group_wa = Column(String, default="")

    status_osago_id = Column(Integer, ForeignKey("status_osago.id"), default=1)

    status_bot = Column(String, default="Бот остановлен")

    priority_application = Column(Boolean, default=False)
    reg_date = Column(String, default="")
    oformitel_id = Column(Integer, default=None)
    success_date = Column(String, default="")

    reg_date_telephone = Column(String, default="")
    telephone = Column(String, default="")
    id_num_telephone = Column(String, default="")
    telephone_service = Column(String, default="")

    @property
    def user_name(self):
        db_user = SessionLocal()
        return db_user.query(User).filter_by(id=self.user_id).first().username
    @property
    def oformitel_name(self):
        db_user = SessionLocal()
        oformitel = db_user.query(User).filter_by(id=self.oformitel_id).first()
        if oformitel != None:
            return oformitel.username
        else:
            return ""
    @property
    def reg_date_minutes(self):
        return (datetime.now() - datetime.strptime(self.reg_date, "%d.%m.%Y %H:%M")).minute

class VoditelOsk(Base):
    __tablename__ = 'voditel_osk'
    id = Column(Integer, primary_key=True)

    surname = Column(String, default="")
    name = Column(String, default="")
    otchestvo = Column(String, default="")
    birthday = Column(String, default="")
    seriya_vu = Column(String, default="")
    nomer_vu = Column(String, default="")
    data_vidachi_vu = Column(String, default="")
    nachalo_staga = Column(String, default="")

    osago_id = Column(Integer, ForeignKey("osago_osk.id"))


class OsagoUGSK(Base):
    __tablename__ = 'osago_ugsk'
    id = Column(Integer, primary_key=True)

    type_osago = Column(String, default="osago_ugsk")

    url_rca = Column(String, default="")
    login_rca = Column(String, default="")
    password_rca = Column(String, default="")

    login_osk = Column(String, default="")
    password_osk = Column(String, default="")

    email_login = Column(String, default="")
    email_password = Column(String, default="")

    surname = Column(String, default="")
    name = Column(String, default="")
    otchestvo = Column(String, default="")
    birthday = Column(String, default="")
    pass_seriya = Column(String, default="")
    pass_number = Column(String, default="")
    pass_vidach = Column(String, default="")
    pass_address = Column(String, default="")

    sobstv_yavl_strah = Column(String, default="")
    sobstv_surname = Column(String, default="")
    sobstv_name = Column(String, default="")
    sobstv_otchestvo = Column(String, default="")
    sobstv_birthday = Column(String, default="")
    sobstv_pass_seriya = Column(String, default="")
    sobstv_pass_number = Column(String, default="")
    sobstv_pass_vidach = Column(String, default="")
    sobstv_pass_address = Column(String, default="")

    target = Column(String, default="")
    mark = Column(String, default="")
    model = Column(String, default="")
    category = Column(String, default="")
    other_mark = Column(String, default="")
    year = Column(String, default="")
    powers = Column(String, default="")
    type_engine = Column(String, default="")
    type_cusov = Column(String, default="")
    transmission = Column(String, default="")
    modification = Column(String, default="")

    max_mass = Column(String, default="")
    pricep = Column(String, default="")

    count_pass_mest = Column(String, default="")

    type_document = Column(String, default="")

    ctc_ptc_seriya = Column(String, default="")
    ctc_ptc_number = Column(String, default="")
    ctc_ptc_vidach = Column(String, default="")
    ctc_ptc_reg_znak = Column(String, default="")
    ctc_ptc_vin = Column(String, default="")
    ctc_ptc_nomer_shassi = Column(String, default="")
    ctc_ptc_nomer_cusov = Column(String, default="")

    nomer_dk = Column(String, default="")
    data_TO = Column(String, default="")

    c_ogr_or_not = Column(String, default="")

    voditeli = relationship("VoditelUGSK", backref="osago")

    OSAGO_start = Column(String, default="")
    OSAGO_count_mouth = Column(String, default="")

    strah_comp = Column(String, default="")

    server_id = Column(Integer, ForeignKey("server.id"))
    user_id = Column(Integer, ForeignKey("user.id"))

    trans_num = Column(String, default="")
    est_price_policy = Column(String, default="")
    real_price_policy = Column(String, default="")
    num_group_wa = Column(String, default="")

    status_osago_id = Column(Integer, ForeignKey("status_osago.id"), default=1)

    status_bot = Column(String, default="Бот остановлен")

    priority_application = Column(Boolean, default=False)
    reg_date = Column(String, default="")
    oformitel_id = Column(Integer, default=None)
    success_date = Column(String, default="")

    reg_date_telephone = Column(String, default="")
    telephone = Column(String, default="")
    id_num_telephone = Column(String, default="")
    telephone_service = Column(String, default="")

    @property
    def user_name(self):
        db_user = SessionLocal()
        return db_user.query(User).filter_by(id=self.user_id).first().username
    @property
    def oformitel_name(self):
        db_user = SessionLocal()
        oformitel = db_user.query(User).filter_by(id=self.oformitel_id).first()
        if oformitel != None:
            return oformitel.username
        else:
            return ""
    @property
    def reg_date_minutes(self):
        return ((datetime.strptime(self.reg_date, "%d.%m.%Y %H:%M") + timedelta(minutes=15)) - datetime.now()).seconds % 3600 / 60
    @property
    def prepared(self):
        if self.mark != "":
            return True
        else:
            return False

class VoditelUGSK(Base):
    __tablename__ = 'voditel_ugsk'
    id = Column(Integer, primary_key=True)

    surname = Column(String, default="")
    name = Column(String, default="")
    otchestvo = Column(String, default="")
    birthday = Column(String, default="")
    seriya_vu = Column(String, default="")
    nomer_vu = Column(String, default="")
    data_vidachi_vu = Column(String, default="")
    nachalo_staga = Column(String, default="")
    foreign_dl = Column(Boolean, default=False)
    tr = Column(Boolean, default=False)

    osago_id = Column(Integer, ForeignKey("osago_ugsk.id"))


class Osago21(Base):
    __tablename__ = 'osago_21'
    id = Column(Integer, primary_key=True)

    type_osago = Column(String, default="osago_21")

    url_rca = Column(String, default="")
    login_rca = Column(String, default="")
    password_rca = Column(String, default="")

    login_osk = Column(String, default="")
    password_osk = Column(String, default="")

    email_login = Column(String, default="")
    email_password = Column(String, default="")

    surname = Column(String, default="")
    name = Column(String, default="")
    otchestvo = Column(String, default="")
    birthday = Column(String, default="")
    pass_seriya = Column(String, default="")
    pass_number = Column(String, default="")
    pass_vidach = Column(String, default="")
    pass_address = Column(String, default="")
    strah_type_document = Column(String, default="RussianPassport")

    sobstv_yavl_strah = Column(String, default="")
    sobstv_surname = Column(String, default="")
    sobstv_name = Column(String, default="")
    sobstv_otchestvo = Column(String, default="")
    sobstv_birthday = Column(String, default="")
    sobstv_pass_seriya = Column(String, default="")
    sobstv_pass_number = Column(String, default="")
    sobstv_pass_vidach = Column(String, default="")
    sobstv_pass_address = Column(String, default="")
    sobstv_type_document = Column(String, default="RussianPassport")

    target = Column(String, default="")
    mark = Column(String, default="")
    model = Column(String, default="")
    category = Column(String, default="")
    other_mark = Column(String, default="")
    year = Column(String, default="")
    powers = Column(String, default="")
    type_engine = Column(String, default="")
    type_cusov = Column(String, default="")
    transmission = Column(String, default="")
    modification = Column(String, default="")

    max_mass = Column(String, default="")
    pricep = Column(String, default="")

    count_pass_mest = Column(String, default="")

    type_document = Column(String, default="")

    ctc_ptc_seriya = Column(String, default="")
    ctc_ptc_number = Column(String, default="")
    ctc_ptc_vidach = Column(String, default="")
    ctc_ptc_reg_znak = Column(String, default="")
    ctc_ptc_vin = Column(String, default="")
    ctc_ptc_nomer_shassi = Column(String, default="")
    ctc_ptc_nomer_cusov = Column(String, default="")

    nomer_dk = Column(String, default="")
    data_TO = Column(String, default="")

    c_ogr_or_not = Column(String, default="")

    voditeli = relationship("Voditel21", backref="osago")

    OSAGO_start = Column(String, default="")
    OSAGO_count_mouth = Column(String, default="")

    strah_comp = Column(String, default="")

    server_id = Column(Integer, ForeignKey("server.id"))
    user_id = Column(Integer, ForeignKey("user.id"))

    trans_num = Column(String, default="")
    est_price_policy = Column(String, default="")
    real_price_policy = Column(String, default="")
    num_group_wa = Column(String, default="")

    status_osago_id = Column(Integer, ForeignKey("status_osago.id"), default=1)

    status_bot = Column(String, default="Бот остановлен")

    priority_application = Column(Boolean, default=False)
    reg_date = Column(String, default="")
    oformitel_id = Column(Integer, default=None)
    success_date = Column(String, default="")

    reg_date_telephone = Column(String, default="")
    telephone = Column(String, default="")
    id_num_telephone = Column(String, default="")
    telephone_service = Column(String, default="")

    @property
    def user_name(self):
        db_user = SessionLocal()
        return db_user.query(User).filter_by(id=self.user_id).first().username
    @property
    def oformitel_name(self):
        db_user = SessionLocal()
        oformitel = db_user.query(User).filter_by(id=self.oformitel_id).first()
        if oformitel != None:
            return oformitel.username
        else:
            return ""
    @property
    def reg_date_minutes(self):
        return ((datetime.strptime(self.reg_date, "%d.%m.%Y %H:%M") + timedelta(minutes=15)) - datetime.now()).seconds % 3600 / 60
    @property
    def prepared(self):
        if self.mark != "":
            return True
        else:
            return False

class Voditel21(Base):
    __tablename__ = 'voditel_21'
    id = Column(Integer, primary_key=True)

    surname = Column(String, default="")
    name = Column(String, default="")
    otchestvo = Column(String, default="")
    birthday = Column(String, default="")
    seriya_vu = Column(String, default="")
    nomer_vu = Column(String, default="")
    data_vidachi_vu = Column(String, default="")
    nachalo_staga = Column(String, default="")
    foreign_dl = Column(Boolean, default=False)
    tr = Column(Boolean, default=False)

    osago_id = Column(Integer, ForeignKey("osago_21.id"))



class OsagoArm(Base):
    __tablename__ = 'osago_arm'
    id = Column(Integer, primary_key=True)

    type_osago = Column(String, default="osago_arm")

    url_rca = Column(String, default="")
    login_rca = Column(String, default="")
    password_rca = Column(String, default="")

    login_osk = Column(String, default="")
    password_osk = Column(String, default="")

    email_login = Column(String, default="")
    email_password = Column(String, default="")

    surname = Column(String, default="")
    name = Column(String, default="")
    otchestvo = Column(String, default="")
    birthday = Column(String, default="")
    pass_seriya = Column(String, default="")
    pass_number = Column(String, default="")
    pass_vidach = Column(String, default="")
    pass_address = Column(String, default="")

    sobstv_yavl_strah = Column(String, default="")
    sobstv_surname = Column(String, default="")
    sobstv_name = Column(String, default="")
    sobstv_otchestvo = Column(String, default="")
    sobstv_birthday = Column(String, default="")
    sobstv_pass_seriya = Column(String, default="")
    sobstv_pass_number = Column(String, default="")
    sobstv_pass_vidach = Column(String, default="")
    sobstv_pass_address = Column(String, default="")

    target = Column(String, default="")
    mark = Column(String, default="")
    model = Column(String, default="")
    category = Column(String, default="")
    other_mark = Column(String, default="")
    year = Column(String, default="")
    powers = Column(String, default="")
    type_engine = Column(String, default="")
    type_cusov = Column(String, default="")
    transmission = Column(String, default="")
    modification = Column(String, default="")

    max_mass = Column(String, default="")
    pricep = Column(String, default="")

    count_pass_mest = Column(String, default="")

    type_document = Column(String, default="")

    ctc_ptc_seriya = Column(String, default="")
    ctc_ptc_number = Column(String, default="")
    ctc_ptc_vidach = Column(String, default="")
    ctc_ptc_reg_znak = Column(String, default="")
    ctc_ptc_vin = Column(String, default="")
    ctc_ptc_nomer_shassi = Column(String, default="")
    ctc_ptc_nomer_cusov = Column(String, default="")

    nomer_dk = Column(String, default="")
    data_TO = Column(String, default="")

    c_ogr_or_not = Column(String, default="")

    voditeli = relationship("VoditelArm", backref="osago")

    OSAGO_start = Column(String, default="")
    OSAGO_count_mouth = Column(String, default="")

    strah_comp = Column(String, default="")

    server_id = Column(Integer, ForeignKey("server.id"))
    user_id = Column(Integer, ForeignKey("user.id"))

    trans_num = Column(String, default="")
    est_price_policy = Column(String, default="")
    real_price_policy = Column(String, default="")
    num_group_wa = Column(String, default="")

    status_osago_id = Column(Integer, ForeignKey("status_osago.id"), default=1)

    status_bot = Column(String, default="Бот остановлен")

    priority_application = Column(Boolean, default=False)
    reg_date = Column(String, default="")
    oformitel_id = Column(Integer, default=None)
    success_date = Column(String, default="")

    proxy = Column(String, default="")
    pump = Column(Boolean, default=False)
    proxy_batut = Column(String, default="")

    prepare_pump = Column(Boolean, default=False)

    reg_date_telephone = Column(String, default="")
    telephone = Column(String, default="")
    id_num_telephone = Column(String, default="")
    telephone_service = Column(String, default="")

    @property
    def user_name(self):
        db_user = SessionLocal()
        return db_user.query(User).filter_by(id=self.user_id).first().username
    @property
    def oformitel_name(self):
        db_user = SessionLocal()
        oformitel = db_user.query(User).filter_by(id=self.oformitel_id).first()
        if oformitel != None:
            return oformitel.username
        else:
            return ""
    @property
    def reg_date_minutes(self):
        return ((datetime.strptime(self.reg_date, "%d.%m.%Y %H:%M") + timedelta(minutes=15)) - datetime.now()).seconds % 3600 / 60
    @property
    def prepared(self):
        if self.mark != "":
            return True
        else:
            return False

class VoditelArm(Base):
    __tablename__ = 'voditel_arm'
    id = Column(Integer, primary_key=True)

    surname = Column(String, default="")
    name = Column(String, default="")
    otchestvo = Column(String, default="")
    birthday = Column(String, default="")
    seriya_vu = Column(String, default="")
    nomer_vu = Column(String, default="")
    data_vidachi_vu = Column(String, default="")
    nachalo_staga = Column(String, default="")
    foreign_dl = Column(Boolean, default=False)
    tr = Column(Boolean, default=False)

    osago_id = Column(Integer, ForeignKey("osago_arm.id"))


class OsagoAlfa(Base):
    __tablename__ = 'osago_alfa'
    id = Column(Integer, primary_key=True)

    type_osago = Column(String, default="osago_alfa")

    is_main_osago = Column(Boolean, default=False)
    main_osago_id = Column(String, default="")
    main_osago_type = Column(String, default="")

    login_parea = Column(String, default="")
    password_parea = Column(String, default="")

    email_login = Column(String, default="")
    email_password = Column(String, default="")

    surname = Column(String, default="")
    name = Column(String, default="")
    otchestvo = Column(String, default="")
    birthday = Column(String, default="")
    pass_seriya = Column(String, default="")
    pass_number = Column(String, default="")
    pass_vidach = Column(String, default="")
    pass_address = Column(String, default="")

    sobstv_yavl_strah = Column(String, default="")
    sobstv_surname = Column(String, default="")
    sobstv_name = Column(String, default="")
    sobstv_otchestvo = Column(String, default="")
    sobstv_birthday = Column(String, default="")
    sobstv_pass_seriya = Column(String, default="")
    sobstv_pass_number = Column(String, default="")
    sobstv_pass_vidach = Column(String, default="")
    sobstv_pass_address = Column(String, default="")


    target = Column(String, default="")
    category = Column(String, default="")
    year = Column(String, default="")
    powers = Column(String, default="")
    auto_region = Column(String, default="")
    auto_type = Column(String, default="")
    brand_name = Column(String, default="")
    brand = Column(String, default="")
    brand_name_other = Column(String, default="")
    model = Column(String, default="")
    model_name_other = Column(String, default="")
    model_name = Column(String, default="")
    modification = Column(String, default="")
    modification_name = Column(String, default="")


    max_mass = Column(String, default="")
    pricep = Column(String, default="")

    count_pass_mest = Column(String, default="")

    type_document = Column(String, default="")

    ctc_ptc_seriya = Column(String, default="")
    ctc_ptc_number = Column(String, default="")
    ctc_ptc_vidach = Column(String, default="")
    ctc_ptc_reg_znak = Column(String, default="")
    ctc_ptc_vin = Column(String, default="")
    ctc_ptc_nomer_shassi = Column(String, default="")
    ctc_ptc_nomer_cusov = Column(String, default="")

    nomer_dk = Column(String, default="")
    data_TO = Column(String, default="")

    c_ogr_or_not = Column(String, default="")

    voditeli = relationship("VoditelAlfa", backref="osago")

    OSAGO_start = Column(String, default="")
    OSAGO_count_mouth = Column(String, default="")

    strah_comp = Column(String, default="")

    server_id = Column(Integer, ForeignKey("server.id"))
    user_id = Column(Integer, ForeignKey("user.id"))

    trans_num = Column(String, default="")
    est_price_policy = Column(String, default="")
    real_price_policy = Column(String, default="")
    num_group_wa = Column(String, default="")

    status_osago_id = Column(Integer, ForeignKey("status_osago.id"), default=1)

    status_bot = Column(String, default="Бот остановлен")

    priority_application = Column(Boolean, default=False)
    reg_date = Column(String, default="")
    oformitel_id = Column(Integer, default=None)
    success_date = Column(String, default="")

    reg_date_telephone = Column(String, default="")
    telephone = Column(String, default="")
    id_num_telephone = Column(String, default="")
    telephone_service = Column(String, default="")

    url_pay = Column(String, default="")

    @property
    def user_name(self):
        db_user = SessionLocal()
        return db_user.query(User).filter_by(id=self.user_id).first().username
    @property
    def oformitel_name(self):
        db_user = SessionLocal()
        oformitel = db_user.query(User).filter_by(id=self.oformitel_id).first()
        if oformitel != None:
            return oformitel.username
        else:
            return ""
    @property
    def reg_date_minutes(self):
        return ((datetime.strptime(self.reg_date, "%d.%m.%Y %H:%M") + timedelta(minutes=15)) - datetime.now()).seconds % 3600 / 60
    @property
    def prepared(self):
        if not self.is_main_osago:
            return False
        for self.child_osago in self.list_child_osago:
            if not self.child_osago.prepared:
                return False
        if self.brand_name != "":
            return True
        else:
            return False
    @property
    def list_child_osago(self):
        if self.is_main_osago:
            self.db = SessionLocal()
            self.all_child_osago = []

            self.all_child_osago.extend(self.db.query(OsagoVsk).filter_by(main_osago_id=self.id, main_osago_type='osago_alfa').all())

            return self.all_child_osago
    @property
    def name_type(self):
        return 'Альфа'

class VoditelAlfa(Base):
    __tablename__ = 'voditel_alfa'
    id = Column(Integer, primary_key=True)

    surname = Column(String, default="")
    name = Column(String, default="")
    otchestvo = Column(String, default="")
    birthday = Column(String, default="")
    seriya_vu = Column(String, default="")
    nomer_vu = Column(String, default="")
    data_vidachi_vu = Column(String, default="")
    nachalo_staga = Column(String, default="")
    foreign_dl = Column(Boolean, default=False)
    tr = Column(Boolean, default=False)

    osago_id = Column(Integer, ForeignKey("osago_alfa.id"))


class OsagoVsk(Base):
    __tablename__ = 'osago_vsk'
    id = Column(Integer, primary_key=True)

    session_cookies = Column(String, default="")
    session_cookies_date = Column(String, default="")
    session_id = Column(String, default="")

    type_osago = Column(String, default="osago_vsk")

    is_main_osago = Column(Boolean, default=False)
    main_osago_id = Column(String, default="")
    main_osago_type = Column(String, default="")

    login_parea = Column(String, default="")
    password_parea = Column(String, default="")

    email_login = Column(String, default="")
    email_password = Column(String, default="")

    surname = Column(String, default="")
    name = Column(String, default="")
    otchestvo = Column(String, default="")
    birthday = Column(String, default="")
    pass_seriya = Column(String, default="")
    pass_number = Column(String, default="")
    pass_vidach = Column(String, default="")
    city_strah = Column(String, default="")
    street_strah = Column(String, default="")
    building_strah = Column(String, default="")
    house_strah = Column(String, default="")
    apartment_strah = Column(String, default="")
    postal_code_strah = Column(String, default="")
    strah_type_document = Column(String, default="RussianPassport")

    sobstv_yavl_strah = Column(String, default="")
    sobstv_surname = Column(String, default="")
    sobstv_name = Column(String, default="")
    sobstv_otchestvo = Column(String, default="")
    sobstv_birthday = Column(String, default="")
    sobstv_pass_seriya = Column(String, default="")
    sobstv_pass_number = Column(String, default="")
    sobstv_pass_vidach = Column(String, default="")
    city_sobstv = Column(String, default="")
    street_sobstv = Column(String, default="")
    building_sobstv = Column(String, default="")
    house_sobstv = Column(String, default="")
    apartment_sobstv = Column(String, default="")
    postal_code_sobstv = Column(String, default="")
    sobstv_type_document = Column(String, default="RussianPassport")


    target = Column(String, default="")
    category = Column(String, default="")
    year = Column(String, default="")
    powers = Column(String, default="")
    mark = Column(String, default="")
    model = Column(String, default="")
    mark_name_other = Column(String, default="")
    model_name_other = Column(String, default="")
    mark_id = Column(String, default="")
    model_id = Column(String, default="")


    max_mass = Column(String, default="")
    count_pass_mest = Column(String, default="")
    pricep = Column(String, default="")

    type_document = Column(String, default="")

    ctc_ptc_seriya = Column(String, default="")
    ctc_ptc_number = Column(String, default="")
    ctc_ptc_vidach = Column(String, default="")
    ctc_ptc_reg_znak = Column(String, default="")
    ctc_ptc_vin = Column(String, default="")
    ctc_ptc_nomer_shassi = Column(String, default="")
    ctc_ptc_nomer_cusov = Column(String, default="")

    nomer_dk = Column(String, default="")
    data_TO = Column(String, default="")

    c_ogr_or_not = Column(String, default="")

    voditeli = relationship("VoditelVsk", backref="osago")

    OSAGO_start = Column(String, default="")
    OSAGO_count_mouth = Column(String, default="")

    strah_comp = Column(String, default="")

    server_id = Column(Integer, ForeignKey("server.id"))
    user_id = Column(Integer, ForeignKey("user.id"))

    trans_num = Column(String, default="")
    est_price_policy = Column(String, default="")
    real_price_policy = Column(String, default="")
    num_group_wa = Column(String, default="")

    status_osago_id = Column(Integer, ForeignKey("status_osago.id"), default=1)

    status_bot = Column(String, default="Бот остановлен")

    priority_application = Column(Boolean, default=False)
    reg_date = Column(String, default="")
    oformitel_id = Column(Integer, default=None)
    success_date = Column(String, default="")

    prepare_pump = Column(Boolean, default=False)

    reg_date_telephone = Column(String, default="")
    telephone = Column(String, default="")
    id_num_telephone = Column(String, default="")
    telephone_service = Column(String, default="")

    url_pay = Column(String, default="")

    @property
    def user_name(self):
        db_user = SessionLocal()
        return db_user.query(User).filter_by(id=self.user_id).first().username
    @property
    def oformitel_name(self):
        db_user = SessionLocal()
        oformitel = db_user.query(User).filter_by(id=self.oformitel_id).first()
        if oformitel != None:
            return oformitel.username
        else:
            return ""
    @property
    def reg_date_minutes(self):
        return ((datetime.strptime(self.reg_date, "%d.%m.%Y %H:%M") + timedelta(minutes=15)) - datetime.now()).seconds % 3600 / 60
    @property
    def prepared(self):
        if not self.is_main_osago:
            return False
        for self.child_osago in self.list_child_osago:
            if not self.child_osago.prepared:
                return False
        if self.mark != "":
            return True
        else:
            return False
    @property
    def list_child_osago(self):
        if self.is_main_osago:
            self.db = SessionLocal()
            self.all_child_osago = []

            self.all_child_osago.extend(self.db.query(OsagoAlfa).filter_by(main_osago_id=self.id, main_osago_type='osago_vsk').all())
            return self.all_child_osago
    @property
    def name_type(self):
        return 'ВСК'


class VoditelVsk(Base):
    __tablename__ = 'voditel_vsk'
    id = Column(Integer, primary_key=True)

    surname = Column(String, default="")
    name = Column(String, default="")
    otchestvo = Column(String, default="")
    birthday = Column(String, default="")
    seriya_vu = Column(String, default="")
    nomer_vu = Column(String, default="")
    data_vidachi_vu = Column(String, default="")
    nachalo_staga = Column(String, default="")
    foreign_dl = Column(Boolean, default=False)
    tr = Column(Boolean, default=False)

    osago_id = Column(Integer, ForeignKey("osago_vsk.id"))



class StatusOsago(Base):
    __tablename__ = 'status_osago'
    id = Column(Integer, primary_key=True)

    name = Column(String)
    osago_osk = relationship("OsagoOsk", backref="status_osago")
    osago_ugsk = relationship("OsagoUGSK", backref="status_osago")
    osago_21 = relationship("Osago21", backref="status_osago")
    osago_arm = relationship("OsagoArm", backref="status_osago")
    osago_alfa = relationship("OsagoAlfa", backref="status_osago")
    osago_vsk = relationship("OsagoVsk", backref="status_osago")

    @property
    def osago(self):
        self.osago_list = self.osago_osk + self.osago_ugsk + self.osago_21 + self.osago_arm + self.osago_alfa + self.osago_vsk
        return self.osago_list

class Server(Base):
    __tablename__ = 'server'
    id = Column(Integer, primary_key=True)

    server_address = Column(String)
    status_server_id = Column(Integer, ForeignKey('status_server.id'), default=2)
    date_last_status = Column(String)

    osago_osk = relationship("OsagoOsk", backref="server")
    hook = relationship("Hook", backref="server")
    osago_ugsk = relationship("OsagoUGSK", backref="server")
    osago_21 = relationship("Osago21", backref="server")
    osago_arm = relationship("OsagoArm", backref="server")
    osago_alfa = relationship("OsagoAlfa", backref="server")
    osago_vsk = relationship("OsagoVsk", backref="server")

    @property
    def osago(self):
        self.osago_list = self.osago_osk + self.osago_ugsk + self.osago_21 + self.osago_arm + self.osago_alfa + self.osago_vsk
        return self.osago_list

class StatusServer(Base):
    __tablename__ = 'status_server'
    id = Column(Integer, primary_key=True)

    name = Column(String)
    servers = relationship("Server", backref="status_server")


class Hook(Base):
    __tablename__ = 'hook'
    id = Column(Integer, primary_key=True)

    name = Column(String, default="")
    input_url = Column(String, default="")
    url_rca = Column(String, default="")
    strah_comp = Column(String, default="")

    status_bot = Column(String, default="Бот остановлен")

    server_id = Column(Integer, ForeignKey("server.id"))

    user_id = Column(Integer, ForeignKey("user.id"))

# -----------------------------------------Пользователи и сайт----------------------------------------------------------
class User(UserMixin, Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)

    username = Column(String(64), unique=True, index=True)
    password_hash = Column(String(128))

    surname = Column(String(128))
    name = Column(String(128))
    otchestvo = Column(String(128))

    role_id = Column(Integer, ForeignKey("role.id"))

    osago_osk = relationship("OsagoOsk", backref="user")
    hook = relationship("Hook", backref="user")
    osago_ugsk = relationship("OsagoUGSK", backref="user")
    osago_21 = relationship("Osago21", backref="user")
    osago_arm = relationship("OsagoArm", backref="user")
    osago_alfa = relationship("OsagoAlfa", backref="user")
    osago_vsk = relationship("OsagoVsk", backref="user")

    selected_otv_name = Column(String(128), default="")
    selected_oformitel_name = Column(String(128), default="")

    email_address = Column(String, default="")
    email_password = Column(String, default="")

    @property
    def osago(self):
        self.osago_list = self.osago_osk + self.osago_ugsk + self.osago_21 + self.osago_arm + self.osago_alfa + self.osago_vsk
        return self.osago_list
    @property
    def osago_active(self):
        self.osago_list = []

        self.db = SessionLocal()
        self.all_osago_1 = self.db.query(StatusOsago).filter_by(id=1).first().osago
        self.all_osago_2 = self.db.query(StatusOsago).filter_by(id=2).first().osago
        self.all_osago_3 = self.db.query(StatusOsago).filter_by(id=3).first().osago
        self.all_osago_6 = self.db.query(StatusOsago).filter_by(id=6).first().osago
        for self.one_osago in self.all_osago_1+self.all_osago_2+self.all_osago_3+self.all_osago_6:
            if ((self.one_osago.oformitel_id != None and self.one_osago.oformitel_id == self.id) or (self.role_id == 1 or self.role_id == 3) or (self.one_osago.user_id == self.id)) and self.one_osago.is_main_osago:
                self.osago_list.append(self.one_osago)
        return self.osago_list
    @property
    def osago_success(self):
        self.osago_list = []
        for self.one_osago in self.osago_ugsk + self.osago_osk+self.osago_21 + self.osago_arm + self.osago_alfa + self.osago_vsk:
            if self.one_osago.status_osago_id == 4:
                self.osago_list.append(self.one_osago)
        return self.osago_list
    @property
    def osago_delete(self):
        self.osago_list = []
        for self.one_osago in self.osago_ugsk + self.osago_osk+self.osago_21 + self.osago_arm + self.osago_alfa + self.osago_vsk:
            if self.one_osago.status_osago_id == 5:
                self.osago_list.append(self.one_osago)
        return self.osago_list

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    def verify_password(self, password):
        if password == self.password_hash:
            return True
        else:
            return False


    def __repr__(self):
        return '<User %r>' % self.username

@login_manager.user_loader
def load_user(user_id):
    db = SessionLocal()
    return db.query(User).get(int(user_id))

class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True)

    name = Column(String)
    user = relationship("User", backref="role")

class Config(Base):
    __tablename__ = 'config'
    id = Column(Integer, primary_key=True)

    name = Column(String)
    value = Column(String)
