import requests

def hora_sistema():
    url = 'http://127.0.0.1:5000/hora'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f'Erro ao obter hora: {e}')
    return None
