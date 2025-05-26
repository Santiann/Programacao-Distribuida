from app.models.minhasTransacoes import minhasTransacoes
from app.models.MeuSeletor import MeuSeletor
from app import db
from flask import jsonify
from app.models.Validador import Validador
from app.services.validador_service import calcular_percent

def Cadastro_das_Transacoes(idTransacao, fCoins, idValidadores, RValidadores):
    objeto = minhasTransacoes(idTransacao=idTransacao, fCoins=fCoins,
                              idValidadores=idValidadores, status=0, RValidadores=RValidadores)
    db.session.add(objeto)
    db.session.commit()

    return jsonify(objeto)

def verifica_transacao(id):
    Mtransacoes = minhasTransacoes.query.filter_by(idTransacao=id).first()
    meuSeletor = MeuSeletor.query.filter_by(id=1).first()

    if Mtransacoes.RValidadores == Mtransacoes.status and Mtransacoes.status == 1:
        # print('Validadores Acertaram agora vao ganhar a recompensa')
        validadores = Validador.query.all()

        pagamento = Mtransacoes.fCoins * (15 / 100)
        # print(f'O pagamento total foi de: {pagamento}')
        payValidador = pagamento * (8 / 100)

        for v in validadores:
            if str(v.id) in Mtransacoes.idValidadores:
                pagamento -= payValidador
                # print(f'O pagamento V foi de: {payValidador}')
                v.FCoins += payValidador
            else:
                print(f"O valor não está presente na string.")
        # print(f'O pagamento restante foi de: {pagamento}')

        meuSeletor.fCoins += pagamento
        db.session.commit()
        calcular_percent()
    else:
        print('Validadores erraram ')
