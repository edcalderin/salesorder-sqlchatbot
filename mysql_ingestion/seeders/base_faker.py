from abc import ABC, abstractmethod

from faker import Faker


class BaseFaker(ABC):
    def __init__(self, connection):
        self._size: int = 100
        self._connection = connection
        self._faker = Faker()

    @abstractmethod
    def fill_data(self) -> None:
        raise NotImplementedError()
