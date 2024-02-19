from flask import render_template, Blueprint


def create_blueprint() -> Blueprint:
    blueprint = Blueprint(__name__.split('.')[-2], __name__)

    @blueprint.get('/')
    def index():
        return render_template('index.html')

    return blueprint
