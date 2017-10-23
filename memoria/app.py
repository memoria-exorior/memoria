"""
Entrypoint for memoria service.
"""

import logging.config

from flask import Flask, Blueprint

from memoria.config import settings
from memoria.api.rest import ns as facts_namespace
from memoria.api.rest import api
from memoria.database import db

logging.config.fileConfig('logging.conf')
log = logging.getLogger(__name__)


def configure_app(flask_app):
    """
    Configure the application.

    :param: Flask app
    :return: Flask app
    """
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME

    flask_app.config['MONGOALCHEMY_SERVER'] = settings.MONGOALCHEMY_SERVER
    flask_app.config['MONGOALCHEMY_DATABASE'] = 'facts'

    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP


def create_app():
    """
    Creates the Flask application.

    :return: Flask app
    """
    app = Flask(__name__)
    configure_app(app)

    # configure api component
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(facts_namespace)
    app.register_blueprint(blueprint)

    # configure database component
    db.init_app(app)

    # add simple health-check endpoint
    @app.route("/health")
    def health():
        return "ok"

    return app


def main():
    """
    Embedded Flask HTTP server entrypoint function for memoria service.
    """
    flask_app = create_app()
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'
             .format(flask_app.config['SERVER_NAME']))
    flask_app.run(debug=settings.FLASK_DEBUG)


if __name__ == "__main__":
    main()
