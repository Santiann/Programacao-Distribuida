from app import db
from dataclasses import dataclass

@dataclass
class MeuSeletor(db.Model):
    id: int
    fCoins: int
    qtd_transacoes: int

    id = db.Column(db.Integer, primary_key=True)
    fCoins = db.Column(db.Integer, unique=False, nullable=False)
    qtd_transacoes = db.Column(db.Integer, unique=False, nullable=False)