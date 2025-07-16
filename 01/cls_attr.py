"""
Задача - Атрибуты класса
Напишите метакласс, который автоматически добавляет атрибут created_at с текущей датой и временем к любому классу,
который его использует.
"""

from datetime import datetime


class MyMeta(type):
    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)
        new_class.created_at = datetime.now()
        return new_class


class Test(metaclass=MyMeta):
    def __init__(self, some_value):
        self.some_value = some_value


if __name__ == "__main__":
    obj = Test("1")
    obj1 = Test("2")
    print(obj.created_at)
    print(obj1.created_at)
