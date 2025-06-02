from flask import Blueprint, jsonify
from app import db
from app.models.Validador import Validador
from app.models.MeuSeletor import MeuSeletor
from app.services.validador_service import calcular_percent
validador_bp = Blueprint('validador_bp', __name__)

@validador_bp.route('/validador', methods=['GET'])
def listar_cliente():
    validador = Validador.query.all()
    return jsonify(validador)


@validador_bp.route('/validador/<string:nome>/<string:ip>/<int:FCoins>', methods=['POST'])
def cadastro_dos_validadores(nome, ip, FCoins):
    if nome == '' and ip == '' and FCoins < 100:
        return jsonify(['Method Not Allowed'])

    objeto = Validador(nome=nome, ip=ip, flag=0, FCoins=FCoins,
                       percent=0, transacoes=0, aux_flag=1)
    db.session.add(objeto)
    db.session.commit()

    calcular_percent()
    return jsonify(objeto)


@validador_bp.route('/validador/<int:id>', methods=['GET'])
def um_seletor(id):
    produto = Validador.query.get(id)
    return jsonify(produto)


@validador_bp.route('/validador/<int:id>', methods=['DELETE'])
def apagar_validador(id):
    objeto = Validador.query.get(id)
    meuSeletor = MeuSeletor.query.filter_by(id=1).first()

    meuSeletor.fCoins -= objeto.FCoins
    db.session.commit()
    db.session.delete(objeto)
    db.session.commit()

    calcular_percent()

    return jsonify({"message": "Validador Deletado com Sucesso"})

