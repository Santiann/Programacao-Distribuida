from app.models.Seletor import Seletor
from app import db

def listar_seletores():
    return Seletor.query.all()

def inserir_seletor(nome, ip):
    novo = Seletor(nomeSeletor=nome, ipSeletor=ip)
    db.session.add(novo)
    db.session.commit()
    return novo

def buscar_seletor_por_id(id):
    return Seletor.query.get(id)

def editar_seletor(id, nome, ip):
    seletor = Seletor.query.filter_by(id=id).first()
    if seletor:
        seletor.nomeSeletor = nome
        seletor.ipSeletor = ip
        db.session.commit()
    return seletor

def deletar_seletor(id):
    seletor = Seletor.query.get(id)
    if seletor:
        db.session.delete(seletor)
        db.session.commit()
        return True
    return False
