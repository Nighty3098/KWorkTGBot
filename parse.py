import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
import lxml

import time

from get_proxy import *
from config import *

def get_last_call():
    with open('lastOrder.log', 'rt') as file:
        last_call = file.read()
    return last_call


def getSoup(url, proxy=None):
    headers = {'User-Agent': generate_user_agent()}
    if proxy:
        proxies = {'http': proxy, 'https': proxy}
        logger.debug(proxies)
        
        response = requests.get(url, headers=headers, proxies=proxies)
    else:
        response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    logger.debug(headers)
    logger.debug(response)

    return soup

def parsKwork(user_id):
    logger.debug(f"Parsing categories")
    for category in CATEGORIES:
        logger.debug(f"Parsing category: {category}")
        url = f'https://kwork.ru/projects?fc={category}'
        soup = getSoup(url)
        logger.debug(soup)
        find_all_table_with_order = soup.find_all(class_='want-card want-card--list want-card--hover')
        for item in find_all_table_with_order:
            textOrder = item.find(class_='wants-card__header-title breakwords pr250').find('a').get_text()
            urlOrder = item.find(class_='wants-card__header-title breakwords pr250').find('a').get('href')
            priceOrder = item.find(class_='d-inline').get_text()
            priceNumber = int(priceOrder.replace('Desired budget: up to ', '').replace(' ', '').replace('₽', ''))
            if priceNumber <= int(price):
                log = get_last_call()
                if textOrder not in log:
                    text = f"""New project on kwork!\n\n{textOrder}\n\nPrice: {priceOrder};"""

                    with open('lastOrder.log', 'a') as file:
                        file.write(textOrder + "\n")

                    keyboard = types.InlineKeyboardMarkup()
                    button = types.InlineKeyboardButton('Open project', url=urlOrder)
                    keyboard.add(button)

                    bot.send_text(user_id, text, reply_markup=keyboard)

async def startKwork(user_id):
    logger.debug(f"{user_id}: Starting kwork parse")

    while True:
        try:
            parsKwork(user_id)
            time.sleep(5)
        except requests.exceptions.ConnectionError:
            logger.debug(f"{user_id}: Failed to connect to the session. Check the connection with the Internet.")
            continue