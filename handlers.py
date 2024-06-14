import asyncio

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
    user_id = str(message.from_user.id)

    logger.info(f"User {user_id} started the bot")

    if user_id in whitelist:
        await message.answer(HELLO_MESSAGE)
        await update_projects(user_id)

    else:
        await message.answer(NO_ACCESS)