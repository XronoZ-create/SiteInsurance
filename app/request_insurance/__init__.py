from flask import Blueprint

request_insurance = Blueprint('request_insurance', __name__)

from . import views