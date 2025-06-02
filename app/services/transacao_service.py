from app.models.Transacao import Transacao
from app.models.Seletor import Seletor
from app import db
from datetime import datetime
from collections import Counter
import requests
import os
from flask import Blueprint, jsonify

HOST_API = os.getenv("HOST_API", "127.0.0.1")

def listar_transacoes():
    return Transacao.query.all()

def criar_transacao(remetente, recebedor, valor):
    transacao = Transacao(
        remetente=remetente,
        recebedor=recebedor,
        valor=valor,
        status=0,
        horario=datetime.now()
    )
    db.session.add(transacao)
    db.session.commit()
    return transacao

def editar_transacao(id, status):
    transacao = Transacao.query.filter_by(id=id).first()
    if transacao:
        transacao.status = status
        db.session.commit()
    return transacao

def notificar_seletores(transacao):
    seletores = Seletor.query.all()
    resultado_json = []

    for seletor in seletores:
        url = f'http://{seletor.ipSeletor}/transacao/{transacao.id}/{transacao.remetente}/{seletor.id}/{transacao.valor}/{transacao.horario}'
        try:
            response = requests.post(url)
            resultado_json.append(response.json())
        except:
            return jsonify(f"Erro ao contatar seletor {seletor.ipSeletor}")
    return resultado_json

def status_mais_frequente(resultados):
    contagem = Counter(obj["status"] for obj in resultados)
    return contagem.most_common(1)[0][0]

def editar_transacao_remota(id, status):
    url = f'http://{HOST_API}:5000/transactions/{id}/{status}'
    try:
        return requests.post(url)
    except Exception as e:
        print(f'Erro ao atualizar transação central: {e}')

def editar_transacao_seletor(id, status):
    url = f'http://{HOST_API}:5001/trans/{id}/{status}'
    try:
        response = requests.post(url)
        if response.status_code == 200:
            print('Resposta do seletor:', response.json())
    except Exception as e:
        print(f'Erro ao atualizar seletor: {e}')
