import requests
import subprocess
import time
import os

HOST_API = os.getenv("HOST_API", "127.0.0.1")

def subir_validadores():
    try:
        response = requests.get(f"http://{HOST_API}:5001/validador")
        validadores = response.json()
    except Exception as e:
        print(f"http://{HOST_API}:5001/validador")
        print(f"Erro ao consultar seletor: {e}")
        return

    for validador in validadores:
        porta = int(validador['ip'].split(":")[1])
        id_validador = validador['id']
        eh_malicioso = "1" if id_validador == 10 else "0"

        script_path = os.path.join(
            os.path.dirname(__file__), '..', '..', 'run_validador.py'
        )
        subprocess.Popen([
            "python3", script_path
        ], env={
            "PORTA": str(porta),
            "VALIDADOR_ID": str(id_validador),
            "MALICIOSO": eh_malicioso,
            "PYTHONPATH": os.getcwd(),
            **os.environ
        })
        print(f"Validador {id_validador} iniciado na porta {porta}")
        time.sleep(0.5)

if __name__ == "__main__":
    subir_validadores()
