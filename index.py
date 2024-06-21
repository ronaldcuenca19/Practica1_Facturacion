from app import create_app
from jsonschema import ValidationError
from flask import jsonify, make_response, request
from controller.productoControl import ProductoControl

app = create_app()

@app.after_request
def after_request_func(response):
    origin = request.headers.get('Origin')
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Headers', 'x-csrf-token')
        response.headers.add('Access-Control-Allow-Headers', 'Accept')
        response.headers.add('Access-Control-Allow-Headers', 'X-Access-Token')
        response.headers.add('Access-Control-Allow-Methods',
        'GET, POST, OPTIONS, PUT, PATCH, DELETE')
        if origin:
            response.headers.add('Access-Control-Allow-Origin', origin)
    else:
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            if origin:
                response.headers.add('Access-Control-Allow-Origin', origin)
    return response

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