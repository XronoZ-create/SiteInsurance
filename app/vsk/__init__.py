from flask import Blueprint

vsk = Blueprint('vsk', __name__)

from . import views