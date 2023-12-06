import gc
import json
from abc import ABC, abstractmethod

import numpy as np

DOUBLE_EPSILON = 1e-6


def double_greater_than_inclusive(val1, val2):
    return (val1 - val2) > -DOUBLE_EPSILON


def double_less_than_inclusive(val1, val2):
    return (val2 - val1) > -DOUBLE_EPSILON


def get_sign(is_sell):
    return -1 if is_sell else 1


class OrderInsertRequest():
    __slots__ = [
        "is_sell",
        "price",
        "volume",
        "traded_volume",
        "close_open_type",
        "is_completed"
    ]

    def __init__(
        self,
        is_sell,
        price,
        volume,
        close_open_type
    ):
        self.is_sell = is_sell
        self.price = price
        self.volume = volume
        self.traded_volume = 0
        self.close_open_type = close_open_type
        self.is_completed = False


class File(ABC):
    @property
    def filename(self):
        return self.__filename

    @filename.setter
    def filename(self, filename):
        self.__filename = filename

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        self.__data = data

    @data.deleter
    def data(self):
        del self.__data

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def dump(self):
        pass

    def purge(self):
        del self.data
        gc.collect()


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.bool_):
            return bool(obj)
        return json.JSONEncoder.default(self, obj)


class JsonFile(File):
    def load(self, custom=None):
        try:
            with open(custom if custom else self.filename) as f:
                self.data = json.load(f)
        except Exception as e:
            print("e={} filename={}".format(e, self.filename))

    def dump(self, custom=None):
        with open(custom if custom else self.filename, "w") as f:
            json.dump(self.data, f, indent=4, sort_keys=True, cls=NumpyEncoder)


class Order:
    def __init__(self, side, volume, price):
        
        # Order direction, usually 0 (buy), 1 (do nothing), or 2 (sell).
        self.side = side  

        # Order quantity: a reasonable quantity must be provided based on the current market information, 
        # otherwise it will not pass through the risk control module.
        self.volume = volume

        # Order price, a reasonable price must be given based on the current market information, 
        # otherwise it will not pass the risk control module.
        self.price = price

    def __str__(self):
        return f"Side: {self.side}, Volume: {self.volume}, Price: {self.price}"
