import asyncio

from threading import Thread
import pretty_errors
from aiogram import *
from aiogram.enums import *
from aiogram.filters import *
from aiogram.types import *
from aiogram.utils.keyboard import *
from aiogram.utils.markdown import *
from requests.models import *
import requests
import json

import aiohttp
import time
from datetime import time
from config import *
from data.messages import *
from parse import *


@dp.message(CommandStart())
async def start_command(message: Message):
    if not os.path.exists('lastOrder.log'):
        with open('lastOrder.log', 'wt') as file:
            file.write('Start\n')
        logger.debug('File log created!')

    user_id = str(message.from_user.id)

    logger.info(f"User {user_id} started the bot")

    if user_id in whitelist:
        await message.answer(HELLO_MESSAGE)

        threadKwork = Thread(target=await startKwork(user_id))
        threadKwork.start()

    else:
        await message.answer(NO_ACCESS)