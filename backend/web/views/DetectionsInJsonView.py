from io import BytesIO

import PIL
from PIL import Image
from aiohttp.web_exceptions import HTTPBadRequest

from backend.detectors import DETECTOR_RESULT_LABEL_NAMES, DETECTOR_RESULT_BOXES
from backend.web.views.AbstractAuthorizedPostView import AbstractAuthorizedPostView


class DetectionsInJsonView(AbstractAuthorizedPostView):
    """
    Detection as a json data.
    Gets a picture in request and returns json-data with coordinates of detected objects bounding boxes,
    names of detected classes and probabilities of these classes in response.
    """
    async def _process_authorized(self):
        from backend.web import json_response
        try:
            async for obj in (await self.request.multipart()):
                if obj.filename:
                    raw_io = BytesIO(await obj.read())
                    image = Image.open(raw_io)
                    detection_results = await self.request.app.accessor_to_detector.detect(image, markup_image=False)
                    if detection_results is None:
                        return json_response(status="warning", data="There are no any dogs or cats on the photo.")
                    return json_response(data={
                        "boxes": [
                            [coord.item() for coord in box] for box in detection_results[DETECTOR_RESULT_BOXES]["boxes"]
                        ],
                        "labels": [label for label in detection_results[DETECTOR_RESULT_LABEL_NAMES]],
                        "probabilities": [score.item() for score in detection_results[DETECTOR_RESULT_BOXES]["scores"]],
                    })
        except PIL.UnidentifiedImageError:
            raise HTTPBadRequest(reason="Unknown image format. Probably it is not an image.")
        except KeyError:
            raise HTTPBadRequest(reason="Image is absent.")
