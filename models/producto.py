from app import db
from sqlalchemy import Enum
from copy import deepcopy

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String(60))
    stock = db.Column(db.Integer)
    precio = db.Column(db.Float)
    nombre = db.Column(db.String(100))

    def get_copy(self):
        return deepcopy(self)

    def serialize(self):
        return  {
            'stock': self.stock,
            'precio': self.precio,
            'nombre': self.nombre,
            'external_id':self.external_id,
        }

    
    