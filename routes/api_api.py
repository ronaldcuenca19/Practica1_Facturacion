from flask import Blueprint, jsonify, make_response, request
from controller.personaControl import PersonaControl
from flask_expects_json import expects_json
from controller.authenticate import token_required
from controller.utiles.errores import Errors
from werkzeug.utils import secure_filename
import os

def archivosPerm(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in PersonaControl.ALLOWED_EXTENSIONS
    
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

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

schema_usuario_foto = {
    "type": "object",
    "properties": {
        "external_id": {'type': 'string'}, 
    },
    "required": ["external_id"],
}

schema_cliente_2 = {
    'type': 'object',
    'properties': {
        'nombres': {'type': 'string'},
        'apellidos': {'type': 'string'},
        'edad': {'type': 'string'},
        'cedula':{'type': 'string'},
        'external_id' :{'type':'string'}
    },
    'required': ['nombres', 'apellidos', 'edad', 'cedula', 'external_id']
}

@api_api.route("/login", methods=["POST"])
@expects_json(schema_session)
def session():
    data = request.json
    id = personaC.inicio_sesion(data)
    if id != -6:
        return make_response(
                jsonify({"msg": "OK", "code": 200, "data": {"tag": id}}), 200
            )
    else:
        return make_response(
            jsonify(
                {"msg": "ERROR", "code": 400, "data": {"error": Errors.error[str(id)]}}
            ),
            400,
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
    
@api_api.route('/persona/update/cliente', methods=["POST"])
@expects_json(schema_cliente_2)
def update_cliente():
    data = request.json
    person_id = personaC.editarCliente (data)
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

@api_api.route('/usuario/foto', methods=["POST"])
@token_required
def create_foto_producto():
    if 'file' not in request.files:
        return make_response(jsonify({"msg": "Sin parte del archivo para la petición"}), 400)

    file = request.files['file']

    if file.filename == '':
        return make_response(jsonify({"msg": "Ningún archivo para subir"}), 400)

    if file and archivosPerm(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join('static/images_gallery', filename)
        file.save(file_path)

        # Obtén el external_id del formulario
        external_id = request.form.get('external')

        # Guarda la imagen y actualiza el producto
        producto_id = personaC.guardarImage(external_id, filename)
        if producto_id:
            return make_response(
                jsonify({"msg": "OK", "code": 200, "data": producto_id}),
                200
            )
        else:
            return make_response(jsonify({"msg": "Producto no encontrado", "code": 404}), 404)

    return make_response(jsonify({"msg": "Archivo no permitido", "code": 400}), 400)

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

@api_api.route("/persona/<external>",  methods=["GET"])
def list_obtener(external):
    # Aquí se obtiene el parámetro 'external' de la URL y se pasa a la función 'listarPersona'
    datos_persona = personaC.obtenerCliente(external)
    
    # Se verifica si se encontró una persona con el external_id dado
    if datos_persona:
        # Si se encuentra la persona, se serializan los datos y se incluyen en la respuesta
        serialized_data = datos_persona.serialize()
        response_data = {
            "msg": "OK",
            "code": 200,
            "datos": serialized_data
        }
        # Se devuelve la respuesta en formato JSON con el código de estado HTTP 200
        return make_response(jsonify(response_data), 200)
    else:
        # Si no se encuentra la persona, se devuelve un mensaje de error con el código de estado HTTP 404
        return make_response(jsonify({"error": "No se encontró la persona"}), 404)
    

@api_api.route("/persona/cliente", methods=["GET"])
@token_required
def listClient():
    # Aquí se obtiene el parámetro 'external' de la URL y se pasa a la función 'listarPersona'
    datos_persona = personaC.listarCliente()
    
    # Se verifica si se encontró una persona con el external_id dado
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos":([i.serialize() for i in datos_persona])}),
        200
    )
