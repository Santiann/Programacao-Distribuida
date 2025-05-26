from datetime import datetime

def validar_transacao(id, valorRem, valorTrans, horario_str):
    agora = datetime.now()
    horario = datetime.strptime(horario_str, '%Y-%m-%d %H:%M:%S.%f')

    if valorRem >= valorTrans and horario <= agora:
        return {'id': id, 'status': 1}  # APROVADA
    else:
        return {'id': id, 'status': 2}  # REJEITADA
