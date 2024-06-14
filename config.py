import os
import sys
import loguru
import pretty_errors
import json

from aiogram import *
from aiogram.enums import *
from aiogram.filters import *
from aiogram.types import *
from aiogram.utils.markdown import *
from loguru import *


config_file = 'config.json'

KWORK_URL = 'https://kwork.ru/projects'

with open(config_file, 'r') as f:
    config = json.load(f)

log_file = config["log_file"]
whitelist = config["whitelist"]
kwork_login = config['kwork_login']
kwork_password = config['kwork_password']
TOKEN = config['bot_token']
CATEGORIES = config['categories']

global user_id

bot = Bot(TOKEN)
dp = Dispatcher()

logger = loguru.logger

logger.level("DEBUG", color="<green>")
logger.level("INFO", color="<cyan>")
logger.level("WARNING", color="<yellow>")
logger.level("CRITICAL", color="<red>")

logger.add(
    log_file,
    level="DEBUG",
    rotation="1000 MB",
    retention="31 days",
    backtrace=True,
    diagnose=True,
)