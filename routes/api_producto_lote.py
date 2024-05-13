from flask import Blueprint, jsonify, make_response, request
from controller.loteControl import LoteControl
from controller.productoControl import ProductoControl
from flask_expects_json import expects_json
from controller.authenticate import token_required
from controller.utiles.errores import Errors

api_producto_lote = Blueprint('api_producto_lote', __name__)
loteC = LoteControl()
productoC = ProductoControl()

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
   
@api_producto_lote.route('/lote_producto/save', methods=["POST"])
@token_required
@expects_json(schema_lote_producto)
def create_lote_producto():
    data = request.json
    lote_producto_id = productoC.guardarLote_Producto(data)
    
    if lote_producto_id == -2:
        error_msg = Errors.error.get(str(-8), "Unknown error")
        return make_response(
            jsonify({"msg": "Error", "code": 401, "data": {"error": error_msg}}),
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


@api_producto_lote.route("/lote", methods=["GET"])
def listLote():
    datos_lote = loteC.listar()
    
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos":([i.serialize() for i in datos_lote])}),
        200
    )

@api_producto_lote.route("/producto", methods=["GET"])
def listProducto():
    datos_producto = productoC.listar()
    
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos":([i.serialize() for i in datos_producto])}),
        200
    )

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

