import logging
logging.basicConfig(level='DEBUG')

from flask import Blueprint, render_template, request

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors.html', error_code=404), 404

@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors.html', error_code=403), 403

@errors.app_errorhandler(500)
def error_500(error):
    message =  error.description
    logging.debug(f' HA AH HA AH HA AH  {message}')
    return render_template('errors.html', error_code=500, message=message), 500

