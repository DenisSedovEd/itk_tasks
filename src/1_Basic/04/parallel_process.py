"""
Сравнение различных способов параллельной обработки данных в Python:
- Однопоточный режим
- Пул потоков (ThreadPoolExecutor)
- Пул процессов (ProcessPoolExecutor)
- Ручные процессы с multiprocessing.Queue
"""

import json
import math
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from datetime import datetime
from random import randint


def generate_data(n):
    return [randint(1, 1000) for _ in range(n)]


def process_number(number):
    return math.factorial(number)


def single_process(data):
    start = datetime.now()
    result = [process_number(num) for num in data]
    end = datetime.now()
    return (end - start).total_seconds()


def process_multithread(data):
    start = datetime.now()
    with ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        result = list(executor.map(process_number, data))
    end = datetime.now()
    return (end - start).total_seconds()


def process_multiprocess(data):
    start = datetime.now()
    with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        result = list(executor.map(process_number, data))
    end = datetime.now()
    return (end - start).total_seconds()


def worker(input_queue, output_queue):
    while True:
        number = input_queue.get()
        if number is None:
            break
        output_queue.put(process_number(number))


def process_with_queues(data):
    start = datetime.now()
    input_queue = multiprocessing.Queue()
    output_queue = multiprocessing.Queue()
    processes = []
    for _ in range(multiprocessing.cpu_count()):
        p = multiprocessing.Process(target=worker, args=(input_queue, output_queue))
        p.start()
        processes.append(p)
    for num in data:
        input_queue.put(num)
    for _ in processes:
        input_queue.put(None)
    results = [output_queue.get() for _ in range(len(data))]
    for p in processes:
        p.join()
    end = datetime.now()
    return (end - start).total_seconds()


def save_result(results, filename="result.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)


def main(n):
    data = generate_data(n)
    results = {
        "single_process": single_process(data),
        "process_multithread": process_multithread(data),
        "process_multiprocess": process_multiprocess(data),
        "process_with_queues": process_with_queues(data),
    }
    save_result(results)


if __name__ == "__main__":
    main(10000)
