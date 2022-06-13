from flask import Blueprint

arm = Blueprint('arm', __name__)

from . import views