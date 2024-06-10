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

log_file = "logs/FTB.log"
whitelist = ["1660218648"]
config_file = 'config.json'

with open(config_file, 'r') as f:
    config = json.load(f)

kwork_login = config['kwork_login']
kwork_password = config['kwork_password']
user_id = config['user_id']

TOKEN = config['bot_token']

categories = ['desktop_development', 'software']

kwork_url = 'https://kwork.ru/api/v2/projects'

kwork_headers = {
    'Authorization': f'Basic {kwork_login}:{kwork_password}',
    'Content-Type': 'application/json'
}

last_project_id = 0

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

