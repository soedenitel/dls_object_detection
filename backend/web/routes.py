import typing

from backend.web.views.DetectionsInJsonView import DetectionsInJsonView
from backend.web.views.EnterView import EnterView
from backend.web.views.LoginView import LoginView
from backend.web.views.PromptDetectionsInJsonView import PromptDetectionsInJsonView
from backend.web.views.PromptDetectionsInJpegView import PromptDetectionsInJpegView
from backend.web.views.DetectionsInJpegView import DetectionsInJpegView
if typing.TYPE_CHECKING:
    from backend.web.Application import Application


def setup_routes(app: "Application"):
    app.router.add_view("/", EnterView)
    app.router.add_view("/login", LoginView)

    app.router.add_view("/launch_detect_to_jpeg", PromptDetectionsInJpegView)
    app.router.add_view("/detect_to_jpeg", DetectionsInJpegView)

    app.router.add_view("/launch_detect_to_json", PromptDetectionsInJsonView)
    app.router.add_view("/detect_to_json", DetectionsInJsonView)
