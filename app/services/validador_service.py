from random import random
from time import time
import random
import time
from app.models.MeuSeletor import MeuSeletor
from app.models.Validador import Validador
from app import db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def calcular_percent():
    validadores = Validador.query.all()
    meuSeletor = MeuSeletor.query.filter_by(id=1).first()

    totalFCoins = 0
    for v in validadores:
        totalFCoins += v.FCoins
    meuSeletor.fCoins = totalFCoins
    db.session.commit()

    for v in validadores:
        percentual = int((v.FCoins / meuSeletor.fCoins) * 100)
        if percentual < 5:
            percent = 5
        elif percentual > 40:
            percent = 40
        else:
            percent = percentual

        validadorObjeto = Validador.query.filter_by(id=v.id).first()
        db.session.commit()
        validadorObjeto.percent = percent
        db.session.commit()
        # print(f'Validador {v.id} está com o percentual de {percent}')

def escolhe_validadores():
    Validadores = Validador.query.all()

    if len(Validadores) < 3:
        logger.info('Transação em espera aguarde 1 min')
        time.sleep(60)
        Validadores = Validador.query.all()
        if len(Validadores) < 3:
            logger.error('Não foi possivel concluir a transação por falta de validadores')
            return 0
    if len(Validadores) >= 5:
        escolhidos = cinco_validadores()
        logger.info('5 ou mais validadores os escolhidos sao:  %s', escolhidos)
        return escolhidos
    elif len(Validadores) == 3 or len(Validadores) == 4:
        escolhidos = tres_validadores()
        logger.info('3 ou 4 validadores os escolhidos sao:  %s', escolhidos)
        return escolhidos

def cinco_validadores():
    Validadores = Validador.query.all()
    validadoresID = []
    pesos = []

    escolhidos = tres_validadores()

    for v in Validadores:
        if v.id != escolhidos[0] and v.id != escolhidos[1] and v.id != escolhidos[2]:
            validadoresID.append(v.id)
            pesos.append(v.percent)

    v4 = random.choices(validadoresID, pesos)[0]
    # limpa as listas
    validadoresID.clear()
    pesos.clear()

    escolhidos.append(v4)

    for v in Validadores:
        if v.id != escolhidos[0] and v.id != escolhidos[1] and v.id != escolhidos[2] and v.id != v4:
            validadoresID.append(v.id)
            pesos.append(v.percent)

    v5 = random.choices(validadoresID, pesos)[0]
    escolhidos.append(v5)

    return escolhidos

def tres_validadores():
    Validadores = Validador.query.all()
    validadoresID = []
    pesos = []
    for v in Validadores:
        validadoresID.append(v.id)
        pesos.append(v.percent)

    v1 = random.choices(validadoresID, pesos)[0]
    # limpa as listas
    validadoresID.clear()
    pesos.clear()

    for v in Validadores:
        if v.id != v1:
            validadoresID.append(v.id)
            pesos.append(v.percent)

    v2 = random.choices(validadoresID, pesos)[0]
    # limpa as listas
    validadoresID.clear()
    pesos.clear()

    for v in Validadores:
        if v.id != v1 and v.id != v2:
            validadoresID.append(v.id)
            pesos.append(v.percent)

    v3 = random.choices(validadoresID, pesos)[0]
    # limpa as listas
    validadoresID.clear()
    pesos.clear()
    for v in Validadores:
        if v.id != v1 and v.id != v2 and v.id != v3:
            validadoresID.append(v.id)
            pesos.append(v.percent)

    escolhidos = [v1, v2, v3]

    return escolhidos

def adicionar_flag(id):
    validadorObjeto = Validador.query.filter_by(id=id).first()
    db.session.commit()
    validadorObjeto.flag += 1
    db.session.commit()
    # Verifica quantas flags tem caso flags > 2 ele é deletado
    verifica_qtd_flags(id)

def tirar_flag(id):
    validadorObjeto = Validador.query.filter_by(id=id).first()
    db.session.commit()
    # ---------------------------------------------ARRUMAR 10000 TRANSACOES------------------------------------------
    if validadorObjeto.flag > 0 and validadorObjeto.transacoes >= 10 * validadorObjeto.aux_flag:
        validadorObjeto.flag -= 1
        validadorObjeto.aux_flag += 1
        db.session.commit()

def verifica_qtd_flags(id):
    validadorObjeto = Validador.query.filter_by(id=id).first()
    db.session.commit()
    if validadorObjeto.flag > 2:
        objeto = Validador.query.get(id)
        db.session.delete(objeto)
        db.session.commit()

def adicionar_transacao(id):
    validadorObjeto = Validador.query.filter_by(id=id).first()
    db.session.commit()
    validadorObjeto.transacoes += 1
    db.session.commit()