"""
разработайте программу, которая выполняет следующие шаги:
Сбор данных:
Создайте функцию generate_data(n), которая генерирует список из n случайных целых чисел в диапазоне от 1 до 1000.
Например, generate_data(1000000) должна вернуть список из 1 миллиона случайных чисел.
Обработка данных:
Напишите функцию process_number(number), которая выполняет вычисления над числом. Например, вычисляет факториал числа
или проверяет, является ли число простым. Обратите внимание, что обработка должна быть ресурсоёмкой, чтобы продемонстрировать преимущества мультипроцессинга.
Параллельная обработка:
Используйте модули multiprocessing и concurrent.futures для параллельной обработки списка чисел.
Реализуйте три варианта:
Вариант А: Ипользование пула потоков с concurrent.futures.
Вариант Б: Использование multiprocessing.Pool с пулом процессов, равным количеству CPU.
Вариант В: Создание отдельных процессов с использованием multiprocessing.Process и очередей (multiprocessing.Queue) для передачи данных.
Сравнение производительности:
Измерьте время выполнения для всех вариантов и сравните их с однопоточным (однопроцессным) вариантом. Представьте результаты в виде таблицы или графика.
Сохранение результатов:
Сохраните обработанные данные в файл (например, в формате JSON или CSV).
"""

import concurrent.futures as futures
import json
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing
from random import randint
import math
from datetime import datetime, time


def stopwatch(func):
    def wrapper(*args, **kwargs):
        name = func.__name__
        start = datetime.now()
        result = func(*args, **kwargs)
        end = datetime.now()
        total = (end - start).total_seconds()
        print(f"{name} took {total} seconds")
        return total

    return wrapper


def generate_data(number: int) -> list:
    return [randint(1, 1000) for _ in range(number)]


def process_data(number: int) -> int:
    return math.factorial(number)


# def save_data(result: dict[int:int], file_path: str):
#     with open(file_path, "w", encoding="utf-8") as f:
#         f.write(json.dumps(result, ensure_ascii=False, indent=4) + "\n")


# @stopwatch
def single_process(number: int):
    start = datetime.now()
    data = generate_data(number)
    result = [process_data(num) for num in data]
    end = datetime.now()
    total = (end - start).total_seconds()
    return total


# @stopwatch
def process_multithread(number: int):
    start = datetime.now()
    data = generate_data(number)
    with ThreadPoolExecutor(max_workers=10) as executor:
        result = list(executor.map(process_data, data))
    end = datetime.now()
    total = (end - start).total_seconds()
    return total


# @stopwatch
def process_multiprocess(number: int):
    start = datetime.now()
    data = generate_data(number)
    with ProcessPoolExecutor(max_workers=10) as executor:
        result = list(executor.map(process_data, data))
    end = datetime.now()
    total = (end - start).total_seconds()
    return total


def worker(input_queue: multiprocessing.Queue, output_queue: multiprocessing.Queue):
    while True:
        number = input_queue.get()
        if number is None:
            break
        result = process_data(number)
        output_queue.put((number, result))


# @stopwatch
def process_with_queues(number: int):
    start = datetime.now()
    data = generate_data(number)

    input_queue = multiprocessing.Queue()
    output_queue = multiprocessing.Queue()

    processes = []
    for _ in range(multiprocessing.cpu_count()):
        p = multiprocessing.Process(target=worker, args=(input_queue, output_queue))
        p.start()
        processes.append(p)

    for num in data:
        input_queue.put(num)

    for _ in range(multiprocessing.cpu_count()):
        input_queue.put(None)

    results = {}
    for _ in range(len(data)):
        num, result = output_queue.get()
        results[num] = result

    for p in processes:
        p.join()

    end = datetime.now()
    total = (end - start).total_seconds()
    return total


def save_result(results: dict[str, float]) -> None:
    with open("result.json", "a", encoding="utf-8") as f:
        print(results)
        json.dump(results, f, ensure_ascii=False, indent=4)


# @stopwatch
# def main(n: int):
#     result = {}
#     for numer in generate_data(n):
#         result[numer] = process_data(numer)
#     save_data(result, "result.json")
#     return result


if __name__ == "__main__":
    process_with_queues_res = process_with_queues(1000)
    single_process_res = single_process(1000)
    process_multithread_res = process_multithread(1000)
    process_multiprocess_res = process_multiprocess(1000)
    save_result(
        {
            "process_with_queues": process_with_queues_res,
            "single_process": single_process_res,
            "process_multithread": process_multithread_res,
            "process_multiprocess": process_multiprocess_res,
        }
    )
