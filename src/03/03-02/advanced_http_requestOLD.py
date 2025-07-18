"""
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
"""

import asyncio
import json
import os
from datetime import datetime
from typing import Any

from aiohttp import ClientError, ClientSession

semaphore = asyncio.Semaphore(5)


async def read_urls(file_path: str) -> list[str]:
    with open(file_path, "r", encoding="utf-8") as f:
        return [line for line in f]


async def save_results(result: list, file_path: str):
    with open(file_path, "w", encoding="utf-8") as f:
        for res in result:
            f.write(json.dumps(res, ensure_ascii=False))


async def fetch_url(session: ClientSession, url: str) -> (str, dict[str, list]):
    try:
        async with semaphore:
            async with session.get(
                url,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
            ) as response:
                content = {
                    "status": response.status,
                    # "headers": dict(response.headers),
                    # "content_type": response.content_type,
                    # 'text': await response.text(),
#                     "url": str(response.url),
#                     "history": [str(r.url) for r in response.history],
#                     "version": response.version,
                }
                return {
                    "url": url,
                    "content": content,
                }
    except (ClientError, asyncio.TimeoutError, json.JSONDecodeError) as e:
        return {
            "url": url,
            "error": str(e),
        }





async def fetch_urls(in_file: str, out_file: str) -> list[dict[str, Any]]:
    urls = await read_urls(in_file)
    results = []

    queue = asyncio.Queue()


    for url in urls:
        await queue.put(url)

    async def worker(worker_session):
        while not queue.empty():
            worker_url = await queue.get()
            res = await fetch_url(worker_session, worker_url)
            results.append(res)
            queue.task_done()

    # async with aiohttp.ClientSession() as session:
    #     workers = [asyncio.create_task(worker(session)) for _ in range(5)]
    #     await queue.join()
    #     for w in workers:
    #         w.cancel()
    #     await asyncio.gather(*workers, return_exceptions=True)

    if results:
        await save_results(results, out_file)
    return results


async def main():
    input_file = "urls.txt"
    output_file = "results.json"

    if os.path.exists(output_file):
        os.remove(output_file)

    await fetch_urls(input_file, output_file)


if __name__ == "__main__":
    start_time = datetime.now()
    asyncio.run(main())
    end_time = datetime.now()
    print((end_time - start_time).total_seconds())
