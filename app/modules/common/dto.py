from abc import ABC, abstractmethod


class Dto(ABC):

    @property
    @abstractmethod
    def name(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def api(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def model(self):
        raise NotImplementedError()
