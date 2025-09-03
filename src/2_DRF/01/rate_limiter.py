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


class RateLimitExceed(Exception):
    pass


class RateLimiter:
    def __init__(
        self,
        redis_host: str = "localhost",
        redis_port: int = 6379,
        max_requests: int = 5,
        time_window: int = 3,
    ):
        self.redis = redis.Redis(host=redis_host, port=redis_port, db=0)
        self.max_requests = max_requests
        self.time_window = time_window
        self.key_prefix = "rate_limit:"

    def test(self, client_id: str) -> bool:
        key = f"{self.key_prefix}{client_id}"
        current_time = time.time()

        with self.redis.pipeline() as pipe:
            pipe.watch(key)

            pipe.multi()
            pipe.zremrangebyscore(key, 0, current_time - self.time_window)
            pipe.zcard(key)
            _, count = pipe.execute()

            if count < self.max_requests:
                pipe.multi()
                pipe.zadd(key, {f"{current_time}:{time.time_ns()}": current_time})
                pipe.expire(key, self.time_window)
                pipe.execute()
                return True
            return False


def make_api_request(rate_limiter: RateLimiter):
    if not rate_limiter.test("123"):
        raise RateLimitExceed
    else:
        pass


if __name__ == "__main__":
    rate_limiter = RateLimiter()

    for _ in range(50):
        time.sleep(random.randint(1, 2))

        try:
            make_api_request(rate_limiter)
        except RateLimitExceed:
            print("Rate limit exceed!")
        else:
            print("All good")
