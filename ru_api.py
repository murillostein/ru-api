import pandas as pd
import requests
from bs4 import BeautifulSoup

import nest_asyncio
nest_asyncio.apply()

from llama_parse import LlamaParse

import smtplib
from email.mime.text import MIMEText


def get_meals_file(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    cardapios_disponiveis = soup.find_all("div", attrs={'class':"content clearfix"})
    for cardapio in cardapios_disponiveis:
        cardapio_semana_atual = cardapio.find_all('li')[0]
        link = cardapio_semana_atual.find_all('a', href=True)[0]
     #   print(link['href'])
        link_cardapio = link['href']
    #print(response.status_code)

    return response.status_code, link_cardapio


def download_pdf(link, name_cardapio_atual):
    response = requests.get(link, verify=False)
    
    with open(name_cardapio_atual, 'wb') as f:
        f.write(response.content)
     

def parse_pdf(name_cardapio_atual):
    parser = LlamaParse(
        api_key="llx-WDHUAm3jYPuEmfOU4JYIkuhr5lnfXjy13pEHc98E3Te5u5td",  # can also be set in your env as LLAMA_CLOUD_API_KEY
        result_type="markdown",  # "markdown" and "text" are available
        num_workers=4, # if multiple files passed, split in `num_workers` API calls
        verbose=True,
        language="pt" # Optionaly you can define a language, default=en
    )
    #
    documents = parser.load_data(name_cardapio_atual)

    # send email
    cardapio_semanal = documents[0].text.split("\n")[2:7]
    cardapio_hoje = cardapio_semanal[2].encode('utf-8')
    return cardapio_hoje

def send_email(sender, receiver, content):
    
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = 'Cardapio quarta feira'
    msg['From'] = sender
    msg['To'] = receiver
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, 'ohmk abqz fudq vyel')
    server.send_message(msg)


# ler o pdf e fazer download
url = 'https://ru.ufsc.br/ru/'

status_code, link_cardapio = get_meals_file(url)
if status_code==200:
    name_cardapio_atual = 'cardapio_atual.pdf'
    download_pdf(link_cardapio, name_cardapio_atual)
    cardapio_hoje = parse_pdf(name_cardapio_atual)

    email = 'murillo.stein8@gmail.com'
    receiver_email = email
    send_email(email, receiver_email, cardapio_hoje)