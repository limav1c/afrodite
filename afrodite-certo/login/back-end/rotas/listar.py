from geral.config import *
from modelo.pessoa import *

@app.route("/listar/<string:classe>")
@jwt_required()
def listar(classe):
    
    try:
        print("quem está acessando: ")
        current_user = get_jwt_identity()
        print(current_user)
        
        dados = None
        if classe == "Pessoa":
            dados = db.session.query(Pessoa).all()

        # converter dados para json
        lista_jsons = [x.json() for x in dados]
        # converter a lista do python para json
        resposta = jsonify({"resultado":"ok","detalhes":lista_jsons})

    except Exception as e:
        resposta = jsonify({"resultado":"erro","detalhes":str(e)})
        print("ERRO: "+str(e))

    return resposta