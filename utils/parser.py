import logging
import aiohttp
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

async def parse_codewars_profile(url: str) -> list[str]:
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/114.0.0.0 Safari/537.36"
            )
        }

        logger.info(f"Парсим профиль: {url}")

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as response:
                if response.status != 200:
                    logger.warning(f"Ответ {response.status} от Codewars")
                    raise Exception("Ошибка доступа к профилю")
                html = await response.text()

        soup = BeautifulSoup(html, "html.parser")
        blocks = soup.find_all("div", class_="list-item-kata")

        tasks = []
        for block in blocks:
            title_tag = block.find("a", class_="item-title")
            if title_tag:
                task_name = title_tag.text.strip()
                tasks.append(task_name)

        logger.info(f"Найдено задач: {len(tasks)}")
        return tasks

    except Exception as e:
        logger.exception(f"Ошибка при парсинге профиля: {e}")
        raise RuntimeError(f"Ошибка при парсинге профиля: {e}")