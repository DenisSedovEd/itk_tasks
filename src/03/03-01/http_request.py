"""
Задача - Асинхронный HTTP-запрос
Напишите асинхронную функцию fetch_urls, которая принимает список URL-адресов и возвращает словарь,
где ключами являются URL, а значениями — статус-коды ответов. Используйте библиотеку aiohttp для выполнения HTTP-запросов.

Требования:
Ограничьте количество одновременных запросов до 5 (используйте примитивы синхронизации из asyncio библиотеки)
Обработайте возможные исключения (например, таймауты, недоступные ресурсы) и присвойте соответствующие
статус-коды (например, 0 для ошибок соединения).
Сохраните все результаты в файл
"""

import asyncio
import json

import aiohttp
from aiohttp import ClientError, ClientTimeout

urls = [
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://google.com",
    "https://sde-resume.ru",
]

semaphore = asyncio.Semaphore(5)


async def fetch(session: aiohttp.ClientSession, url: str) -> (str, int):
    try:
        async with semaphore:
            async with session.get(url, timeout=ClientTimeout(total=10)) as response:
                print(response.status)
                return url, response.status
    except (ClientError, asyncio.TimeoutError):
        return url, 1
    except Exception:
        return url, 0


def save_result(data: dict[str, int], out_file: str) -> None:
    with open(out_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


async def fetch_urls(urls_list: list[str], file_path: str) -> dict[str, int]:
    result = {}
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls_list]
        for task in asyncio.as_completed(tasks):
            url, status = await task
            result[url] = status
    save_result(result, file_path)
    return result


if __name__ == "__main__":
    asyncio.run(fetch_urls(urls, "./results.json"))
