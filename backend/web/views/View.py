import typing

from aiohttp.web import View as aiohttp_View
if typing.TYPE_CHECKING:
    from backend.web.Request import Request


class View(aiohttp_View):
    @property
    def request(self) -> "Request":
        return super(View, self).request
