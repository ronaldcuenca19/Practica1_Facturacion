from app import db
from copy import deepcopy

class Persona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String(60))
    nombre = db.Column(db.String(100))
    apellido = db.Column(db.String(100))
    estado = db.Column(db.String(50))
    edad = db.Column(db.Integer)
    cedula = db.Column(db.Integer)
    foto = db.Column(db.String(100))
    # Relación uno a muchos con Censo_Persona
    #censos = db.relationship('Censo_Persona', backref='persona', lazy=True)
    id_rol = db.Column(db.Integer, db.ForeignKey('rol.id'))
    rol = db.relationship('Rol', backref=db.backref('personas', lazy=True))

    def get_copy(self):
        return deepcopy(self)
    
    def serialize(self):
        # Obtener el nombre del rol asociado
        nombre_rol = ""
        if self.rol:
            nombre_rol = self.rol.nombre
        
        return  {
            'nombre': self.nombre,
            'apellido': self.apellido,
            'edad': self.edad,
            'estado': self.estado,
            'cedula': self.cedula,
            'rol': nombre_rol,
            'foto':self.foto,
            'external_id':self.external_id,
        }