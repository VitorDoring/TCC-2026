from api.modelos.questao import Questao
from api.modelos.usuario import Usuario
from api.DAOs.questao_dao import Questao_dao

from api.utils.resposta_erro import resposta_erro

class Questao_service:
    def __init__(self, questao_dao_dependency: Questao_dao):
        print("⬆️ questao_service.__init__()")
        self.__questao_dao = questao_dao_dependency

    def criar(self, json_questao: dict):
        print("🟣 questao_service.criar()")



        obj_questao = Questao()
        self._setar_modelo_questao(obj_questao, json_questao)

        if self.__questao_dao.campo_existe("enunciado",obj_questao.enunciado):
            raise resposta_erro(
                400,
                "Enunciado repetido",
                {"mensagem":f'A questão de enunciado "{obj_questao.enunciado}" já está cadastrada'}
            )
        return self.__questao_dao.criar(obj_questao)
    
    
    def importar_excel(self,df) -> int:
        print("🟣 questao_service.importar_excel()")

        docs = []

        inseridos = 0

        for _, linha in df.iterrows():
            if linha.isnull().all():
                print("❌ Linha com valor nulo:", linha)
                continue
            try:
                obj_questao = Questao()
                obj_professor = Usuario()

                self._ler_linha(obj_questao,obj_professor,linha)

                if self.__questao_dao.campo_existe("enunciado",obj_questao.enunciado):
                    continue

                doc = self.__questao_dao.set_doc(obj_questao)

                docs.append(doc)
                inseridos += 1

            except Exception as e:
                print(f"Erro na linha {_} → {e}")
                continue

        if docs:
            self.__questao_dao.importar_excel(docs)
        return inseridos

    
    def consulta(self, filtro) -> list[dict]:
        print("🟣 questao_service.consulta()")
        return self.__questao_dao.consulta(filtro)
    
    
    def atualizar(self, json_questao: dict, filtro) -> bool:
        print("🟣 questao_service.atualizar()")

        obj_questao = Questao()
        self._setar_modelo_questao(obj_questao, json_questao)
        return self.__questao_dao.atualizar(obj_questao,filtro)

    
    def excluir(self, _id: str) -> bool:
        print("🟣 questao_service.excluir()")
        return self.__questao_dao.excluir(_id)
    
    _campos_questao = [
            "assunto",
            "disciplina",
            "tipo_questao",
            "dificuldade",
            "enunciado"
        ]

    
    def _setar_modelo_questao(self,obj_questao,json_questao):


        for campo in self._campos_questao:
            setattr(obj_questao, campo, json_questao.get(campo))
        
        dados_professor = json_questao.get("professor")
        professor = Usuario()
        professor.nome = dados_professor.get("nome")
        obj_questao.professor = professor

        if obj_questao.tipo_questao == "Objetiva":
            obj_questao.alternativas = json_questao.get("alternativas")
            obj_questao.alternativa_correta = json_questao.get("alternativa_correta")

        if json_questao.get("autor") == "":
            obj_questao.autor = obj_questao.professor.nome
        else:
            obj_questao.autor = json_questao.get("autor")



    def _ler_linha(self, obj_questao,obj_professor,linha):

        for campo in self._campos_questao:
            setattr(obj_questao, campo, linha.get(campo))

        obj_professor.nome = linha.get("nome professor")

        obj_questao.professor = obj_professor