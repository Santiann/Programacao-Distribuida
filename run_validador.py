from flask import jsonify, render_template
from app.validators.validador_base import validar_transacao
import os
from app import create_app

app = create_app()

VALIDADOR_ID = int(os.getenv("VALIDADOR_ID", 1))
MALICIOSO = bool(int(os.getenv("MALICIOSO", 0)))

@app.route("/")
def index():
    return render_template("api.html")

@app.route("/validar/<int:id>/<int:valorRem>/<int:valorTrans>/<string:horario>", methods=["POST"])
def validar(id, valorRem, valorTrans, horario):
    if MALICIOSO:
        return jsonify({"id": id, "status": 2})
    return jsonify(validar_transacao(id, valorRem, valorTrans, horario))

@app.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html"), 404

if __name__ == "__main__":
    PORTA = int(os.getenv("PORTA", 5002))
    app.run(host="0.0.0.0", port=PORTA, debug=False, use_reloader=False)