from flask import Blueprint, request, redirect, jsonify

from application.nuts.nuts_services import nuts_service


def create_blueprint() -> Blueprint:
    blueprint = Blueprint(__name__.split('.')[-2], __name__)

    @blueprint.get('/authenticate_with_ozo/<user_id>')
    def authenticate_with_ozo(user_id):
        base_url = f'{request.scheme}://{request.host}'
        redirect_uri = f'{base_url}/'
        return redirect(nuts_service.initiate_oid4vci_issue(user_id, redirect_uri))


    return blueprint
