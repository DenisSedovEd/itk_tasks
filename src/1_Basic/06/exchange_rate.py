"""
Задача - ASGI / WSGI функция которая проксирует курс валют
Приложение должно отдавать курс валюты к доллару используя стороннее АПИ https://api.exchangerate-api.com/v4/latest/{currency}
Например, в ответ на http://localhost:8000/USD должен возвращаться ответ вида:
{"provider":"https://www.exchangerate-api.com","WARNING_UPGRADE_TO_V6":"https://www.exchangerate-api.com/docs/free",
"terms":"https://www.exchangerate-api.com/terms","base":"USD","date":"2024-09-18","time_last_updated":1726617601,
"rates":{"USD":1,"AED":3.67,"AFN":69.45,"ALL":89.49,"AMD":387.39,"ANG":1.79,"AOA":939.8,"ARS":962.42,"AUD":1.48...}

Данные, соответственно, для доллара должны браться из https://api.exchangerate-api.com/v4/latest/USD
Для решения задачи запрещено использовать фреймворки.
"""

import json
import urllib.request
from urllib.error import HTTPError
from wsgiref.simple_server import make_server


def exchange_rate(environ, start_response):
    path = environ.get("PATH_INFO", "").strip("/")

    if len(path) != 3 or not path.isalpha():
        start_response("400 Bad Request", [("Content-Type", "application/json")])
        return [json.dumps({"error": "Invalid currency code"}).encode()]

    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{path}"
        with urllib.request.urlopen(url) as response:
            data = response.read()
            rates = json.loads(data)
            start_response("200 OK", [("Content-Type", "application/json")])
        return [json.dumps(rates).encode()]

    except HTTPError as e:
        start_response(
            f"{e.code} {e.reason}. Rate {path} nof Found.",
            [("Content-Type", "application/json")],
        )
        return [json.dumps({"error": str(e)}).encode()]


if __name__ == "__main__":
    server = make_server("", 8000, exchange_rate)
    print("Сервер запущен на порту 8000")
    server.serve_forever()
