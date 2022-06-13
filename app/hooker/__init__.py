from flask import Blueprint

hooker = Blueprint('hooker', __name__)

from . import views