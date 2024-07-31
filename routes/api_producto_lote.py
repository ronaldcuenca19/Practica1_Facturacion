from flask import Blueprint, jsonify, make_response, request
from controller.loteControl import LoteControl
from controller.productoControl import ProductoControl
from controller.surcursalControl import SucursalControl
from flask_expects_json import expects_json
from controller.authenticate import token_required
from controller.utiles.errores import Errors
from werkzeug.utils import secure_filename
import os

def archivosPerm(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ProductoControl.ALLOWED_EXTENSIONS
    
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

api_producto_lote = Blueprint('api_producto_lote', __name__)
loteC = LoteControl()
productoC = ProductoControl()
sucursalC = SucursalControl()

schema_lote = {
    "type": "object",
    "properties": {
        "fecha_produccion": {'type': 'string', 'format': 'date-time'}, 
    },
    "required": ["fecha_produccion"],
}

schema_producto = {
    "type": "object",
    "properties": {
        "nombre": {'type': 'string'}, 
        "precio": {'type': 'number'}, 
    },
    "required": ["nombre", "precio"],
}

schema_sucursal = {
    "type": "object",
    "properties": {
        "nombre": {'type': 'string'}, 
        "longitud": {'type': 'string'}, 
        "latitud": {'type': 'string'}, 
    },
    "required": ["nombre", "longitud", "latitud"],
}

schema_lote_sucursal = {
    "type": "object",
    "properties": {
        "id_lote_producto": {'type': 'string'}, 
        "id_sucursal": {'type': 'string'}, 
    },
    "required": ["id_lote_producto", "id_sucursal"],
}


schema_lote_producto = {
    "type": "object",
    "properties": {
        "cantidad": {'type': 'integer'}, 
        "id_lote": {'type': 'string'}, 
        "id_producto": {'type': 'string'}, 
        "fecha_caducidad":{'type': 'string', 'format': 'date-time'}, 
    },
    "required": ["cantidad", "id_lote", "id_producto",'fecha_caducidad'],
}

schema_producto_foto = {
    "type": "object",
    "properties": {
        "external_id": {'type': 'string'}, 
    },
    "required": ["external_id"],
}

schema_producto_2 = {
    "type": "object",
    "properties": {
        "nombre": {'type': 'string'}, 
        "precio": {'type': 'number'},
        "external_id": {'type': 'string'}
    },
    "required": ["nombre", "precio", "external_id"],
}

@api_producto_lote.route('/lote/save', methods=["POST"])
@token_required
@expects_json(schema_lote)
def create_lote():
    data = request.json
    lote_id = loteC.guardarLote (data)
    return make_response(
        jsonify({"msg":"OK", "code":200, "data": lote_id}),
        200,
    )

    
@api_producto_lote.route('/producto/save', methods=["POST"])
@token_required
@expects_json(schema_producto)
def create_producto():
    data = request.json
    producto_id = productoC.guardarProducto (data)
    return make_response(
        jsonify({"msg":"OK", "code":200, "data": producto_id}),
        200,
    )

@api_producto_lote.route('/lote_sucursal/save', methods=["POST"])
@expects_json(schema_lote_sucursal)
def create_lote_sucursal():
    data = request.json
    lote_sucursal_id = sucursalC.guardarSucursal_Lote (data)
    return make_response(
        jsonify({"msg":"OK", "code":200, "data": lote_sucursal_id}),
        200,
    )

@api_producto_lote.route("/lote_sucursal", methods=["GET"])
def listLote_Sucursal():
    datos_lote_sucursal = sucursalC.listar2()
    
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos":([i.serialize() for i in datos_lote_sucursal])}),
        200
    )

@api_producto_lote.route('/sucursal/save', methods=["POST"])
@expects_json(schema_sucursal)
def create_sucursal():
    data = request.json
    sucursal_id = sucursalC.guardarSucursal (data)
    return make_response(
        jsonify({"msg":"OK", "code":200, "data": sucursal_id}),
        200,
    )


@api_producto_lote.route("/sucursal", methods=["GET"])
def listSucursal():
    datos_sucursal = sucursalC.listar()
    
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos":([i.serialize() for i in datos_sucursal])}),
        200
    )

@api_producto_lote.route('/foto/producto', methods=["POST"])
@token_required
def create_foto_producto():
    if 'file' not in request.files:
        return make_response(jsonify({"msg": "Sin parte del archivo para la petición"}), 400)

    file = request.files['file']

    if file.filename == '':
        return make_response(jsonify({"msg": "Ningún archivo para subir"}), 400)

    if file and archivosPerm(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join('static/product_gallery', filename)
        file.save(file_path)

        external_id = request.form.get('external')

        producto_id = productoC.guardarImage(external_id, filename)
        if producto_id:
            return make_response(
                jsonify({"msg": "OK", "code": 200, "data": producto_id}),
                200
            )
        else:
            return make_response(jsonify({"msg": "Producto no encontrado", "code": 404}), 404)

    return make_response(jsonify({"msg": "Archivo no permitido", "code": 400}), 400)
   
@api_producto_lote.route('/lote_producto/save', methods=["POST"])
@token_required
@expects_json(schema_lote_producto)
def create_lote_producto():
    data = request.json
    lote_producto_id = productoC.guardarLote_Producto(data)
    
    if lote_producto_id == -2:
        error_msg = Errors.error.get(str(-8), "Unknown error")
        return make_response(
            jsonify({"msg": "Error", "code": 400, "data": {"error": error_msg}}),
            401
        )
    elif lote_producto_id == -1:
        error_msg = Errors.error.get(str(-3), "Unknown error")
        return make_response(
            jsonify({"msg": "Error", "code": 401, "data": {"error": error_msg}}),
            401
        )
    
    elif lote_producto_id == -3:
        error_msg = Errors.error.get(str(-8), "Unknown error")
        return make_response(
            jsonify({"msg": "Error", "code": 401, "data": {"error": error_msg}}),
            401
        )
    
    elif lote_producto_id == -4:
        error_msg = Errors.error.get(str(-4), "Unknown error")
        return make_response(
            jsonify({"msg": "Error", "code": 401, "data": {"error": error_msg}}),
            401
        )

    else:
        return make_response(
            jsonify({"msg": "OK", "code": 200, "data": lote_producto_id}),
            200
        )


@api_producto_lote.route('/producto/update', methods=["POST"])
@token_required
@expects_json(schema_producto_2)
def update_producto():
    data = request.json
    person_id = productoC.editarProducto (data)
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


@api_producto_lote.route("/lote", methods=["GET"])
@token_required
def listLote():
    datos_lote = loteC.listar()
    
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos":([i.serialize() for i in datos_lote])}),
        200
    )

@api_producto_lote.route("/producto", methods=["GET"])
@token_required
def listProducto():
    datos_producto = productoC.listar()
    
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos":([i.serialize() for i in datos_producto])}),
        200
    )


@api_producto_lote.route("/sucursal/<external>",  methods=["GET"])
def list_sucursal_prod(external):
    datos_prod_sucursal = sucursalC.listarProd_Sucursal(external)
    if datos_prod_sucursal != -6:
      return make_response(
        jsonify({"msg": "OK", "code": 200, "datos":([i.serialize() for i in datos_prod_sucursal])}),
        200
    )
    else:
      return make_response(
        jsonify({"msg":"Error", "code":400, "data": {"error": Errors.error[str(-3)]}}),
        400,
        )

@api_producto_lote.route("/sucursal/bajar/<external>",  methods=["GET"])
def bajar_lote_prod(external):
    datos_prod_sucursal = productoC.listarLote_Producto_Escogido(external)
    if datos_prod_sucursal != -6:
      return make_response(
        jsonify({"msg": "OK", "code": 200}),
        200
    )
    else:
      return make_response(
        jsonify({"msg":"Error", "code":400, "data": {"error": Errors.error[str(-3)]}}),
        400,
        )


@api_producto_lote.route("/producto/<external>",  methods=["GET"])
def list_obtener(external):
    # Aquí se obtiene el parámetro 'external' de la URL y se pasa a la función 'listarPersona'
    datos_persona = productoC.obtenerProducto(external)
    
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
    

@api_producto_lote.route("/lote_producto", methods=["GET"])
@token_required
def listLote_Producto():
    datos_lote = productoC.listarLote_Producto()
    
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos":([i.serialize() for i in datos_lote])}),
        200
    )

@api_producto_lote.route("/producto/fresco", methods=["GET"])
def listProductoBueno():
    datos_productoBueno = productoC.listarLote_Producto_Normal()
    
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos":([i.serialize2() for i in datos_productoBueno])}),
        200
    )

@api_producto_lote.route("/producto/apunto", methods=["GET"])
def listProductoAPunto():
    datos_productoAPunto = productoC.listarLote_Producto_Apunto()
    
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos":([i.serialize2() for i in datos_productoAPunto])}),
        200
    )

@api_producto_lote.route("/producto/caducado", methods=["GET"])
def listProductoCaducado():
    datos_productoCaducado = productoC.listarLote_Producto_Caducado()
    
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos":([i.serialize2() for i in datos_productoCaducado])}),
        200
    )

@api_producto_lote.route("/lote_producto/escogido", methods=["GET"])
def listProductoEscodigido():
    datos_productoEscogido = productoC.listarLote_Producto_Escodigo()
    
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos":([i.serialize() for i in datos_productoEscogido])}),
        200
    )

@api_producto_lote.route("/lote_producto/cambiarEstado", methods=["GET"])
@token_required
def cambiarEstado():
    # Aquí se obtiene el parámetro 'external' de la URL y se pasa a la función 'listarPersona'
    productoC.bajarStock()
    
    # Se verifica si se encontró una persona con el external_id dado
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos":()}),
        200
    )

