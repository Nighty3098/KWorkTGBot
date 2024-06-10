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
    logger.info(f"User {user_id} started the bot")

    await message.answer(HELLO_MESSAGE)

@dp.message(Command("parse"))
async def parse_kwork(message: Message):
    logger.info(f"User {user_id} started parser")

    await message.answer("Starting parsing the data")
