from flask import Blueprint, jsonify
from app.services.seletor_service import (
    listar_seletores, inserir_seletor,
    buscar_seletor_por_id, editar_seletor,
    deletar_seletor
)

seletor_bp = Blueprint('seletor_bp', __name__)

@seletor_bp.route('/seletor', methods=['GET'])
def ListarSeletor():
    return jsonify(listar_seletores())

@seletor_bp.route('/seletor/<string:nome>/<string:ip>', methods=['POST'])
def InserirSeletor(nome, ip):
    if nome and ip:
        return jsonify(inserir_seletor(nome, ip))
    return jsonify(['Method Not Allowed'])

@seletor_bp.route('/seletor/<int:id>', methods=['GET'])
def UmSeletor(id):
    if id:
        seletor = buscar_seletor_por_id(id)
        return jsonify(seletor) if seletor else jsonify(['Not Found'])
    else:
        return jsonify(['Method Not Allowed'])

seletor_bp.route('/seletor/<int:id>/<string:nome>/<string:ip>', methods=['POST'])
def EditarSeletor(id, nome, ip):
    if id and nome and ip:
        try:
            seletor = editar_seletor(id, nome, ip)
            return jsonify(seletor) if seletor else jsonify(['Seletor não encontrado'])
        except Exception:
            return jsonify({"message": "Atualização não realizada"})
    else:
        return jsonify(['Method Not Allowed'])

seletor_bp.route('/seletor/<int:id>', methods=['DELETE'])
def ApagarSeletor(id):
    if id:
        if deletar_seletor(id):
            return jsonify({"message": "Seletor Deletado com Sucesso"})
        return jsonify(["Seletor não encontrado"])
    else:
        return jsonify(['Method Not Allowed'])
