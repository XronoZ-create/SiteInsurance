"""
Конфиг для Flask-а

"""

import os
basedir = os.path.abspath(os.path.dirname(__file__))

#Базовый класс настроек для всех конфигураций
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string' # секретный ключ для защиты. Устанавливается из переменной окружения или дефолт.
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # уведомления до и после внесения изменений в базу данных

    MARKET_STEAM_SERVER_IP = '188.120.249.110:5000'

    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    TESTING = False

    CELERY_BROKER_URL = 'amqp://'
    result_backend = 'amqp://'

    API_KEY = ""
    ADMIN_PASSWORD = ""

    token_dadata = ""

    @staticmethod
    def init_app(app):
        pass

#конфиги для разных баз данных.Продакшн, девелоп, тест. Разные базы данных.
class DevelopmentConfig(Config):
    DEBUG = True
    EMAIL_SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'email_db.sqlite')
    INSURANCE_SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'insurance_db.sqlite')

#Основной словарь, с которым мы будет работать
config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
