from flask import Blueprint, jsonify
from app.services.cliente_service import (
    listar_clientes, inserir_cliente, buscar_cliente_por_id,
    editar_cliente, deletar_cliente
)

cliente_bp = Blueprint('cliente_bp', __name__)

@cliente_bp.route('/cliente', methods=['GET'])
def ListarCliente():
    return jsonify(listar_clientes())

@cliente_bp.route('/cliente/<string:nome>/<string:senha>/<int:qtdMoedas>', methods=['POST'])
def InserirCliente(nome, senha, qtdMoedas):
    if nome and senha and qtdMoedas:
        return jsonify(inserir_cliente(nome, senha, qtdMoedas))

    return jsonify(['Method Not Allowed'])

@cliente_bp.route('/cliente/<int:id>', methods=['GET'])
def UmCliente(id):
    if id:
        cliente = buscar_cliente_por_id(id)
        return jsonify(cliente) if cliente else jsonify(['Not Found'])
    else:
        return jsonify(['Method Not Allowed'])

# Da apenas para editar a quantidade de moeadas que o cliente possui.
@cliente_bp.route('/cliente/<int:id>/<int:qtdMoedas>', methods=['POST'])
def EditarCliente(id, qtdMoedas):
    if id and qtdMoedas:
        try:
            cliente = editar_cliente(id, qtdMoedas)
            return jsonify(cliente) if cliente else jsonify(['Cliente não encontrado'])
        except Exception:
            return jsonify({"message": "Atualização não realizada"})
    else:
        return jsonify(['Method Not Allowed'])

@cliente_bp.route('/cliente/<int:id>', methods=['DELETE'])
def ApagarCliente(id):
    if id:
        if deletar_cliente(id):
            return jsonify({"message": "Cliente Deletado com Sucesso"})
        return jsonify(["Cliente não encontrado"])
    else:
        return jsonify(['Method Not Allowed'])
