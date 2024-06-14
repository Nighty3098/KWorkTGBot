import requests
from bs4 import BeautifulSoup
import lxml

import time

from config import *


def getSoupWithWrite(url):
    req = requests.get(url)
    with open('index.html', 'wt', encoding='utf-8') as file:
        file.write(req.text)
    soup = BeautifulSoup(req.text, 'lxml')
    return soup


def get_last_call():
    with open('lastOrder.log', 'rt') as file:
        last_call = file.read()
    return last_call


def getSoup(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'lxml')
    return soup


def sendNotification(message):
    url = "https://api.telegram.org/bot" + f'{token}'
    method = url + "/sendMessage"

    requests.post(method, data={
        "chat_id": int(id),
        "text": str(message)
    })

def parsKwork(user_id):
    logger.debug(f"Parsing categories")
    for category in CATEGORIES:
        logger.debug(f"Parsing category: {category}")
        url = f'https://kwork.ru/projects?fc={category}'
        soup = getSoup(url)
        find_all_table_with_order = soup.find_all(class_='card__content pb5')
        for item in find_all_table_with_order:
            nameOrder = item.find(class_='wants-card__header-title first-letter breakwords pr250').find('a').get_text()
            urlOrder = item.find(class_='wants-card__header-title first-letter breakwords pr250').find('a').get('href')
            priceOrder = item.find(class_='wants-card__header-price wants-card__price m-hidden').get_text()
            priceNumber = int(priceOrder.replace('Desired budget: up to ', '').replace(' ', '').replace('₽', ''))
            if priceNumber <= int(price):
                log = get_last_call()
                if nameOrder not in log:
                    text = f"""New project on kwork!\n\n{nameOrder}\n\nPrice: {priceOrder};\n\nLink: {urlOrder}
                    """

                    with open('lastOrder.log', 'a') as file:
                        file.write(nameOrder + "\n")

                    bot.send_text(user_id, text)


async def startKwork(user_id):
    logger.debug(f"{user_id}: Starting kwork parse")

    while True:
        try:
            parsKwork(user_id)
            time.sleep(5)
        except requests.exceptions.ConnectionError:
            logger.debug(f"{user_id}: Failed to connect to the session. Check the connection with the Internet.")
            continue
