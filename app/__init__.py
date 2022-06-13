from flask import Flask

from flask_login import LoginManager
from config import config
from flask_socketio import SocketIO


login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

socketio = SocketIO()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    #серия init_app подключения приложений
    login_manager.init_app(app)

    #серия подключения макетов

    from .main import main as check_blueprint
    app.register_blueprint(check_blueprint)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    from .error import error as error_blueprint
    app.register_blueprint(error_blueprint, url_prefix='/errors')
    from .osk import osk as osk_blueprint
    app.register_blueprint(osk_blueprint, url_prefix='/osk')
    from .request_insurance import request_insurance as request_insurance_blueprint
    app.register_blueprint(request_insurance_blueprint, url_prefix='/request_insurance')
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    from .hooker import hooker as hooker_blueprint
    app.register_blueprint(hooker_blueprint, url_prefix='/hooker')
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    from .ugsk import ugsk as ugsk_blueprint
    app.register_blueprint(ugsk_blueprint, url_prefix='/ugsk')
    from .vek21 import vek21 as vek21_blueprint
    app.register_blueprint(vek21_blueprint, url_prefix='/vek21')
    from .statistic import statistic as statistic_blueprint
    app.register_blueprint(statistic_blueprint, url_prefix='/statistic')
    from .arm import arm as arm_blueprint
    app.register_blueprint(arm_blueprint, url_prefix='/arm')
    from .alfa import alfa as alfa_blueprint
    app.register_blueprint(alfa_blueprint, url_prefix='/alfa')
    from .vsk import vsk as vsk_blueprint
    app.register_blueprint(vsk_blueprint, url_prefix='/vsk')


    socketio.init_app(app, async_mode='threading')

    return app
