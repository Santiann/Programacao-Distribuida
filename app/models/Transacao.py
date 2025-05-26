from dataclasses import dataclass
from app import db

@dataclass
class Transacao(db.Model):
    id: int
    remetente: int
    recebedor: int
    valor: int
    status: int
    horario: db.DateTime

    id = db.Column(db.Integer, primary_key=True)
    remetente = db.Column(db.Integer, unique=False, nullable=False)
    recebedor = db.Column(db.Integer, unique=False, nullable=False)
    valor = db.Column(db.Integer, unique=False, nullable=False)
    horario = db.Column(db.DateTime, unique=False, nullable=False)
    status = db.Column(db.Integer, unique=False, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'remetente': self.remetente,
            'recebedor': self.recebedor,
            'valor': self.valor,
            'status': self.status
        }
