from app import db

class Rol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    descripcion = db.Column(db.String(100))
    estado = db.Column(db.Boolean, default=True)
    external_id = db.Column(db.String(60))

    def serialize(self):
        return {
            'id' : self.id,
            'nombre': self.nombre,
            'descripcion':self.descripcion,
            'external_id':self.external_id,
            'estado':self.estado
        }

""" HOST Docker LOCAl """