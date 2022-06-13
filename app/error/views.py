from . import error
from flask import render_template, redirect, url_for
from flask_login import current_user

# @error.app_errorhandler(404)
# def page_not_found(e):
#     return render_template('pages-404.html'), 404
#
# @error.app_errorhandler(Exception)
# def page_error(e):
#     error = type(e).__name__
#     print(error)
#     return render_template('pages-500.html', error=error), 500