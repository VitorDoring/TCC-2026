from flask import request,jsonify
from api.services.questao_service import Questao_service
import pandas as pd

class Questao_controle:
    def __init__(self, questao_service:Questao_service):
        print("⬆️  Questao_controle.constructor()")
        self.__questao_service = questao_service

    def cadastrar(self):
        print("🔵 questao_controle.cadastrar()")

        json_questao = request.json.get("questao")
        cadastro = self.__questao_service.criar(json_questao)

        return self._retornar_sucesso(
            mensagem = "Cadastro realizado com sucesso",
            data = {"questão":self._formatar_questao(json_questao)},
            codigo = 201
        )
    
    def importar(self):
        print("🔵 questao_controle.importar()")

        arquivo = next(request.files.values(), None)
        if not arquivo:

            return self._retornar_erro(
                erro = "Arquivo não enviado",
                codigo= 400
            )
        
        if not arquivo.filename.endswith(".xlsx"):
            return self._retornar_erro(
                erro = "Formato de arquivo inválido",
                codigo = 400
            )
        
        df = pd.read_excel(arquivo)
        resultado = self.__questao_service.importar_excel(df)

        return self._retornar_sucesso(
            mensagem = "Executado com sucesso",
            data = {"questões inseridas":resultado},
            codigo = 200
        )
    
    def ler(self):
        print("🔵 questao_controle.ler()")

        tipos = {"id_questao":int,"registro":int}
        
        campos_permitidos = ["id_questao","registro","nome",
                            "assunto","disciplina","tipo_questao",
                            "dificuldade","autor","enunciado"]

        filtro, erro = self._formatar_pesquisa(
                    tipos = tipos,
                    campos_permitidos = campos_permitidos,
                    args = request.args.items() 
                    )
        
        if erro:
            return self._retornar_erro(erro = erro, codigo = 400)
        
        consulta = self.__questao_service.consulta(filtro)

        return self._retornar_sucesso(
            mensagem = "Executado com sucesso",
            data = {"questão":consulta},
            codigo = 200
        )
    
    def alterar(self):
        print("🔵 questao_controle.alterar()")

        filtro, erro = self._formatar_pesquisa(
            tipos = {"id_questao":int},
            campos_permitidos = ["id_questao"],
            args = request.args.items()
        )

        if erro:
            return self._retornar_erro(erro = erro, codigo = 400)

        json_questao = request.json.get("questao")
        sucesso = self.__questao_service.atualizar(json_questao, filtro)

        if sucesso:
            return self._retornar_sucesso(
                mensagem = "Atualizado com sucesso",
                data = {"questão":self._formatar_questao(json_questao)},
                codigo = 200
            )
        else:
            return self._retornar_erro(
                erro = f"Não foi possível atualizar a questão de id {json_questao.get('id_questao')}",
                codigo = 400
            )
        
    def deletar(self, id_questao):
        print("🔵 questao_controle.deletar()")
        excluiu = self.__questao_service.excluir(id_questao)
        if excluiu:
            return self._retornar_sucesso(
                mensagem = "Excluído com sucesso",
                data = None,
                codigo = 200
            )
        else:
            return self._retornar_erro(
                erro = f"Não existe questão com o id {id_questao}",
                codigo =  404
            )

        

    def _formatar_pesquisa(self,tipos,campos_permitidos,args):
        filtro = {}

        for key, value in args:
            if key not in campos_permitidos or not value:
                continue

            conversor = tipos.get(key,str)

            try:
                filtro[key] = conversor(value)
            except ValueError:
                return None, f"{key} inválido: {value}"
            
        return filtro, None
            

    def _formatar_questao(self,questao):
        professor = questao.get("professor")

        formatado = {
            "id_questao":questao.get("id_questao"),
            "professor":{
                "registro":professor.get("registro"),
                "nome":professor.get("nome")
            },
            "assunto":questao.get("assunto"),
            "disciplina":questao.get("disciplina"),
            "tipo_questao":questao.get("tipo_questao"),
            "dificuldade":questao.get("dificuldade"),
            "autor":questao.get("autor"),
            "enunciado":questao.get("enunciado"),
            "alternativas":questao.get("alternativas"),
            "alternativa_correta":questao.get("alternativa_correta")
        }

        return formatado
    
    def _retornar_sucesso(self,mensagem,data,codigo):
        return jsonify({
            "sucesso": True,
            "mensagem": mensagem,
            "data":data
        }),codigo
                
    def _retornar_erro(self, erro, codigo):
        return jsonify({
            "sucesso": False,
            "erro": {"mensagem":erro}
        }),codigo