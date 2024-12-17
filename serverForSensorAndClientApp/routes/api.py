from flask import Blueprint, jsonify
from flask import Flask, request

from service.service import handle_data_from_pico, handle_data_from_ui

api=Blueprint('api', __name__)


@api.route('/data-from-pico', methods=["POST"])
def handle_data_from_pico_endpoint():
    print("request from pico")
    pico_request = request.json
    gate = pico_request.get("data")

    result = handle_data_from_pico(gate)
    if result.__eq__("NOK"):
        return (jsonify({"result": result})), 500
    return jsonify({"result": result})

@api.route('/data-from-ui', methods=['POST'])
def handle_data_from_ui_endpoint():
    print("request from ui")
    ui_request = request.json
    user_id = ui_request.get("userId")
    session = ui_request.get("session")
    result = handle_data_from_ui(user_id, session)
    if result.__eq__("NOK"):
        return (jsonify({"result": result})), 500
    return jsonify({"result": result})