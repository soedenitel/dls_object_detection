import typing
from typing import Optional

from PIL.Image import Image

from backend.detectors.FasterRCnnResnet50FpnV2Detector import FasterRCnnResnet50FpnV2Detector

if typing.TYPE_CHECKING:
    from backend.web.Application import Application


class AccessorToDetector(object):
    def __init__(self):
        self.__app: Optional["Application"] = None
        self.__detector: Optional[FasterRCnnResnet50FpnV2Detector] = None

    async def connect(self, app: "Application"):
        self.__app = app
        self.__detector = FasterRCnnResnet50FpnV2Detector()
        print("FasterRCnnResnet50FpnV2Detector is initialized.")

    async def disconnect(self, _: "Application"):
        self.__app = None
        if self.__detector is not None:
            del self.__detector
            self.__detector = None
        print("FasterRCnnResnet50FpnV2Detector was disposed.")

    async def detect(self, image: Image, markup_image: bool = True) -> Optional[tuple[dict, Image]]:
        if self.__detector is None:
            return None
        return self.__detector(image, markup_image)
