from flask import jsonify


class Resposta:

    @staticmethod
    def sucesso(mensagem, data=None, codigo=200):

        return jsonify({
            "sucesso": True,
            "mensagem": mensagem,
            "data": data
        }), codigo

    @staticmethod
    def erro(mensagem, codigo=400, detalhes=None):

        return jsonify({
            "sucesso": False,
            "mensagem": mensagem,
            "erro": detalhes
        }), codigo