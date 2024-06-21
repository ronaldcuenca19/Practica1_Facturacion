from app import db
from sqlalchemy import Enum, CheckConstraint

class Factura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String(60))
    fecha = db.Column(db.Date)
    total = db.Column(db.Float)
    numero_factura = db.Column(db.String(150))
    id_persona = db.Column(db.Integer, db.ForeignKey('persona.id'))
    persona = db.relationship('Persona', backref=db.backref('facturas', lazy=True))

    def serialize(self):
        nombre_cliente = ""
        if self.persona:
            nombre_cliente = self.persona.nombre + ' ' + self.persona.apellido

        nombre_cedula = ""
        if self.persona:
            nombre_cedula = self.persona.cedula
        return  {
            'fecha': self.fecha,
            'total': self.total,
            'numero_factura': self.numero_factura,
            'external': self.external_id,
            'cliente': nombre_cliente,
            'cedula': nombre_cedula
        }