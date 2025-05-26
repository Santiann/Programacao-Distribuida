from flask import Blueprint, jsonify
from app import db
from app.models.Validador import Validador
from app.models.MeuSeletor import MeuSeletor
from app.services.validador_service import calcular_percent
validador_bp = Blueprint('validador_bp', __name__)

@validador_bp.route('/validador', methods=['GET'])
def ListarCliente():
    validador = Validador.query.all()
    return jsonify(validador)


@validador_bp.route('/validador/<string:nome>/<string:ip>/<int:FCoins>', methods=['POST'])
def Cadastro_dos_Validadores(nome, ip, FCoins):
    if nome == '' and ip == '' and FCoins < 100:
        return jsonify(['Method Not Allowed'])

    objeto = Validador(nome=nome, ip=ip, flag=0, FCoins=FCoins,
                       percent=0, transacoes=0, aux_flag=1)
    db.session.add(objeto)
    db.session.commit()

    calcular_percent()
    return jsonify(objeto)


@validador_bp.route('/validador/<int:id>', methods=['GET'])
def UmSeletor(id):
    if (id == ''):
        return jsonify(['Method Not Allowed'])
        
    produto = Validador.query.get(id)
    return jsonify(produto)


@validador_bp.route('/validador/<int:id>', methods=['DELETE'])
def ApagarValidador(id):
    if (id == ''):
        return jsonify(['Method Not Allowed'])
        
    objeto = Validador.query.get(id)
    meuSeletor = MeuSeletor.query.filter_by(id=1).first()

    meuSeletor.fCoins -= objeto.FCoins
    db.session.commit()
    db.session.delete(objeto)
    db.session.commit()

    return jsonify({"message": "Validador Deletado com Sucesso"})

