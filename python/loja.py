#
# IMPORTAÇÕES
#

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
import datetime

#
# VARIÁVEIS E CONFIGURAÇÕES
#

app = Flask(__name__)

# configurações específicas para o SQLite
caminho = os.path.dirname(os.path.abspath(__file__))
arquivobd = os.path.join(caminho, 'afrodite.db')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + arquivobd

db = SQLAlchemy(app)

CORS(app)


#
# CLASSES
#

class Produto(db.Model):
    # atributos da pessoa
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.Text)
    situacao = db.Column(db.Text)
    cor = db.Column(db.Text)
    nome_imagem= db.Column(db.Text)
    saida=db.Column(db.Boolean,  default=False)

    # expressar a classe em formato texto
    def __str__(self):
        return f'{self.descricao}, {self.situacao}, {self.cor}, {self.nome_imagem}, {self.saida}'

    # expressar a classe em formato json
    def json(self):
        return {
            "id": self.id,
            "descricao": self.descricao,
            "situacao": self.situacao,
            "cor": self.cor,
            "nome_imagem":self.nome_imagem,
            "saida": self.saida
        }

class Compra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #informacoes do usuario e opiniao, data da saida
    info=db.Column(db.Text)
    
    #produto_id = db.Column(db.Integer, db.ForeignKey(Produto.id), nullable=True)
    #produto = db.relationship("Produto")

    # lista de produtos :-)
    produtos = db.relationship("Produto", secondary="ProdutosDaCompra")
    
    def __str__(self):
        s = f'''
        Produto: {self.produto}
        '''
        for c in self.produtos:
            s += f'\n passou em: {c}'
        
        return s

# tabela n x n (sem classe - acessível via lista "produtos" na classe "Compra")
ProdutosDaCompra = db.Table('ProdutosDaCompra', db.metadata,
    db.Column('id_produto', db.Integer, db.ForeignKey(Produto.id)),
    db.Column('id_compra', db.Integer, db.ForeignKey(Compra.id))
)


@app.route("/")
def ola():
    return "backend operante"

# curl localhost:5000/listar_produtos

@app.route("/listar_produtos")
def listar_produtos():
    try:
        # obter os resultados
        lista = db.session.query(Produto).all()
        # converter resultado pra json
        lista_retorno = [x.json() for x in lista]
        # preparar uma parte da resposta: resultado ok
        meujson = {"resultado": "ok"}
        meujson.update({"detalhes": lista_retorno})
        # retornar a lista de pessoas json, com resultado ok
        resposta = jsonify(meujson)
        return resposta
    except Exception as e:
        return jsonify({"resultado": "erro", "detalhes": str(e)})

@app.route('/carrinho')
def carrinho():
    # Lógica para buscar os produtos do carrinho do banco de dados
    return render_template('carrinho.html', ProdutosDaCompra=ProdutosDaCompra)

@app.route('/adicionar-ao-carrinho/<int:produto_id>', methods=['POST'])
def adicionar_ao_carrinho(produto_id):
    # Lógica para adicionar o produto ao carrinho no banco de dados
    return jsonify({'mensagem': 'Produto adicionado ao carrinho'})

@app.route('/remover-do-carrinho/<int:produto_id>', methods=['POST'])
def remover_do_carrinho(produto_id):
    # Lógica para remover o produto do carrinho no banco de dados
    return jsonify({'mensagem': 'Produto removido do carrinho'})

# curl -d '{"info":"doação em 02/11/2023, para Hylson", produtos_ids="1,3,5"} -H "Content-Type:application/json" localhost:5000/finalizar
@app.route('/finalizar', methods=['POST'])
def finalizar():
    # receber os dados da requisicao(lista de produtos e informacoes sobre a compra) - olhar rota de incluir
    ## receber as informações do novo objeto
    dados = request.get_json()  
    try:
        #criar compra com os dados recebidos
        nova = Compra()
        nova.info = dados['info']
       
        # quebrar a lista de id dos produtos (essa informação vem do carrinho de compras)
        ids = dados['produtos_ids'].split(",")
        # adicionar os produtos
        for id in ids:
            # obtém o produto
            prod = db.session.get(Produto, id)
            # marca que esse produto foi doado :-)
            prod.saida = True
            # atualiza o produto
            db.session.add(prod)
            db.session.commit()

            # adiciona o produto na compra
            nova.produtos.append(prod)
                    
        # salva a compra :-)
        db.session.add(nova)
        db.session.commit()

        # responde a requisicao
        # retorno de sucesso :-)
        return jsonify({"resultado": "ok", "detalhes": "ok"})
    except Exception as e:  # em caso de erro...
        # informar mensagem de erro :-(
        return jsonify({"resultado": "erro", "detalhes": str(e)})
    
    

@app.route("/listar_produtos_categoria/<string:filtro>")
def listar_produtos_categoria(filtro):
    try:
        # obter os resultados
        # https://stackoverflow.com/questions/3325467/sqlalchemy-equivalent-to-sql-like-statement
        lista = db.session.query(Produto).filter(Produto.descricao.ilike(f'%{filtro}%')).all()
        # converter resultado pra json
        lista_retorno = [x.json() for x in lista]
        # preparar uma parte da resposta: resultado ok
        meujson = {"resultado": "ok"}
        meujson.update({"detalhes": lista_retorno})
        # retornar a lista de pessoas json, com resultado ok
        resposta = jsonify(meujson)
        return resposta
    except Exception as e:
        return jsonify({"resultado": "erro", "detalhes": str(e)})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
