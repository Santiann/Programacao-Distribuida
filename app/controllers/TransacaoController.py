from flask import Blueprint, jsonify
from app.services.transacao_service import (
    listar_transacoes as listar_transacoes_service,
    criar_transacao as criar_transacao_service,
    editar_transacao as editar_transacao_service,
    notificar_seletores,
    status_mais_frequente,
    editar_transacao_remota,
    editar_transacao_seletor
)

transacao_bp = Blueprint('transacao_bp', __name__)

@transacao_bp.route('/transacoes', methods=['GET'])
def listar_transacoes():
    return jsonify(listar_transacoes_service())

@transacao_bp.route('/transacoes/<int:rem>/<int:reb>/<int:valor>', methods=['POST'])
def cria_transacao(rem, reb, valor):
    if rem and reb and valor:
        transacao = criar_transacao_service(rem, reb, valor)
        resultados = notificar_seletores(transacao)

        status_final = status_mais_frequente(resultados)
        remote_update = editar_transacao_remota(transacao.id, status_final)

        for resultado in resultados:
            editar_transacao_seletor(resultado['id_transacao'], resultado['status'])

        return jsonify(remote_update or transacao.to_dict())

    return jsonify(['Method Not Allowed'])

@transacao_bp.route('/transactions/<int:id>/<int:status>', methods=['POST'])
def edita_transacao(id, status):
    if id and status:
        try:
            transacao = editar_transacao_service(id, status)
            return jsonify(transacao) if transacao else jsonify(["Transação não encontrada"])
        except Exception:
            return jsonify({"message": "transação não atualizada"})
    else:
        return jsonify(['Method Not Allowed'])
