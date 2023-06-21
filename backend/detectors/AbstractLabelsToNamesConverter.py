from abc import ABC, abstractmethod
import numpy


class AbstractLabelsToNamesConverter(ABC):
    def __call__(self, labels: numpy.array) -> list[str]:
        return self.convert(labels)

    @abstractmethod
    def convert(self, labels: numpy.array) -> list[str]:
        raise NotImplementedError
