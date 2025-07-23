"""
Задача - Ограничитель скорости (rate limiter)
Ваше приложение делает HTTP запросы в сторонний сервис (функция make_api_request), при этом сторонний сервис имеет
проблемы с производительностью и ваша задача ограничить количество запросов к этому сервису - не больше пяти запросов
за последние три секунды. Ваша задача реализовать RateLimiter.test метод который:

возвращает True в случае если лимит на кол-во запросов не достигнут
возвращает False если за последние 3 секунды уже сделано 5 запросов.
Ваша реализация должна использовать Redis, т.к. предполагается что приложение работает на нескольких серверах.
"""

import random
import time

import redis
import requests


class RateLimitExceed(Exception):
    pass


class RateLimiter:
    def __init__(self, redis_host: str = "localhost", redis_port: int = 6379):
        self.redis = redis.Redis(host=redis_host, port=redis_port, db=0)
        self.key = "rate_limiter"
        self.time_limin = 3
        self.count = 5

    def test(self) -> bool:
        current_time = int(time.time())

        timestamps = self.redis.lrange(self.key, 0, -1)
        timestamps = [int(ts) for ts in timestamps]

        cutoff_time = current_time - self.time_limin
        timestamps = [ts for ts in timestamps if ts > cutoff_time]

        self.redis.delete(self.key)
        for ts in timestamps:
            self.redis.rpush(self.key, ts)

        if len(timestamps) < self.count:
            self.redis.rpush(self.key, current_time)
            return True
        else:
            return False


def make_api_request(rate_limiter: RateLimiter):
    if not rate_limiter.test():
        raise RateLimitExceed
    else:
        request = requests.get("https://google.cm")
        return request


if __name__ == "__main__":
    rate_limiter = RateLimiter()

    for _ in range(20):
        time.sleep(random.randint(1, 2))

        try:
            make_api_request(rate_limiter)
        except RateLimitExceed:
            print("Rate limit exceed!")
        else:
            print("All good")
