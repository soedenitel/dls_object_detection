from io import BytesIO
import PIL
from PIL import Image
from aiohttp.web_exceptions import HTTPBadRequest

from backend.detectors import DETECTOR_RESULT_IMAGE
from backend.web.views.AbstractAuthorizedPostView import AbstractAuthorizedPostView


class DetectionsInJpegView(AbstractAuthorizedPostView):
    """
    Detection as a photo's markup.
    Gets a picture in request and returns one with detected objects bounding boxes in response.
    """
    async def _process_authorized(self):
        from backend.web import json_response, jpeg_response
        try:
            async for obj in (await self.request.multipart()):
                if obj.filename:
                    raw_io = BytesIO(await obj.read())
                    image = Image.open(raw_io)
                    detection_results = await self.request.app.accessor_to_detector.detect(image)
                    if detection_results is None:
                        return json_response(status="warning", data="There are no any dogs or cats on the photo.")
                    return jpeg_response(detection_results[DETECTOR_RESULT_IMAGE])
        except PIL.UnidentifiedImageError:
            raise HTTPBadRequest(reason="Unknown image format. Probably it is not an image.")
        except KeyError:
            raise HTTPBadRequest(reason="Image is absent.")
