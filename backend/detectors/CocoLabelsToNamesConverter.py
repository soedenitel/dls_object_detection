import numpy
from pycocotools.coco import COCO
from backend.detectors.AbstractLabelsToNamesConverter import AbstractLabelsToNamesConverter


class CocoLabelsToNamesConverter(AbstractLabelsToNamesConverter):
    def __init__(self, path_to_annotations_json: str):
        self.__coco = COCO(path_to_annotations_json)

    def convert(self, labels: numpy.array) -> list[str]:
        return [label["name"] for label in self._coco.loadCats(labels)]

    @property
    def _coco(self) -> COCO:
        return self.__coco
