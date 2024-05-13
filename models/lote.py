from app import db

class Lote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String(60))
    fecha_produccion = db.Column(db.Date)
    num_lote = db.Column(db.String(100))


    def serialize(self):
        return  {
            'fecha_produccion': self.fecha_produccion,
            'num_lote': self.num_lote,
            'external_id':self.external_id,
        }