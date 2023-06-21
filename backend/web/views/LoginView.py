from hashlib import sha256

import aiohttp_session
from aiohttp.web_exceptions import HTTPForbidden
from aiohttp_apispec import docs, request_schema, response_schema

from backend.web.views.View import View
from backend.web.views.schemes import LoginSchema, OkResponseSchema


class LoginView(View):
    @docs(
        tags=["Main api"],
        summary="Login user.",
        description="Process authorization for user credentials."
    )
    @request_schema(LoginSchema)
    @response_schema(OkResponseSchema, 200)
    async def post(self):
        from backend.web import json_response
        data = self.request["data"]
        if data["login"] != self.request.app.config.authorization.login:
            raise HTTPForbidden
        if self.request.app.config.authorization.password != sha256(data["password"].encode()).hexdigest():
            raise HTTPForbidden
        session = await aiohttp_session.new_session(self.request)
        config = self.request.app.config
        session["primary_key"] = {"secondary_key": config.authorization.login + config.session.launcher_token}
        return json_response(data={"message": "You are authorized successfully!"})
