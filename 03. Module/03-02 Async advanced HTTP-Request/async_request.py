"""
{"url": "https://example1.com",
"content": {
"any key": "any value",
}
{"url": "https://example2.com", "content": {"key": "value", ...}


"""

import asyncio
import os
from typing import Any

import aiohttp
import json

from aiohttp import ClientSession, ClientError

SEM = asyncio.Semaphore(10)


async def fetch(session: ClientSession, url: str) -> (str, dict[str, Any]):
    try:
        async with SEM:
            async with session.get(url) as response:
                if response.status == 200:
                    content = await response.json()
                    return {"url": url, "content": content}
                else:
                    return {"url": url, "error": f"Status code {response.status}"}

    except (ClientError, asyncio.TimeoutError, json.JSONDecodeError) as e:
        return {"url": url, "error": str(e)}
    except Exception as e:
        return {"url": url, "error": f"Unexpected error: {str(e)}"}


async def read_urls(file_path: str) -> list[str]:
    with open(file_path, "r", encoding="utf-8") as f:
        return [line for line in f]


async def save_results(result: list, file_path: str):
    with open(file_path, "w", encoding="utf-8") as f:
        for res in result:
            f.write(json.dumps(res, ensure_ascii=False) + "\n")


async def fetch_urls(input_file: str, out_file: str):
    urls = await read_urls(input_file)
    results = []

    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        for task in asyncio.as_completed(tasks):
            result = await task
            results.append(result)
            if len(results) >= 50:
                await save_results(results, out_file)

    if results:
        await save_results(results, out_file)


async def main():
    input_file = "urls.txt"
    output_file = "results.jsonl"

    if os.path.exists(output_file):
        os.remove(output_file)

    await fetch_urls(input_file, output_file)


if __name__ == "__main__":
    asyncio.run(main())
