import requests
from bs4 import BeautifulSoup
import re
import time  # Importe o módulo time para usar o sleep

def ler_numeros_do_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, 'r') as file:
            numeros = file.read().splitlines()
        return numeros
    except FileNotFoundError:
        print(f"O arquivo {nome_arquivo} não foi encontrado.")
        return []

def enviar_solicitacao_post(numero):
    try:
        url = "http://consultaoperadora.com.br/site2015/resposta.php"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/125.0.6422.112 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Origin": "http://consultaoperadora.com.br",
            "Referer": "http://consultaoperadora.com.br/site2015/resposta.php",
        }
        dados = {
            "tipo": "consulta",
            "numero": numero
        }
        response = requests.post(url, headers=headers, data=dados)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            operadora_element = soup.find('span', class_='azul lead', string='Operadora:')
            
            if operadora_element:
                operadora = operadora_element.find_next('span', class_='lead laranja').get_text(strip=True)
                print(f"Número: {numero} | Operadora: {operadora}")
            else:
                print(f"Número: {numero} | Operadora não encontrada na resposta.")
        else:
            print(f"Falha na conexão para o número {numero}. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Ocorreu um erro ao tentar se conectar à URL para o número {numero}: {e}")

def main():
    nome_arquivo = 'numero.txt'
    numeros = ler_numeros_do_arquivo(nome_arquivo)

    for numero in numeros:
        enviar_solicitacao_post(numero)
        time.sleep(20)  # Adiciona um delay de 20 segundos entre as requisições

if __name__ == "__main__":
    main()
