from abc import ABC, abstractmethod


class BaseFaker(ABC):
    def __init__(self, connection):
        self._size: int = 100
        self._connection = connection

    @abstractmethod
    def fill_data(self) -> None:
        raise NotImplementedError()
