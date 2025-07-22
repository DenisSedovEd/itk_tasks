'''
Задача - Распределенный лок
У вас есть распределенное приложение работающее на десятках серверах. Вам необходимо написать декоратор single который
гарантирует, что декорируемая функция не исполняется параллельно.

Пример использования:
import time

@single(max_processing_time=datetime.timedelta(minutes=2))
def process_transaction():
    time.sleep(2)
Параметр max_processing_time указывает на максимально допустимое время работы декорируемой функции.
'''
import datetime
import functools
import time

from redis import Redis


class FuncAlreadyRunning(Exception):
    pass


def single(*args, **kwargs):
    def decorator(func):
        max_processing_time = kwargs.get('max_processing_time')
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            redis = Redis(host='localhost', port=6379, db=0, decode_responses=True)
            func_key = f'func_{func.__name__}'
            timeout = int(max_processing_time.total_seconds())
            if redis.set(func_key, 'True', nx=True, ex=timeout):
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    redis.delete(func_key)
            else:
                raise FuncAlreadyRunning(func_key)
        return wrapper
    return decorator


if __name__ == '__main__':
    @single(max_processing_time=datetime.timedelta(minutes=2))
    def process_transaction():
        print("Start processing...")
        time.sleep(3)
        print("Finished!")
        return "OK"




    # Тест
    result = process_transaction()
    print(f"Result: {result}")