import os
from typing import Optional
from aiohttp.web import Application as aiohttp_Application
from backend.accessors.AccessorToDetector import AccessorToDetector
from backend.web.config.Config import Config


class Application(aiohttp_Application):
    accessor_to_detector: Optional[AccessorToDetector] = None
    config: Optional[Config] = None

    @property
    def path_to_enter_html(self) -> str:
        return os.path.join(os.getcwd(), "frontend", "login.html")

    @property
    def path_to_test_html_prompt_for_jpeg(self) -> str:
        return os.path.join(os.getcwd(), "frontend", "detect_for_jpeg.html")

    @property
    def path_to_test_html_prompt_for_json(self) -> str:
        return os.path.join(os.getcwd(), "frontend", "detect_for_json.html")
