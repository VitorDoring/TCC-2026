from flask import Blueprint, request
from functools import wraps
#from backend.api.middlewares.jwt_middleware import Jwt_middleware
#from backend.api.middlewares.questao_middleware import Questao_middleware
from api.controles.questao_controle import Questao_controle

class Questao_rotas:
    #def __init__(self, jwt_middleware:Jwt_middleware, questao_middleware:Questao_middleware, questao_controle:Questao_controle):
    def __init__(self, questao_controle:Questao_controle):
        print("⬆️  questao_rotas.__init__()")

        #self.jwt_middleware = jwt_middleware
        #self.questao_middleware = questao_middleware
        self.__questao_controle = questao_controle

        self.__blueprint = Blueprint('questoes',__name__)

    def criar_rotas(self):
        
        @self.__blueprint.route('/',methods=['POST'])
        #@self.jwt_middleware.validar_token
        #@self.jwt_middleware.validar_body_criar
        def cadastrar():
            return self.__questao_controle.cadastrar()
        
        def importar():
            return self.__questao_controle.importar()
        
        @self.__blueprint.route('/',methods=['GET'])
        def ler():
            return self.__questao_controle.cadastrar()
        
        @self.__blueprint.route('/',methods=['PUT'])
        def alterar():
            return self.__questao_controle.alterar()
        
        @self.__blueprint.route('/<int:id_questao>',methods=['DELETE'])
        def deletar(id_questao):
            return self.__questao_controle.deletar(id_questao)
        
        return self.__blueprint