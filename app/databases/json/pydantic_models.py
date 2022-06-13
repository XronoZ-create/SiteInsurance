from pydantic import BaseModel
from typing import List

class PydanticHook(BaseModel):
    id: int
    input_url: str
    url_rca: str
    strah_comp: str
    status_bot: str

    class Config:
        orm_mode = True

class PydanticVoditeliOsk(BaseModel):
    surname: str
    name: str
    otchestvo: str
    birthday: str
    seriya_vu: str
    nomer_vu: str
    data_vidachi_vu: str
    nachalo_staga: str

    class Config:
        orm_mode = True

class PydanticVoditeliUGSK(BaseModel):
    surname: str
    name: str
    otchestvo: str
    birthday: str
    seriya_vu: str
    nomer_vu: str
    data_vidachi_vu: str
    nachalo_staga: str
    foreign_dl: bool
    tr: bool

    class Config:
        orm_mode = True

class PydanticVoditeli21(BaseModel):
    surname: str
    name: str
    otchestvo: str
    birthday: str
    seriya_vu: str
    nomer_vu: str
    data_vidachi_vu: str
    nachalo_staga: str
    foreign_dl: bool
    tr: bool

    class Config:
        orm_mode = True

class PydanticVoditeliArm(BaseModel):
    surname: str
    name: str
    otchestvo: str
    birthday: str
    seriya_vu: str
    nomer_vu: str
    data_vidachi_vu: str
    nachalo_staga: str
    foreign_dl: bool
    tr: bool

    class Config:
        orm_mode = True

class PydanticVoditeliAlfa(BaseModel):
    surname: str
    name: str
    otchestvo: str
    birthday: str
    seriya_vu: str
    nomer_vu: str
    data_vidachi_vu: str
    nachalo_staga: str
    foreign_dl: bool
    tr: bool

    class Config:
        orm_mode = True

class PydanticVoditeliVsk(BaseModel):
    surname: str
    name: str
    otchestvo: str
    birthday: str
    seriya_vu: str
    nomer_vu: str
    data_vidachi_vu: str
    nachalo_staga: str
    foreign_dl: bool
    tr: bool

    class Config:
        orm_mode = True


class PydanticOsagoOsk(BaseModel):
    id: int

    type_osago: str

    url_rca: str
    login_rca: str
    password_rca: str

    login_osk: str
    password_osk: str

    email_login: str
    email_password: str

    surname: str
    name: str
    otchestvo: str
    birthday: str
    pass_seriya: str
    pass_number: str
    pass_vidach: str
    pass_address: str
    strah_type_document: str

    sobstv_yavl_strah: str
    sobstv_surname: str
    sobstv_name: str
    sobstv_otchestvo: str
    sobstv_birthday: str
    sobstv_pass_seriya: str
    sobstv_pass_number: str
    sobstv_pass_vidach: str
    sobstv_pass_address: str
    sobstv_type_document: str

    target: str
    mark: str
    model: str
    category: str
    other_mark: str
    year: str
    powers: str
    type_engine: str
    type_cusov: str
    transmission: str
    modification: str

    max_mass: str
    pricep: str

    count_pass_mest: str

    type_document: str

    ctc_ptc_seriya: str
    ctc_ptc_number: str
    ctc_ptc_vidach: str
    ctc_ptc_reg_znak: str
    ctc_ptc_vin: str
    ctc_ptc_nomer_shassi: str
    ctc_ptc_nomer_cusov: str

    nomer_dk: str
    data_TO: str

    c_ogr_or_not: str

    voditeli: List[PydanticVoditeliOsk]

    OSAGO_start: str
    OSAGO_count_mouth: str

    strah_comp: str

    trans_num: str
    est_price_policy: str
    real_price_policy: str
    num_group_wa: str

    status_bot: str

    reg_date_telephone: str
    telephone: str

    reg_date_telephone: str
    telephone: str
    id_num_telephone: str
    telephone_service: str

    class Config:
        orm_mode = True

class PydanticOsagoUGSK(BaseModel):
    id: int

    type_osago: str

    url_rca: str
    login_rca: str
    password_rca: str

    login_osk: str
    password_osk: str

    email_login: str
    email_password: str

    surname: str
    name: str
    otchestvo: str
    birthday: str
    pass_seriya: str
    pass_number: str
    pass_vidach: str
    pass_address: str

    sobstv_yavl_strah: str
    sobstv_surname: str
    sobstv_name: str
    sobstv_otchestvo: str
    sobstv_birthday: str
    sobstv_pass_seriya: str
    sobstv_pass_number: str
    sobstv_pass_vidach: str
    sobstv_pass_address: str

    target: str
    mark: str
    model: str
    category: str
    other_mark: str
    year: str
    powers: str
    type_engine: str
    type_cusov: str
    transmission: str
    modification: str

    max_mass: str
    pricep: str

    count_pass_mest: str

    type_document: str

    ctc_ptc_seriya: str
    ctc_ptc_number: str
    ctc_ptc_vidach: str
    ctc_ptc_reg_znak: str
    ctc_ptc_vin: str
    ctc_ptc_nomer_shassi: str
    ctc_ptc_nomer_cusov: str

    nomer_dk: str
    data_TO: str

    c_ogr_or_not: str

    voditeli: List[PydanticVoditeliUGSK]

    OSAGO_start: str
    OSAGO_count_mouth: str

    strah_comp: str

    trans_num: str
    est_price_policy: str
    real_price_policy: str
    num_group_wa: str

    status_bot: str

    reg_date_telephone: str
    telephone: str
    id_num_telephone: str
    telephone_service: str

    class Config:
        orm_mode = True

class PydanticOsago21(BaseModel):
    id: int

    type_osago: str

    url_rca: str
    login_rca: str
    password_rca: str

    login_osk: str
    password_osk: str

    email_login: str
    email_password: str

    surname: str
    name: str
    otchestvo: str
    birthday: str
    pass_seriya: str
    pass_number: str
    pass_vidach: str
    pass_address: str
    strah_type_document: str

    sobstv_yavl_strah: str
    sobstv_surname: str
    sobstv_name: str
    sobstv_otchestvo: str
    sobstv_birthday: str
    sobstv_pass_seriya: str
    sobstv_pass_number: str
    sobstv_pass_vidach: str
    sobstv_pass_address: str
    sobstv_type_document: str


    target: str
    mark: str
    model: str
    category: str
    other_mark: str
    year: str
    powers: str
    type_engine: str
    type_cusov: str
    transmission: str
    modification: str

    max_mass: str
    pricep: str

    count_pass_mest: str

    type_document: str

    ctc_ptc_seriya: str
    ctc_ptc_number: str
    ctc_ptc_vidach: str
    ctc_ptc_reg_znak: str
    ctc_ptc_vin: str
    ctc_ptc_nomer_shassi: str
    ctc_ptc_nomer_cusov: str

    nomer_dk: str
    data_TO: str

    c_ogr_or_not: str

    voditeli: List[PydanticVoditeli21]

    OSAGO_start: str
    OSAGO_count_mouth: str

    strah_comp: str

    trans_num: str
    est_price_policy: str
    real_price_policy: str
    num_group_wa: str

    status_bot: str

    reg_date_telephone: str
    telephone: str
    id_num_telephone: str
    telephone_service: str

    class Config:
        orm_mode = True

class PydanticOsagoArm(BaseModel):
    id: int

    type_osago: str

    url_rca: str
    login_rca: str
    password_rca: str

    login_osk: str
    password_osk: str

    email_login: str
    email_password: str

    surname: str
    name: str
    otchestvo: str
    birthday: str
    pass_seriya: str
    pass_number: str
    pass_vidach: str
    pass_address: str

    sobstv_yavl_strah: str
    sobstv_surname: str
    sobstv_name: str
    sobstv_otchestvo: str
    sobstv_birthday: str
    sobstv_pass_seriya: str
    sobstv_pass_number: str
    sobstv_pass_vidach: str
    sobstv_pass_address: str

    target: str
    mark: str
    model: str
    category: str
    other_mark: str
    year: str
    powers: str
    type_engine: str
    type_cusov: str
    transmission: str
    modification: str

    max_mass: str
    pricep: str

    count_pass_mest: str

    type_document: str

    ctc_ptc_seriya: str
    ctc_ptc_number: str
    ctc_ptc_vidach: str
    ctc_ptc_reg_znak: str
    ctc_ptc_vin: str
    ctc_ptc_nomer_shassi: str
    ctc_ptc_nomer_cusov: str

    nomer_dk: str
    data_TO: str

    c_ogr_or_not: str

    voditeli: List[PydanticVoditeliArm]

    OSAGO_start: str
    OSAGO_count_mouth: str

    strah_comp: str

    trans_num: str
    est_price_policy: str
    real_price_policy: str
    num_group_wa: str

    status_bot: str

    proxy: str
    pump: bool
    proxy_batut: str
    prepare_pump: bool

    reg_date_telephone: str
    telephone: str
    id_num_telephone: str
    telephone_service: str

    class Config:
        orm_mode = True

class PydanticOsagoAlfa(BaseModel):
    id: int

    type_osago: str

    login_parea: str
    password_parea: str

    email_login: str
    email_password: str

    surname: str
    name: str
    otchestvo: str
    birthday: str
    pass_seriya: str
    pass_number: str
    pass_vidach: str
    pass_address: str

    sobstv_yavl_strah: str
    sobstv_surname: str
    sobstv_name: str
    sobstv_otchestvo: str
    sobstv_birthday: str
    sobstv_pass_seriya: str
    sobstv_pass_number: str
    sobstv_pass_vidach: str
    sobstv_pass_address: str

    target: str
    category: str
    year: str
    powers: str
    auto_region: str
    auto_type: str
    brand_name: str
    brand: str
    brand_name_other: str
    model: str
    model_name_other: str
    model_name: str
    modification: str
    modification_name: str

    max_mass: str
    pricep: str

    count_pass_mest: str

    type_document: str

    ctc_ptc_seriya: str
    ctc_ptc_number: str
    ctc_ptc_vidach: str
    ctc_ptc_reg_znak: str
    ctc_ptc_vin: str
    ctc_ptc_nomer_shassi: str
    ctc_ptc_nomer_cusov: str

    nomer_dk: str
    data_TO: str

    c_ogr_or_not: str

    voditeli: List[PydanticVoditeliAlfa]

    OSAGO_start: str
    OSAGO_count_mouth: str

    strah_comp: str

    trans_num: str
    est_price_policy: str
    real_price_policy: str
    num_group_wa: str

    status_bot: str

    reg_date_telephone: str
    telephone: str
    id_num_telephone: str
    telephone_service: str

    url_pay: str

    class Config:
        orm_mode = True

class PydanticOsagoVsk(BaseModel):
    id: int

    session_cookies: str
    session_cookies_date: str
    session_id: str

    type_osago: str

    login_parea: str
    password_parea: str

    email_login: str
    email_password: str

    surname: str
    name: str
    otchestvo: str
    birthday: str
    pass_seriya: str
    pass_number: str
    pass_vidach: str
    city_strah: str
    street_strah: str
    building_strah: str
    house_strah: str
    apartment_strah: str
    postal_code_strah: str
    strah_type_document: str

    sobstv_yavl_strah: str
    sobstv_surname: str
    sobstv_name: str
    sobstv_otchestvo: str
    sobstv_birthday: str
    sobstv_pass_seriya: str
    sobstv_pass_number: str
    sobstv_pass_vidach: str
    city_sobstv: str
    street_sobstv: str
    building_sobstv: str
    house_sobstv: str
    apartment_sobstv: str
    postal_code_sobstv: str
    sobstv_type_document: str

    target: str
    category: str
    year: str
    powers: str
    mark: str
    model: str
    mark_name_other: str
    model_name_other: str
    mark_id: str
    model_id: str

    max_mass: str
    pricep: str
    count_pass_mest: str

    type_document: str

    ctc_ptc_seriya: str
    ctc_ptc_number: str
    ctc_ptc_vidach: str
    ctc_ptc_reg_znak: str
    ctc_ptc_vin: str
    ctc_ptc_nomer_shassi: str
    ctc_ptc_nomer_cusov: str

    nomer_dk: str
    data_TO: str

    c_ogr_or_not: str

    voditeli: List[PydanticVoditeliVsk]

    OSAGO_start: str
    OSAGO_count_mouth: str

    strah_comp: str

    trans_num: str
    est_price_policy: str
    real_price_policy: str
    num_group_wa: str

    status_bot: str

    reg_date_telephone: str
    telephone: str
    id_num_telephone: str
    telephone_service: str

    url_pay: str

    class Config:
        orm_mode = True