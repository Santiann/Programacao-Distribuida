import requests
import os

HOST_API = os.getenv("HOST_API", "127.0.0.1")

def hora_sistema():
    url = f'http://{HOST_API}:5000/hora'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f'Erro ao obter hora: {e}')
    return None
