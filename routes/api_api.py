from flask import Blueprint, jsonify, make_response, request
from controller.personaControl import PersonaControl
from flask_expects_json import expects_json
from controller.authenticate import token_required
from controller.utiles.errores import Errors

api_api = Blueprint('api_api', __name__)
personaC = PersonaControl()

schema = {
    'type': 'object',
    'properties': {
        'nombres': {'type': 'string'},
        'apellidos': {'type': 'string'},
        'edad': {'type': 'string'},
        'correo': {'type': 'string'},
        'clave': {'type': 'string'},
        'cedula':{'type': 'string'},
        'estado': {'type': 'string'},
    },
    'required': ['nombres', 'apellidos', 'edad', 'correo', 'clave', 'estado', 'cedula']
}

schema_cliente = {
    'type': 'object',
    'properties': {
        'nombres': {'type': 'string'},
        'apellidos': {'type': 'string'},
        'edad': {'type': 'string'},
        'cedula':{'type': 'string'},
        'estado': {'type': 'string'},
    },
    'required': ['nombres', 'apellidos', 'edad', 'cedula','estado']
}

schema_session = {
    "type": "object",
    "properties": {
        "correo": {"type": "string"},
        "clave": {"type": "string"},
    },
    "required": ["correo", "clave"],
}

@api_api.route("/login", methods=["POST"])
@expects_json(schema_session)
def session():
    data = request.json
    id = personaC.inicio_sesion(data)
    if (type(id)) == int:
        return make_response(
            jsonify(
                {"msg": "ERROR", "code": 400, "data": {"error": Errors.error[str(id)]}}
            ),
            400,
        )
    else:
        return make_response(
            jsonify({"msg": "OK", "code": 200, "data": {"tag": id}}), 200
        )

@api_api.route('/persona/save/admin', methods=["POST"])
@expects_json(schema)
def create():
    data = request.json
    person_id = personaC.guardarFacturador (data)
    if person_id != -8:
        return make_response(
            jsonify({"msg":"OK", "code":200, "data": person_id}),
            200,
        )
    else:
        return make_response(
            jsonify(
                {"msg":"Error", "code":401, "data": {"error": Errors.error[str(-8)]}}
            ),
            401,
        )

@api_api.route('/persona/save/cliente', methods=["POST"])
@token_required
@expects_json(schema_cliente)
def create_cliente():
    data = request.json
    person_id = personaC.guardarCliente (data)
    if person_id != -8:
        return make_response(
            jsonify({"msg":"OK", "code":200, "data": person_id}),
            200,
        )
    else:
        return make_response(
            jsonify(
                {"msg":"Error", "code":401, "data": {"error": Errors.error[str(-8)]}}
            ),
            401,
        )
    
@api_api.route("/persona", methods=["GET"])
@token_required
def list():
    # Aquí se obtiene el parámetro 'external' de la URL y se pasa a la función 'listarPersona'
    datos_persona = personaC.listar()
    
    # Se verifica si se encontró una persona con el external_id dado
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos":([i.serialize() for i in datos_persona])}),
        200
    )
