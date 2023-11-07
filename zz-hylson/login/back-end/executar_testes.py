from modelo.pessoa import *
from testes import *

with app.app_context():

    TestarCifrar.run()
    TestarPessoa.run()