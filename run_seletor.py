from app.models.MeuSeletor import MeuSeletor
from app import create_app, db

app = create_app()

def inicializar_seletor():
    if not MeuSeletor.query.filter_by(id=1).first():
        seletor = MeuSeletor(fCoins=0, qtd_transacoes=0)
        db.session.add(seletor)
        db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        inicializar_seletor()
    app.run(host="0.0.0.0", port=5001, debug=True)
