import typing

from backend.accessors.AccessorToDetector import AccessorToDetector

if typing.TYPE_CHECKING:
    from backend.web.Application import Application


def setup_accessors(app: "Application"):
    app.accessor_to_detector = AccessorToDetector()
    app.on_startup.append(app.accessor_to_detector.connect)
    app.on_cleanup.append(app.accessor_to_detector.disconnect)
