import typing

from aiohttp.web import Request as aiohttp_Request
if typing.TYPE_CHECKING:
    from backend.web.Application import Application


class Request(aiohttp_Request):
    @property
    def app(self) -> "Application":
        return super(Request, self).app()
