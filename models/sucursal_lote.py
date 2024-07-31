from app import db

class Sucursal_Lote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String(60))
    id_lote_producto = db.Column(db.Integer, db.ForeignKey('lote__producto.id'))
    lote_producto = db.relationship('Lote_Producto', backref=db.backref('sucursal_lotes', lazy=True))
    id_sucursal = db.Column(db.Integer, db.ForeignKey('sucursal.id'))
    sucursal = db.relationship('Sucursal', backref=db.backref('sucursal_lotes', lazy=True))


    def serialize(self):
        nombre_producto = ""
        if self.lote_producto:
            nombre_producto = self.lote_producto.producto.nombre

        precio_producto = ""
        if self.lote_producto:
            precio_producto = self.lote_producto.producto.precio

        estado_producto = ""
        if self.lote_producto:
            estado_producto = self.lote_producto.estado

        return {
            'nombre': nombre_producto,
            'estado': estado_producto,
            'precio': precio_producto
        }
