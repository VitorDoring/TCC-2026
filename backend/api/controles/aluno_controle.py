from flask import request,jsonify
from api.services.aluno_service import Aluno_service
from api.utils.resposta import Resposta
import pandas as pd

class Aluno_controle:
    def __init__(self, aluno_service:Aluno_service):
        print("⬆️  Aluno_controle.constructor()")
        self.__aluno_service = aluno_service

    def cadastrar(self):
        print("🔵 aluno_controle.cadastrar()")

        json_aluno = request.json.get("aluno")
        cadastro = self.__aluno_service.criar(json_aluno)
        return Resposta.sucesso(
            mensagem = "Cadastro realizado com sucesso",
            data = {"aluno":self._formatar_aluno(json_aluno)},
            codigo = 201
        )
    
    def importar(self):
        print("🔵 aluno_controle.importar()")

        arquivo = next(request.files.values(), None)
        if not arquivo:
        
            return Resposta.erro(
                mensagem = "Arquivo não enviado",
                codigo = 400
            )
        
        if not arquivo.filename.endswith(".xlsx"):
            return Resposta.erro(
                mensagem = "Formato inválido",
                codigo = 400
            )
        
        df = pd.read_excel(arquivo)
        resultado = self.__aluno_service.importar_excel(df)

        return Resposta.sucesso(
            mensagem = "Executado com sucesso",
            data = {"alunos inseridos": resultado},
            codigo = 200
        )
    
    
    def ler(self):
        print("🔵 aluno_controle.ler()")

        tipos = {
            "matricula_aluno": int,
            "serie":int,
            "ativo":bool
        }

        campos_permitidos = {"matricula_aluno", "nome_aluno",
                            "turma" ,"serie","situacao","ativo"}

        filtro = {}

        for key, value in request.args.items():
            if key not in campos_permitidos or not value:
                continue

            conversor = tipos.get(key, str)

            try:
                filtro[key] = conversor(value)
            except ValueError:
                return jsonify({
                    "sucesso": False,
                    "erro": {"mensagem": f"{key} inválido: {value}"}
                }), 400
    
        
        consulta = self.__aluno_service.consulta(filtro)
        

        return jsonify({
            "sucesso":True,
            "mensagem":"Executado com sucesso",
            "data":{"alunos":consulta}
        }),200
    
    
    def alterar(self,matricula_aluno):
        print("🔵 aluno_controle.alterar()")

        json_aluno = request.json.get("aluno") 
        sucesso = self.__aluno_service.atualizar(json_aluno, matricula_aluno)
        
        if sucesso:
            return jsonify({
                "sucesso": True,
                "mensagem": "Atualizado com sucesso",
                "data": {
                    "aluno":self._formatar_aluno(json_aluno)               
                }
            }), 200
        else:
            return jsonify({
                "sucesso": False,
                "erro": {"mensagem": f"Não foi possível atualizar o aluno com a matricula {json_aluno.get("matricula_aluno")}"},
            }), 404
    
    def deletar(self, matricula_aluno):
        print("🔵 aluno_controle.deletar()")
        excluiu = self.__aluno_service.excluir(matricula_aluno)
        if excluiu:
            return jsonify({
            "sucesso": True,
            "mensagem": "Excluído com sucesso"
        }), 204
        else:
            return jsonify({
                "sucesso": False,
                "erro": {"mensagem": f"Não existe aluno com a matrícula {matricula_aluno}"}
            }), 404
        
    def _formatar_aluno(self, aluno):
        return {
            "matricula_aluno": aluno.get("matricula_aluno"),
            "nome_aluno": aluno.get("nome_aluno"),
            "turma": aluno.get("turma"),
            "serie": aluno.get("serie"),
            "situacao": aluno.get("situacao"),
            "email_aluno": aluno.get("email_aluno"),
            "ativo":aluno.get("ativo")
        }
