from random import choice, randint
from threading import Thread

import requests
from requests import get, post
from config import *

async def generate_proxy():
    try:
        proxy = get(
            "https://gimmeproxy.com/api/getProxy?curl=true&protocol=http&supportsHttps=true"
        ).text
        return {proxy}
    except Exception as err:
        logger.error(f"{err}")
