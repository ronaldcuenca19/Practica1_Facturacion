from models.factura import Factura
from models.detalle_factura import Detalle_Factura
from models.persona import Persona
from models.producto import Producto
from controller.productoControl import ProductoControl
from app import db
import uuid
from datetime import datetime, timedelta

productoC = ProductoControl()

class FacturaControl:
    def guardarFactura(self, data):
        cliente2 = Persona.query.filter_by(external_id=data.get("id_persona")).first()
        factura = Factura()
        factura.fecha = datetime.now().date()
        factura.total = 0
        factura.numero_factura = FacturaControl.generar_numero_factura()
        factura.id_persona = cliente2.id
        factura.external_id = uuid.uuid4()
        db.session.add(factura)
        db.session.commit()
        return factura.id
    
    def guardarDetalleFactura(self, data):
        productoC.bajarStock()
        factura2 = Factura.query.filter_by(external_id=data.get("id_factura")).first()
        producto2 = Producto.query.filter_by(external_id=data.get("id_producto")).first()
        if producto2 and factura2:
            detalle_factura = Detalle_Factura()
            detalle_factura.cantidad = data.get("cantidad")
            detalle_factura.total_producto = (data.get("cantidad")*producto2.precio)
            detalle_factura.id_factura = factura2.id
            detalle_factura.id_producto = producto2.id
            detalle_factura.external_id = uuid.uuid4()
            productos_existentes = Detalle_Factura.query.filter_by(id_factura=factura2.id).all()
            for producto_existente in productos_existentes:
                if producto_existente.id_producto == producto2.id:
                    db.session.rollback()
                    return -4
            if producto2.stock >= data.get("cantidad"):
                producto2.stock -= data.get("cantidad")
                db.session.merge(producto2)
                db.session.add(detalle_factura)
                db.session.commit()
                self.actualizarTotalFactura(factura2.id)
            else:
                return -2
        else:
            return -1
        return detalle_factura.id
    
    def generar_numero_factura():
        ultima_factura = Factura.query.order_by(Factura.id.desc()).first()
        if ultima_factura and ultima_factura.numero_factura.isdigit():
            nuevo_numero = str(int(ultima_factura.numero_factura) + 1).zfill(7)
        else:
            nuevo_numero = '0000001'
        return nuevo_numero

    
    def modificar_stock(cantidad, data):
        producto2 = Factura.query.filter_by(external_id=data.get("id_producto")).first()
        if producto2.stock >= cantidad:
            producto2.stock -= cantidad
            db.session.merge(producto2)
            db.session.commit()
        else:
            -3

    def listarFactura(self):
        return Factura.query.all()
    
    def listarDetalleFactura(self):
        return Detalle_Factura.query.all() 
    
    def listarDetalleEspecifica(self, external):
        factura2 = Factura().query.filter_by(external_id = external).first()
        return Detalle_Factura.query.filter_by(id_factura = factura2.id).all() 
    
    def actualizarTotalFactura(self, id_factura):
    # Obtener la factura a actualizar
        factura = Factura.query.filter_by(id=id_factura).first()
        
        # Verificar si la factura existe
        if factura:
            # Obtener todos los detalles de factura asociados a esta factura
            detalles_factura = Detalle_Factura.query.filter_by(id_factura=id_factura).all()
            
            # Inicializar el total de la factura
            total_factura = 0
            
            for detalle in detalles_factura:
                total_factura += detalle.total_producto
            
            factura.total = total_factura
            
            db.session.merge(factura)
            db.session.commit()
            
            return total_factura
        else:
            return "La factura con el ID especificado no existe."


    
        
