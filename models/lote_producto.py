from app import db
from sqlalchemy import Enum

class Lote_Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String(60))
    estado = db.Column(Enum('Caducado', 'Bueno'))
    escogido = db.Column(db.Boolean, default=True)
    cantidad = db.Column(db.Integer)
    fecha_caducidad = db.Column(db.Date)
    bandera = db.Column(db.Boolean, default=False)
    id_lote = db.Column(db.Integer, db.ForeignKey('lote.id'))
    lote = db.relationship('Lote', backref=db.backref('lote_productos', lazy=True))
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id'))
    producto = db.relationship('Producto', backref=db.backref('lote_productos', lazy=True))

    def serialize(self):
        nombre_producto = ""
        if self.producto:
            nombre_producto = self.producto.nombre

        nombre_lote = ""
        if self.lote:
            nombre_lote = self.lote.fecha_produccion
        
        return  {
            'estado': self.estado,
            'escogido': self.escogido,
            'cantidad': self.cantidad,
            'producto': nombre_producto,
            'lote': nombre_lote,
            'fecha_caducidad': self.fecha_caducidad,
            'external_id':self.external_id,
            'bandera':self.bandera
        }
    
    def serialize2(self):
        producto_data = None
        if self.producto:
            producto_data = {
                'precio': self.producto.precio,
                'nombre':self.producto.nombre,
                'stock':self.producto.stock
            }

        nombre_lote = ""
        if self.lote:
            nombre_lote = self.lote.id
        
        return  {
            'estado': self.estado,
            'producto': producto_data,
            'lote': nombre_lote,
            'fecha_caducidad': self.fecha_caducidad,
        }