'''
Задача - Асинхронный HTTP-запрос. Продвинутая реализация.
Напишите асинхронную функцию fetch_urls, которая принимает файл со списком урлов (каждый URL адрес возвращает JSON)
и сохраняет результаты выполнения в другой файл (result.jsonl), где ключами являются URL,
а значениями — распарсенный json, при условии что статус код — 200. Используйте библиотеку aiohttp для выполнения HTTP-запросов.

Требования:
Ограничьте количество одновременных запросов до 5
Обработайте возможные исключения (например, таймауты, недоступные ресурсы) ошибок соединения

Контекст:
Урлов в файле может быть десятки тысяч
Некоторые урлы могут весить до 300-500 мегабайт
При внезапной остановке и/или перезапуске скрипта - допустимо скачивание урлов по новой.
'''

import json
import aiohttp
import asyncio
from typing import Any
from aiohttp import ClientSession

semaphore = asyncio.Semaphore(5)


def reads_urls(file_path: str) -> list[str]:
    with open(file_path, "r", encoding="utf-8") as f:
       return [line for line in f]


def save_file(file_path: str, result: dict[str: Any]) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        for res in result:
            f.write(json.dumps(res, ensure_ascii=False) + "\n")


async def fetch_url(session: ClientSession, url: str) -> (str, dict[str, list]):
    async with session.get(url) as response:
        return url, await response.json()


async def fetch_urls(urls: list[str]) -> dict[str, Any]:
    results = {}
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            tasks = [fetch_url(session, url) for url in urls]
            for task in asyncio.as_completed(tasks):
                url, res = await task
                results[url] = res
    return results


# async def main():
#
#     fetched_data = await fetch_urls(data)


if __name__ == '__main__':
    input_file = 'urls.txt'
    output_file = 'result.json'
    data = reads_urls(input_file)
    fetched_data = asyncio.run(fetch_urls(data))
    save_file(output_file, fetched_data)
