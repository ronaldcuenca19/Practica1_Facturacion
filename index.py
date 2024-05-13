from app import create_app
from jsonschema import ValidationError
from flask import jsonify, make_response
from controller.productoControl import ProductoControl

app = create_app()

@app.errorhandler(400)
def bad_request(error):
    if isinstance(error.description, ValidationError):
        msg_error = error.description
        return make_response(
        jsonify({"msg":"error", "code":400, "datos":{"error": msg_error.message}}),
        400
    )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")



#pip install python-dotenv
#apt-get install python3-mysqldb

# ORM que se va a utilizar:

# pip install flask_sqlalchemy
#pip install PyMySQL
#pip install cryptography