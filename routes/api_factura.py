from flask import Blueprint, jsonify, make_response, request
from controller.facturaControl import FacturaControl
from flask_expects_json import expects_json
from controller.authenticate import token_required
from controller.utiles.errores import Errors

api_factura = Blueprint('api_factura', __name__)
facturaC = FacturaControl()

schema_factura = {
    "type": "object",
    "properties": {
        "id_persona":{'type': 'string'},
    },
    "required": ["id_persona"],
}

schema_detalle_factura = {
    "type": "object",
    "properties": {
        "cantidad":{'type': 'number'},
        "id_factura":{'type': 'string'},
        "id_producto":{'type': 'string'},
    },
    "required": ["cantidad", "id_factura", "id_producto"],
}

@api_factura.route('/factura/save', methods=["POST"])
@token_required
@expects_json(schema_factura)
def create_factura():
    data = request.json
    factura_id = facturaC.guardarFactura (data)
    return make_response(
        jsonify({"msg":"OK", "code":200, "data": factura_id}),
        200,
    )

@api_factura.route('/detalle_factura/save', methods=["POST"])
@token_required
@expects_json(schema_detalle_factura)
def create_detalle_factura():
    data = request.json
    detalle_factura_id = facturaC.guardarDetalleFactura (data)
    if detalle_factura_id == -1:
        error_msg = Errors.error.get(str(-3), "Unknown error")
        return make_response(
            jsonify({"msg": "Error", "code": 401, "data": {"error": error_msg}}),
            401
        )
    elif detalle_factura_id == -2:
        error_msg = Errors.error.get(str(-10), "Unknown error")
        return make_response(
            jsonify({"msg": "Error", "code": 401, "data": {"error": error_msg}}),
            401
        )
    elif detalle_factura_id == -4:
        error_msg = Errors.error.get(str(-4), "Unknown error")
        return make_response(
            jsonify({"msg": "Error", "code": 401, "data": {"error": error_msg}}),
            401
        )
    else:
        return make_response(
            jsonify({"msg":"OK", "code":200, "data": detalle_factura_id}),
            200,
        )
    
@api_factura.route("/factura", methods=["GET"])
@token_required
def listLote_Producto():
    datos_factura = facturaC.listarFactura()
    
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos":([i.serialize() for i in datos_factura])}),
        200
    )

    
@api_factura.route("/detalle_factura", methods=["GET"])
@token_required
def listfactura_detalle():
    datos_facturadetalle = facturaC.listarDetalleFactura()
    
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos":([i.serialize() for i in datos_facturadetalle])}),
        200
    )
