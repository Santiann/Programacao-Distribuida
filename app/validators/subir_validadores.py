import requests
import subprocess
import time
import os

def subir_validadores():
    try:
        response = requests.get("http://127.0.0.1:5001/validador")
        validadores = response.json()
    except Exception as e:
        print(f"Erro ao consultar seletor: {e}")
        return

    for validador in validadores:
        porta = int(validador['ip'].split(":")[1])
        id_validador = validador['id']
        eh_malicioso = "1" if id_validador == 10 else "0"

        subprocess.Popen([
            "python3", "run_validador.py"
        ], env={
            "PORTA": str(porta),
            "VALIDADOR_ID": str(id_validador),
            "MALICIOSO": eh_malicioso,
            "PYTHONPATH": ".",
            **os.environ
        })
        print(f"Validador {id_validador} iniciado na porta {porta}")
        time.sleep(0.5)

if __name__ == "__main__":
    subir_validadores()
