from app import db
from dataclasses import dataclass

@dataclass
class Validador(db.Model):
    id: int
    nome: str
    ip: str
    flag: int
    FCoins: int
    percent: int
    transacoes: int
    aux_flag: int

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), nullable=False)
    ip = db.Column(db.String(50), nullable=False)
    flag = db.Column(db.Integer, nullable=False)
    FCoins = db.Column(db.Integer, nullable=False)
    percent = db.Column(db.Integer, nullable=False)
    transacoes = db.Column(db.Integer, nullable=False)
    aux_flag = db.Column(db.Integer, nullable=False)
