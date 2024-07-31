from models.producto import Producto
from models.lote_producto import Lote_Producto
from models.lote import Lote
from app import db
import uuid
from datetime import datetime, timedelta
from flask import current_app, request
from werkzeug.utils import secure_filename
import os

class ProductoControl:
    def archivosPerm(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ProductoControl.ALLOWED_EXTENSIONS
    
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    
    def guardarImage(self, external_id, filename):
        producto = Producto.query.filter_by(external_id=external_id).first()
        if producto:
            producto.foto = filename
            db.session.commit()
            return producto.id
        else:
            return None

    def guardarProducto(self, data):
        producto = Producto()
        producto.stock = 0
        producto.precio = data.get("precio")
        producto.nombre = data.get("nombre")
        producto.foto = "producto.png"
        producto.external_id = uuid.uuid4()
        db.session.add(producto)
        db.session.commit()
        return producto.id
    
    def guardarLote_Producto(self, data):
        producto2 = Producto.query.filter_by(external_id=data.get("id_producto")).first()
        lote2 = Lote.query.filter_by(external_id=data.get("id_lote")).first()
        if producto2 and lote2:
            lote_producto = Lote_Producto()
            lote_producto.cantidad = data.get("cantidad")
            lote_producto.external_id = uuid.uuid4()
            lote_producto.fecha_caducidad = data.get("fecha_caducidad")
            lote_producto.id_lote = lote2.id
            lote_producto.id_producto = producto2.id
            #////////////////////////////////////////////////////////////////////////////
            fecha_produccion_str = lote2.fecha_produccion.strftime("%Y-%m-%d")
            #/////////////////////////////////////////////////////////////////////////////
            lote_producto.estado = 'Bueno'
            if not ProductoControl.fechaCorrecta(fecha_produccion_str, lote_producto.fecha_caducidad):
                return -3
            
            productos_existentes = Lote_Producto.query.filter_by(id_lote=lote2.id).all()
            for producto_existente in productos_existentes:
                if producto_existente.id_producto == producto2.id:
                    db.session.rollback()
                    return -4

            if lote_producto.estado == "Caducado" or lote_producto.estado == "Bueno":
                db.session.add(lote_producto)
                db.session.commit()
                external = data.get("id_producto")
                external2 = data.get("id_lote")
                self.modificarStock(external, external2)
            else:
                return -2
        else:
            return -1
        return lote_producto.id
    
    def fechaCorrecta(fechaIn, fechaFin):
        fecha_inicio = datetime.strptime(fechaIn, '%Y-%m-%d')
        fecha_fin = datetime.strptime(fechaFin, '%Y-%m-%d')
        
        # Restar la fecha de inicio de la fecha de fin
        diferencia = fecha_fin - fecha_inicio
        
        if diferencia.days < 0:
            return False
        else:
            return True
    
    def listar(self):
        return Producto.query.all()
    
    def listarLote_Producto(self):
        return Lote_Producto.query.all()

        
    def modificarStock(self, external, external2):
        productoAUx = Producto.get_copy
        producto2 = Producto.query.filter_by(external_id=external).first()
        lote2 = Lote.query.filter_by(external_id=external2).first()
        productoAUx = producto2
        if productoAUx is None:
            print('El censador especificado no existe.')
            return None
        else:
            productos_stock = Lote_Producto.query.filter(Lote_Producto.id_lote == lote2.id, Lote_Producto.id_producto == producto2.id).first()
            productoAUx.stock += productos_stock.cantidad
            db.session.merge(productoAUx)
            db.session.commit()

    def bajarStock(self):
        self.estado_producto()
    # Obtener todos los lotes de productos caducados que aún no han restado su cantidad al stock
        lotes_caducados_no_restados = Lote_Producto.query.filter_by(estado='Caducado', bandera=False).all()
        
        cantidad_por_producto = {}

        # Calcular la cantidad total por producto a restar del stock
        for lote_producto in lotes_caducados_no_restados:
            id_producto = lote_producto.id_producto
            cantidad = lote_producto.cantidad

            if id_producto in cantidad_por_producto:
                cantidad_por_producto[id_producto] += cantidad
            else:
                cantidad_por_producto[id_producto] = cantidad

            # Marcar el lote como restado del stock para evitar restarlo nuevamente
            lote_producto.bandera = True
            db.session.merge(lote_producto)

        # Restar la cantidad total por producto del stock
        for id_producto, cantidad_total in cantidad_por_producto.items():
            producto = Producto.query.filter_by(id=id_producto).first()

            if producto:
                producto.stock -= cantidad_total
                db.session.merge(producto)

        db.session.commit()
        return lotes_caducados_no_restados

    def estado_producto(self):
        fecha_actual = datetime.now().date()
        lote_productos = Lote_Producto.query.all()

        for lote_producto in lote_productos:
            diferencia = lote_producto.fecha_caducidad - fecha_actual

            if diferencia <= timedelta(days=5):
                lote_producto.estado = 'Caducado'
                db.session.merge(lote_producto)
                db.session.commit()
        return lote_productos
    
    def listarLote_Producto_Normal(self):
        return Lote_Producto.query.filter_by(estado='Bueno').all()
    
    def listarLote_Producto_Escodigo(self):
        return Lote_Producto.query.filter_by(escogido=True).all()
    
    def listarLote_Producto_Apunto(self):
        fecha_actual = datetime.now().date()
        fecha_limite_superior = fecha_actual + timedelta(days=5)
        fecha_limite_inferior = fecha_actual + timedelta(days=1)  # Excluye la fecha actual

        return Lote_Producto.query.filter(Lote_Producto.fecha_caducidad > fecha_limite_inferior,
                                           Lote_Producto.fecha_caducidad <= fecha_limite_superior).all()
    
    def listarLote_Producto_Caducado(self):
        return Lote_Producto.query.filter_by(estado='Caducado').all()
    

    def editarProducto(self, data):
        censAUx = Producto.get_copy 
        censador2 = Producto.query.filter_by(external_id=data.get("external_id")).first()
        censAUx = censador2
        censAUx.nombre = data.get("nombre")
        censAUx.precio = data.get("precio")
        db.session.merge(censAUx)
        db.session.commit()
        return censAUx.id
    
    def obtenerProducto(self, external):
        return Producto.query.filter_by(external_id = external).first()



