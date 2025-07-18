"""
Реализуйте lru_cache декоратор.
Требования:

Декоратор должен кешировать результаты вызовов функции на основе её аргументов.
Если функция вызывается с теми же аргументами, что и ранее, возвращайте результат из кеша вместо
повторного выполнения функции.
Декоратор должно быть возможно использовать двумя способами: с указанием максимального кол-ва элементов и без.
"""

import unittest.mock
from collections import OrderedDict


def lru_cache(*args, **kwargs):
    def decorator(func):
        maxsize = kwargs.get("maxsize")
        cache = OrderedDict()

        def wrapper(*deco_args, **deco_kwargs):
            key = (deco_args, frozenset(deco_kwargs.items()))
            if key in cache:
                cache.move_to_end(key)
                return cache[key]
            result = func(*deco_args, **deco_kwargs)
            cache[key] = result

            if maxsize and maxsize < len(cache):
                cache.popitem(last=False)

            return result

        return wrapper

    if len(args) == 1 and callable(args[0]):
        return decorator(args[0])
    return decorator


@lru_cache
def sum(a: int, b: int) -> int:
    return a + b


@lru_cache
def sum_many(a: int, b: int, *, c: int, d: int) -> int:
    return a + b + c + d


@lru_cache(maxsize=3)
def multiply(a: int, b: int) -> int:
    return a * b


if __name__ == "__main__":
    assert sum(1, 2) == 3
    assert sum(3, 4) == 7

    assert multiply(1, 2) == 2
    assert multiply(3, 4) == 12

    assert sum_many(1, 2, c=3, d=4) == 10

    mocked_func = unittest.mock.Mock()
    mocked_func.side_effect = [1, 2, 3, 4]

    decorated = lru_cache(maxsize=2)(mocked_func)
    assert decorated(1, 2) == 1
    assert decorated(1, 2) == 1
    assert decorated(3, 4) == 2
    assert decorated(3, 4) == 2
    assert decorated(5, 6) == 3
    assert decorated(5, 6) == 3
    assert decorated(1, 2) == 4
    assert mocked_func.call_count == 4
