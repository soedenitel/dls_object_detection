from hashlib import sha256

import aiofiles
import aiohttp_session
from aiohttp.web_exceptions import HTTPForbidden
from aiohttp_apispec import docs, request_schema, response_schema
from aiohttp.web_response import Response

from backend.web.views.View import View
from backend.web.views.schemes import LoginSchema, OkResponseSchema


class LoginViewDemo(View):
    @docs(
        tags=["Main api"],
        summary="Login user.",
        description="Process authorization for user credentials."
    )
    @request_schema(LoginSchema)
    @response_schema(OkResponseSchema, 200)
    async def post(self):
        data = self.request["data"]

        if data["login"] != self.request.app.config.authorization.login:
            raise HTTPForbidden
        if self.request.app.config.authorization.password != sha256(data["password"].encode()).hexdigest():
            raise HTTPForbidden

        session = await aiohttp_session.new_session(self.request)
        config = self.request.app.config
        session["primary_key"] = {"secondary_key": config.authorization.login + config.session.launcher_token}

        async with aiofiles.open(self.request.app.path_to_demo_html, mode="r") as html_file:
            html = await html_file.read()
            return Response(text=html, content_type="text/html")
