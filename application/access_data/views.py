from flask import Blueprint, jsonify

from application.nuts.nuts_services import nuts_service


def create_blueprint() -> Blueprint:
    blueprint = Blueprint(__name__.split('.')[-2], __name__)

    @blueprint.get('/get_access_token/<user_id>')
    def get_access_token(user_id):
        assert user_id is not None
        return jsonify(nuts_service.get_access_token(user_id))

    return blueprint
