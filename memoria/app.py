"""
Entrypoint for memoria service.
"""

import logging.config

from flask import Flask, Blueprint

from memoria.config import settings
from memoria.api.rest import ns as facts_namespace
from memoria.api.rest import api
from memoria.database import db


app = Flask(__name__)
logging.config.fileConfig('logging.conf')
log = logging.getLogger(__name__)


def configure_app(flask_app):
    """
    Configure the application.
    """
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME

    flask_app.config['MONGOALCHEMY_DATABASE_URI'] = settings.MONGOALCHEMY_DATABASE_URI
    flask_app.config['MONGOALCHEMY_DATABASE'] = 'facts'

    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP


def initialise_app(flask_app):
    """
    Initalises the application.
    """
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(facts_namespace)
    flask_app.register_blueprint(blueprint)

    db.init_app(flask_app)


def main():
    """
    Entrypoint function for memoria service.
    """
    initialise_app(app)
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug=settings.FLASK_DEBUG)


if __name__ == "__main__":
    main()
