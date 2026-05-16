from functools import wraps
from flask import request
from api.utils.resposta_erro import resposta_erro

class Questao_middleware:
    def validar_body(self, f):
        @wraps(f)
        def decorated_function(*args,**kwargs):
            print("🔷 questao_middleware.validar_body()")
            body = request.get_json()

            if not body or 'questao' not in body:
                raise resposta_erro(400, "Erro na validação de dados", {"mensagem": "O campo 'questão' é obrigatório!"})
            
            questao = body['questao']
            campos_obrigatorios = ["professor","assunto","disciplina",
                                    "tipo_questao","dificuldade","autor",
                                    "enunciado"]
            
            professor = questao["professor"]
            campos_obrigatorios_professor = ["nome"]

            for campo in campos_obrigatorios:
                if campo not in questao:
                    raise resposta_erro(400, "Erro na validação de dados", {"mensagem":f"O campo '{campo}' é obrigatório!"})
                                
            for campo_professor in campos_obrigatorios_professor:
                if campo_professor not in professor:
                    raise resposta_erro(400, "Erro na validação de dados", {"mensagem": f"O campo '{campo_professor}' do professor é obrigatório!"})
                
            return f(*args, **kwargs)
        return decorated_function
    
    def validar_id_questao(self,f):
        @wraps(f)
        def decorated_function(*args,**kwargs):
            print("🔷 questao_middleware.validar_id()")
            if 'id_hash' not in kwargs:
                raise resposta_erro(400, "Erro na validação de dados", {"mensagem": "O parâmetro 'id_hash' é obrigatório!"})
            return f(*args, **kwargs)
        return decorated_function