from models.lote import Lote
from app import db
import uuid, re
from datetime import datetime

class LoteControl:
    def guardarLote(self, data):
        lote = Lote()
        lote.fecha_produccion = data.get("fecha_produccion")
        lote.external_id = uuid.uuid4()
        fecha_objeto = datetime.strptime(lote.fecha_produccion, "%Y-%m-%d")
        # Formatea la fecha en el formato deseado "yyyymmdd"
        fecha_formateada = fecha_objeto.strftime("%Y%m%d")
        lote.num_lote = fecha_formateada
        db.session.add(lote)
        db.session.commit()
        return lote.id
        
    def listar(self):
        return Lote.query.all()
        

