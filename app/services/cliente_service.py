from app.models.Cliente import Cliente
from app import db
import requests
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HOST_API = os.getenv("HOST_API", "127.0.0.1")

def listar_clientes():
    return Cliente.query.all()

def inserir_cliente(nome, senha, qtdMoedas):
    novo = Cliente(nome=nome, senha=senha, qtdMoeda=qtdMoedas)
    db.session.add(novo)
    db.session.commit()
    return novo

def buscar_cliente_por_id(id):
    return db.session.get(Cliente, id)

def editar_cliente(id, qtdMoedas):
    cliente = Cliente.query.filter_by(id=id).first()
    if cliente:
        cliente.qtdMoedas = qtdMoedas
        db.session.commit()
    return cliente

def deletar_cliente(id):
    cliente = Cliente.query.get(id)
    if cliente:
        db.session.delete(cliente)
        db.session.commit()
        return True
    return False

def visualizar_Cliente_id(id):
    url = f'http://{HOST_API}:5000/cliente/{id}'
    response = requests.get(url)

    if response.status_code == 200:
        dados = response.json()
        return dados
    else:
        logger.error('Falha ao enviar a mensagem.')
