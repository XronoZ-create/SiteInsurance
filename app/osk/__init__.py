from flask import Blueprint

osk = Blueprint('osk', __name__)

from . import views