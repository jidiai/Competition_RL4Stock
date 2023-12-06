
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
