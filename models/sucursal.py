from app import db

class Sucursal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    external_id = db.Column(db.String(60))
    latitud = db.Column(db.String(120))
    longitud = db.Column(db.String(120))


    def serialize(self):
        return {
            'nombre': self.nombre,
            'latitud': self.latitud,
            'longitud': self.longitud,
            'external_id': self.external_id,
        }
