from flask import Flask
from flask_behind_proxy import FlaskBehindProxy

from application import oid4vci, access_data, index


def register_blueprints(app):
    app.register_blueprint(oid4vci.views.create_blueprint())
    app.register_blueprint(access_data.views.create_blueprint())
    app.register_blueprint(index.views.create_blueprint())


def create_app(config=None) -> Flask:
    app = Flask(__name__, instance_relative_config=True,
                static_url_path='',
                static_folder='html/static',
                template_folder='html/templates')
    FlaskBehindProxy(app)
    if config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py')
    else:
        # load the test config if passed in
        app.config.from_mapping(config)

    register_blueprints(app)
    return app
