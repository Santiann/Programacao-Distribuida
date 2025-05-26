from app import db
from dataclasses import dataclass

@dataclass
class Seletor(db.Model):
    id: int
    nomeSeletor: str
    ipSeletor: str

    id = db.Column(db.Integer, primary_key=True)
    nomeSeletor = db.Column(db.String(20), unique=False, nullable=False)
    ipSeletor = db.Column(db.String(20), unique=False, nullable=False)