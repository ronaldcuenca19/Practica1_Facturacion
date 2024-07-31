from models.lote_producto import Lote_Producto
from models.sucursal import Sucursal
from models.sucursal_lote import Sucursal_Lote
from app import db
import uuid, re
from datetime import datetime

class SucursalControl:
    def guardarSucursal(self, data):
        surcursal = Sucursal()
        surcursal.nombre = data.get("nombre")
        surcursal.external_id = uuid.uuid4()
        surcursal.latitud = data.get("latitud")
        surcursal.longitud = data.get("longitud")
        db.session.add(surcursal)
        db.session.commit()
        return surcursal.id
    
    def guardarSucursal_Lote(self, data):
        lote_producto2 = Lote_Producto.query.filter_by(external_id=data.get("id_lote_producto")).first()
        sucursal2 = Sucursal.query.filter_by(external_id=data.get("id_sucursal")).first()
        surcursal_lote = Sucursal_Lote()
        surcursal_lote.external_id = uuid.uuid4()
        surcursal_lote.id_lote_producto=lote_producto2.id
        surcursal_lote.id_sucursal=sucursal2.id
        db.session.add(surcursal_lote)
        db.session.commit()
        SucursalControl.listarLote_Producto_Escogido(self, data.get("id_lote_producto"))
        return surcursal_lote.id

    def listarLote_Producto_Escogido(self, external):
        lote_producto3 = Lote_Producto()
        lote_producto2 = Lote_Producto.query.filter_by(external_id=external).first()
        lote_producto3 = lote_producto2
        if lote_producto3 is None:
            return -6
        else:
            lote_producto3.escogido = False
            db.session.merge(lote_producto3)
            db.session.commit()
            return lote_producto3.id

    def listarProd_Sucursal(self, external):
        sucursal2 = Sucursal.query.filter_by(external_id=external).first()
        if sucursal2 is None:
            return -6
        else:
            id_suc = sucursal2.id
            auxBusc = Sucursal_Lote.query.filter_by(id_sucursal=id_suc).all()
            return auxBusc


    def listar2(self):
        return Sucursal_Lote.query.all()
        
    def listar(self):
        return Sucursal.query.all()
        