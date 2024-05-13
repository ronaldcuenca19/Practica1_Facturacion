from app import db
from sqlalchemy import CheckConstraint

class Detalle_Factura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String(60))
    cantidad = db.Column(db.Integer, CheckConstraint('cantidad >= 1 AND cantidad<= 200'))
    total_producto = db.Column(db.Float)
    id_factura = db.Column(db.Integer, db.ForeignKey('factura.id'))
    factura = db.relationship('Factura', backref=db.backref('facturas', lazy=True))
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id'))
    producto = db.relationship('Producto', backref=db.backref('detalle_facturas', lazy=True))


    def serialize(self):
        nombre_producto = ""
        if self.producto:
            nombre_producto = self.producto.nombre

        nombre_factura = ""
        if self.factura:
            nombre_factura = self.factura.numero_factura

        return  {
            'cantidad': self.cantidad,
            'total_producto': self.total_producto,
            'external': self.external_id,
            'producto': nombre_producto,
            'factura':nombre_factura
        }