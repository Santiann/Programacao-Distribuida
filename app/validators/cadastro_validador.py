import requests
import subprocess
import time
import os

def cadastrar_validador(nome, ip):
    url = f'http://127.0.0.1:5001/validador/{nome}/{ip}/1000'
    response = requests.post(url)
    if response.status_code == 200:
        print(f'{nome} cadastrado com sucesso!')
    else:
        print(f'{nome} falhou ao cadastrar.')

def chamar_validadores():
    for i in range(2, 12):
        nome = f"Validador{str(i).zfill(2)}"
        porta = 5000 + i
        ip = f"127.0.0.1:{porta}"
        # Inicia o validador em background
        subprocess.Popen([
            "python3", "run_validador.py"
        ], env={
            "PORTA": str(porta),
            "VALIDADOR_ID": str(i),
            "MALICIOSO": "1" if i == 10 else "0",  # Ex: id 10 é malicioso
            **dict(os.environ)  # preserva variáveis existentes
        })
        time.sleep(0.5)  # evita race condition no boot

        cadastrar_validador(nome, ip)

if __name__ == "__main__":
    chamar_validadores()