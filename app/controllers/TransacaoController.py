from flask import Blueprint, jsonify
from app.services.transacao_service import (
    listar_transacoes,
    criar_transacao,
    editar_transacao,
    notificar_seletores,
    status_mais_frequente,
    editar_transacao_remota,
    editar_transacao_seletor
)

transacao_bp = Blueprint('transacao_bp', __name__)

@transacao_bp.route('/transacoes', methods=['GET'])
def ListarTransacoes():
    return jsonify(listar_transacoes())

@transacao_bp.route('/transacoes/<int:rem>/<int:reb>/<int:valor>', methods=['POST'])
def CriaTransacao(rem, reb, valor):
    if rem and reb and valor:
        transacao = criar_transacao(rem, reb, valor)
        resultados = notificar_seletores(transacao)

        status_final = status_mais_frequente(resultados)
        transacao = editar_transacao_remota(transacao.id, status_final)

        for resultado in resultados:
            editar_transacao_seletor(resultado['id_transacao'], resultado['status'])

        return jsonify(transacao)
    return jsonify(['Method Not Allowed'])

@transacao_bp.route('/transactions/<int:id>/<int:status>', methods=['POST'])
def EditaTransacao(id, status):
    if id and status:
        try:
            transacao = editar_transacao(id, status)
            return jsonify(transacao) if transacao else jsonify(["Transação não encontrada"])
        except Exception:
            return jsonify({"message": "transação não atualizada"})
    else:
        return jsonify(['Method Not Allowed'])
