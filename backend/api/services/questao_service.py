from api.modelos.questao import Questao
from api.modelos.usuario import Usuario
from backend.api.DAOs.questao_dao import Questao_dao

from api.utils.resposta_erro import resposta_erro

class Questao_service:
    def __init__(self, questao_dao_dependency: Questao_dao):
        print("⬆️ questao_service.__init__()")
        self.__questao_dao = questao_dao_dependency

    def criar(self, json_questao: dict) -> bool:
        print("🟣 questao_service.criar()")

        obj_questao = Questao()
        obj_questao.id_questao = self.__questao_dao.buscar_ultimo_id()
        self._setar_modelo_questao(obj_questao, json_questao)

        return self.__questao_dao.criar(obj_questao)
    
    
    def importar_excel(self,df) -> int:
        print("🟣 questao_service.importar_excel()")

        docs = []

        inseridos = 0
        ultimo_id = self.__questao_dao.buscar_ultimo_id()

        for _, linha in df.iterrows():
            if linha.isnull().all():
                print("❌ Linha com valor nulo:", linha)
                continue
            try:
                obj_questao = Questao()
                obj_professor = Usuario()

                obj_questao.id_questao = ultimo_id
                obj_questao.assunto = linha["assunto"]
                obj_questao.disciplina = linha["disciplina"]
                obj_questao.tipo_questao = linha["tipo_questao"]
                obj_questao.dificuldade = linha["dificuldade"]
                obj_questao.autor = linha["autor"]
                obj_questao.enunciado = linha["enunciado"]
                obj_questao.alternativas = linha["alternativas"]
                obj_questao.alternativa_correta = linha["alternativa_correta"]

                obj_professor.nome = linha["nome professor"]
                obj_professor.registro = linha["registro professor"]

                obj_questao.professor = obj_professor

                if self.__questao_dao.campo_existe("enunciado",obj_questao.enunciado):
                    continue

                doc = {
                    "id_questao":obj_questao.id_questao,
                    "assunto":obj_questao.assunto,
                    "disciplina":obj_questao.disciplina,
                    "autor":obj_questao.autor,
                    "enunciado":obj_questao.enunciado,
                    "alternativas":obj_questao.alternativas,
                    "alternativa_correta":obj_questao.alternativa_correta,
                    "professor":obj_questao.professor
                }

                docs.append(doc)
                inseridos += 1
                ultimo_id += 1

            except Exception as e:
                print(f"Erro na linha: {linha} → {e}")
                continue

        self.__questao_dao.importar_excel(docs)

    
    def consulta(self, filtro) -> list[dict]:
        print("🟣 questao_service.consulta()")
        return self.__questao_dao.consulta(filtro)
    
    
    def atualizar(self, json_questao: dict, filtro) -> bool:
        print("🟣 questao_service.atualizar()")

        obj_questao = Questao()
        self._setar_modelo_questao(obj_questao, json_questao)
        return self.__questao_dao.atualizar(obj_questao,filtro)

    
    def excluir(self, id_questao: int) -> bool:
        print("🟣 questao_service.excluir()")
        obj_questao = Questao()
        obj_questao.id_questao = id_questao
        return self.__questao_dao.excluir(obj_questao.id_questao)

    
    def _setar_modelo_questao(self,obj_questao,json_questao):
        obj_questao.assunto = json_questao.get("assunto")
        obj_questao.disciplina = json_questao.get("disciplina")
        obj_questao.tipo_questao = json_questao.get("tipo_questao")
        obj_questao.dificuldade = json_questao.get("dificuldade")
        obj_questao.autor = json_questao.get("autor")
        obj_questao.enunciado = json_questao.get("enunciado")
        obj_questao.alternativas = json_questao.get("alternativas")
        obj_questao.alternativa_correta = json_questao.get("alternativa_correta")
        
        dados_professor = json_questao.get("professor")
        professor = Usuario()
        professor.registro = dados_professor.get("registro")
        professor.nome = dados_professor.get("nome")
        obj_questao.professor = professor