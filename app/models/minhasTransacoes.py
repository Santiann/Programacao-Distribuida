from app import db
from dataclasses import dataclass

@dataclass
class minhasTransacoes(db.Model):
    id: int
    idTransacao: int
    fCoins: int
    idValidadores: str
    status: int
    RValidadores: int

    id = db.Column(db.Integer, primary_key=True)
    idTransacao = db.Column(db.Integer, unique=True, nullable=False)
    RValidadores = db.Column(db.Integer, unique=False, nullable=False)
    status = db.Column(db.Integer, unique=False, nullable=False)
    fCoins = db.Column(db.Integer, unique=False, nullable=False)
    idValidadores = db.Column(db.String(50), unique=False, nullable=False)