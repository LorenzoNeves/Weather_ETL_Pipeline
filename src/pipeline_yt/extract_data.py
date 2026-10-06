import requests
import json
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

#TESTE
# api_key = '1a3b808d735db3709706ceb0613b3776'
# url = f'https://api.openweathermap.org/data/2.5/weather?q=Sao Paulo,BR&units=metric&appid={api_key}'
#=========

def extract_weather_data(url:str) -> list:
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        logging.error('Erro de requisição.')
        return[]

    if not data:
        logging.warning('Nenhum dado retornado.') #ou warn
        return[]

    #criando o caminho das pastas aonde a gnt quer salvar esse arquivo
    output_path = Path(__file__).resolve().parents[2] / 'data' / 'weather_data.json'
    output_dir = Path(output_path).parent #sai da pasta src para procurar a pasta data
    output_dir.mkdir(parents=True, exist_ok=True) #cria pasta para o arquivo json, se existir blz

    #vamos abrir o arquivo que foi gerado
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)#ele vai ler o dicionario e vai escrever

    logging.info(f"Arquivos salvos em {output_path}.")
    return data

# extract_weather_data(url)