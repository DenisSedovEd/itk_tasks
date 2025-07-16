"""
Задача - Синглтон
Реализуйте паттерн синглтон тремя способами:
с помощью метаклассов
с помощью метода __new__ класса
через механизм импортов
"""


# SingleTon metaclass
class SingleTonMeta(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super().__call__(*args, **kwargs)
        return cls._instance[cls]


class SingleTonMetaExemple(metaclass=SingleTonMeta):
    pass


# SingleTon __new__
class SingleTonNew:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super().__new__(cls, *args, **kwargs)


class SingleTonNewExemple(SingleTonNew):
    pass


# SingleTonImport
from singleton_import import singleton

if __name__ == "__main__":
    meta = SingleTonMetaExemple()
    meta1 = SingleTonMetaExemple()
    if meta is meta1:
        print("They are the same object")

    new = SingleTonNewExemple()
    new1 = SingleTonNewExemple()
    if new is new1:
        print("They are the same object")

    imp = singleton
    imp1 = singleton
    if imp is imp1:
        print("They are the same object")
