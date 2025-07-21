'''
Задача - Очередь
Реализуйте класс очереди который использует редис под капотом

class RedisQueue:
    def publish(self, msg: dict):
        raise NotImplementedError

    def consume(self) -> dict:
        raise NotImplementedError


if __name__ == '__main__':
    q = RedisQueue()
    q.publish({'a': 1})
    q.publish({'b': 2})
    q.publish({'c': 3})

    assert q.consume() == {'a': 1}
    assert q.consume() == {'b': 2}
    assert q.consume() == {'c': 3}
'''

import redis
import json


class RedisQueue:

    def __init__(self, host='localhost', port=6379, db=0, queue_name='default_queue'):
        self.redis_client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self.queue_name = queue_name


    def publish(self, msg: dict):
        try:
            msg = json.dumps(msg)
            self.redis_client.publish(self.queue_name, msg)
        except Exception as e:
            raise e


    def consume(self) -> dict:
        try:
            msg = self.redis_client.rpop(self.queue_name)
            if msg is None:
                return None
            return json.loads(msg)
        except Exception as e:
            raise e

if __name__ == '__main__':
    q = RedisQueue()
    q.publish({'a': 1})
    q.publish({'b': 2})
    q.publish({'c': 3})

    assert q.consume() == {'a': 1}
    assert q.consume() == {'b': 2}
    assert q.consume() == {'c': 3}