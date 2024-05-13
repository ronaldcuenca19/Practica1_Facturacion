from models.lote_producto import Lote_Producto
from models.lote import Lote
from models.persona import Persona
from models.rol import Rol
from models.cuenta import Cuenta
from models.factura import Factura
from models.detalle_factura import Detalle_Factura
from models.producto import Producto
from app import db
from sqlalchemy.exc import IntegrityError
import re
import uuid
import jwt
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from controller.utiles.errores import Errors

class PersonaControl:

    def inicio_sesion(self, data):
        accountA = Cuenta.query.filter_by(correo=data["correo"]).first()
        if accountA:
            #decrypt password
            if check_password_hash(accountA.clave, data["clave"]):
                expire_time = datetime.now() + timedelta(minutes=90)
                token_payload = {
                    "external_id": accountA.external_id,
                    "expire": expire_time.strftime("%Y-%m-%d %H:%M:%S") 
                }
                print('-------------', token_payload)
                token = jwt.encode(
                    token_payload,
                    key=current_app.config["SECRET_KEY"],
                    algorithm="HS512"
                )    
                person = accountA.getPerson(accountA.id_persona)
                user_info = {
                    "token": token,
                    "user": person.apellido + " " + person.nombre
                }
                return user_info
            else:
                -6
        else:
            return -6
        
    def guardarFacturador(self, data):
        roles2 = Rol.query.filter_by(nombre=("Facturador")).first()
        contraseña_sin_hashear = data.get("clave")
        contraseña_hasheada = generate_password_hash(contraseña_sin_hashear)
        print('caqui1', roles2.nombre)
        persona = Persona()
        persona.apellido = data.get("apellidos")
        persona.nombre = data.get("nombres")
        persona.edad = data.get("edad")
        persona.external_id = uuid.uuid4()
        persona.estado = data.get("estado")
        persona.id_rol = roles2.id
        cuenta = Cuenta()
        cuenta.correo = data.get("correo")
        cuenta.clave = contraseña_hasheada
        cuenta.external_id = uuid.uuid4()
        persona.cuenta = cuenta

        if not PersonaControl.validar_correo(cuenta.correo):
            db.session.rollback()
            return None

        cuentas_existentes = Cuenta.query.all()
        for cuenta_existente in cuentas_existentes:
            if cuenta_existente.correo == cuenta.correo:
                db.session.rollback()
                return None

        try:
            db.session.add(persona)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()  
            return -8

        return persona.id

    def guardarCliente(self, data):
        roles2 = Rol.query.filter_by(nombre=("Cliente")).first()
        persona = Persona()
        persona.apellido = data.get("apellidos")
        persona.nombre = data.get("nombres")
        persona.edad = data.get("edad")
        persona.external_id = uuid.uuid4()
        persona.estado = data.get("estado")
        persona.cedula = data.get("cedula")
        persona.id_rol = roles2.id
        if not PersonaControl.validar_cedula(persona.cedula):
            db.session.rollback()
            return -8
        db.session.add(persona)
        db.session.commit()
        return persona.id



    def validar_correo(correo):
        patron = r"^[a-zA-Z0-9\.\-]+@[a-zA-Z0-9\.\-]+[.][a-zA-Z]*$"
        if re.match(patron, correo):
            return True
        else:
            return False
        
    def validar_cedula(correo):
        patron = r"^([0-9]{10})$"
        if re.match(patron, correo):
            return True
        else:
            return False

    def listar(self):
        return Persona.query.all()
    
    




