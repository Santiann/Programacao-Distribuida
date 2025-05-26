from flask import Blueprint, jsonify
import requests
from app.models.minhasTransacoes import minhasTransacoes
from app.models.MeuSeletor import MeuSeletor
from app.models.Validador import Validador
from app.services.transacoes_service import verifica_transacao, Cadastro_das_Transacoes
from app.services.validador_service import escolhe_validadores, adicionar_transacao, adicionar_flag, tirar_flag
from collections import Counter
from app import db
from app.services.cliente_service import visualizar_Cliente_id

seletorlocal_bp = Blueprint('seletorlocal_bp', __name__)

@seletorlocal_bp.route('/meuSeletor', methods=['GET'])
def Seletor():
    seletor = MeuSeletor.query.all()
    return jsonify(seletor)
    
@seletorlocal_bp.route('/trans', methods=['GET'])
def transacoes():
    transacoes = minhasTransacoes.query.all()
    return jsonify(transacoes)

@seletorlocal_bp.route('/trans/<int:idTransacao>/<int:status>', methods=['POST'])
def AttTransacoes(idTransacao, status):
    if idTransacao == '' and status == '':
        return jsonify(['Method Not Allowed'])

    Mtransacoes = minhasTransacoes.query.filter_by(
        idTransacao=idTransacao).first()

    Mtransacoes.status = status
    db.session.commit()
    verifica_transacao(idTransacao)

    return jsonify(Mtransacoes)

@seletorlocal_bp.route('/meuSeletor/<int:id>', methods=['DELETE'])
def ApagarMeuSeletor(id):
    # Lógica invertida para a redução do else e também retirado um nivel de camada.
    if (id == ''):
        return jsonify(['Method Not Allowed'])

    objeto = MeuSeletor.query.get(id)
    db.session.delete(objeto)
    db.session.commit()

    return jsonify({"message": "meuSeletor Deletado com Sucesso"})

@seletorlocal_bp.route('/transacao/<int:id>/<int:remetente>/<int:idSeletor>/<int:valor>/<string:horario>', methods=['POST'])
def receberTransacao(id, remetente, idSeletor, valor, horario):
    if id == '' and remetente == '' and idSeletor == '' and valor == '' and horario == '':
        return jsonify(['Method Not Allowed'])
        
    Validadores = Validador.query.all()
    rem = visualizar_Cliente_id(remetente)
    escolhidos = escolhe_validadores()

    saldoRem = rem['qtdMoeda']
    resultado_json = []
    for v in Validadores:
        for e in escolhidos:
            if v.id == e:
                url = f'http://{v.ip}/validar/{v.id}/{saldoRem}/{valor}/{horario}'
                response = requests.post(url)
                resultado_json.append(response.json())

    status_counts = Counter(item['status'] for item in resultado_json)

    most_common_status = status_counts.most_common(1)[0][0]

    print(f"O valor de status que mais aparece é: {most_common_status}")

    ids_with_different_status = [
        item['id'] for item in resultado_json if item['status'] != most_common_status]
    ids_with_same_status = [
        item['id'] for item in resultado_json if item['status'] == most_common_status]
    print(
        f"IDs com valores de status diferentes da maioria: {ids_with_different_status}")
    print(
        f"IDs com valores de status igauis da maioria: {ids_with_same_status}")

    # PARA QUEM ACERTOU A TRANSACAO adiciona +1
    for same_ids in ids_with_same_status:
        adicionar_transacao(same_ids)
        # TIRA FLAG CASO ELE TENHA ALGUMA E TRANSACOES SEJA >= 10000
        tirar_flag(same_ids)

    # ADICIONA UMA FLAG PRA QUEM ERROU A TRANSACAO
    for different_ids in ids_with_different_status:
        # ADICIONA UMA FLAG E CASO SEJA A TERCEIRA ELE É DELETADO DA REDE
        adicionar_flag(different_ids)

    response_data = {'id_transacao': id,
                        'status': most_common_status, 'id_seletor': idSeletor}

    # Criar uma nova lista com os elementos formatados
    numeros_formatados = [f"id: {num}" for num in ids_with_same_status]

    # Unir os elementos da lista em uma única string, separados por vírgulas
    string_formatada = ", ".join(numeros_formatados)

    Cadastro_das_Transacoes(
        id, valor, string_formatada, most_common_status)

    return response_data
