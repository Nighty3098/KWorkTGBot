from bs4 import BeautifulSoup
from bs4 import *
import asyncio
import aiohttp

from config import *


async def search_new_projects():
    logger.debug("Parsing")
    async with aiohttp.ClientSession() as session:
        async with session.get(KWORK_URL) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            projects = soup.find_all('div', {'class': 'project-card'})
            new_projects = []
            for project in projects:
                category = int(project.find('span', {'class': 'category'}).text.strip())
                if category in CATEGORIES:
                    title = project.find('h2', {'class': 'title'}).text.strip()
                    link = project.find('a', {'class': 'link'})['href']
                    price = project.find('span', {'class': 'price'}).text.strip()
                    new_projects.append((title, link, price))
            return new_projects

async def send_new_projects(user_id, new_projects):
    for title, link, price in new_projects:
        logger.info(f"New project: {title}")
        await bot.send_message(user_id, f'New project: {title}\nPrice: {price}\n{link}')

async def update_projects(user_id):
    await bot.send_message(user_id, "Parsing...")
    while True:
        new_projects = await search_new_projects()
        if new_projects:
            await send_new_projects(user_id, new_projects)
        await asyncio.sleep(5)
