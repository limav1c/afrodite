# https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage.html

from flask import Flask
from flask import jsonify
from flask import request

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app = Flask(__name__)

# configuração da senha secreta da aplicação
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
# vínculo com a biblioteca de gerenciamento do jwt
jwt = JWTManager(app)

# rota para autenticação e obtenção do token
@app.route("/login", methods=["POST"])
def login():
    # receber os parâmetros
    username = request.json.get("username")
    password = request.json.get("password")
    # validação estática de login e senha
    if username != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401
    # códigos de erro http:
    # https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Status

    # criar a json web token (JWT)
    tk = create_access_token(identity=username)

    # retornar
    return jsonify(access_token=tk)

@app.route("/protected", methods=["GET"])
@jwt_required() # rota protegida? Então jwt é requerida
def protected():
    # acessa a identidade de quem está logado
    # se não está logado, a requisição é negada
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == "__main__":
    app.run()

'''

$ curl localhost:5000/protected
{"msg":"Missing Authorization Header"}

$ curl -X POST localhost:5000/login -d '{"username":"test","password":"test"}' -H 'Content-Type: application/json'
{"access_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY1ODMxMzcyNiwianRpIjoiYTU1ZWUxZWItNWE0Yy00ODEyLThmZGUtMjY0YmY1M2MzNGRiIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InRlc3QiLCJuYmYiOjE2NTgzMTM3MjYsImV4cCI6MTY1ODMxNDYyNn0.kG2au9uMC9vn0iSSp4eHCCdCbXFaHeIlpDvhO_8zOxE"}

$ curl localhost:5000/protected -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY1ODMxMzcyNiwianRpIjoiYTU1ZWUxZWItNWE0Yy00ODEyLThmZGUtMjY0YmY1M2MzNGRiIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InRlc3QiLCJuYmYiOjE2NTgzMTM3MjYsImV4cCI6MTY1ODMxNDYyNn0.kG2au9uMC9vn0iSSp4eHCCdCbXFaHeIlpDvhO_8zOxE'
{"logged_in_as":"test"}

'''    