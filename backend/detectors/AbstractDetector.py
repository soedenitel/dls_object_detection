from abc import ABC, abstractmethod
from typing import Optional

from PIL.Image import Image

from backend.detectors.AbstractLabelsToNamesConverter import AbstractLabelsToNamesConverter


class AbstractDetector(ABC):
    def __init__(
            self,
            labels_to_names_converter: AbstractLabelsToNamesConverter,
            probability_threshold: float,
            labels_threshold: tuple[str],
    ):
        self.__probability_threshold: float = probability_threshold if 0 <= probability_threshold <= 1 else 0.6
        self.__labels_threshold: set[str] = set(labels_threshold)
        self.__labels_to_names_converter: AbstractLabelsToNamesConverter = labels_to_names_converter

    @abstractmethod
    def process(self, picture: Image, markup_image: bool = True) -> Optional[tuple[dict, Optional[Image], list]]:
        """
        Detect object on the source image
        :param picture:source image
        :param markup_image: do or not graphical markup on the source image
        :return: tuple[result dictionary, the source image with Bounding Boxes, detected class names]
        """
        raise NotImplementedError

    @property
    def _labels_to_names_converter(self) -> AbstractLabelsToNamesConverter:
        return self.__labels_to_names_converter

    @property
    def _probability_threshold(self) -> float:
        return self.__probability_threshold

    @property
    def _labels_threshold(self) -> set[str]:
        return self.__labels_threshold

    def __call__(self, picture: Image, markup_image: bool = True) -> Optional[tuple[dict, Optional[Image], list]]:
        return self.process(picture, markup_image)
