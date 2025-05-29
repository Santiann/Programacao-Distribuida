import requests
import os

HOST_API = os.getenv("HOST_API", "127.0.0.1")

def cadastrar_validador(nome, ip):
    url = f'http://{HOST_API}:5001/validador/{nome}/{ip}/1000'
    response = requests.post(url)
    if response.status_code == 200:
        print(f'{nome} cadastrado com sucesso!')
    else:
        print(f'{nome} falhou ao cadastrar.')

def registrar_validadores():
    for i in range(2, 12):
        nome = f"Validador{str(i).zfill(2)}"
        ip = f"{HOST_API}:{5000 + i}"
        cadastrar_validador(nome, ip)

if __name__ == "__main__":
    registrar_validadores()
