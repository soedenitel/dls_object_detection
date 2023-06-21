from abc import abstractmethod

import aiohttp_session
from aiohttp.web_exceptions import HTTPUnauthorized

from backend.web.views.View import View


class AbstractAuthorizedPostView(View):
    async def post(self):
        await self._check_authorization()
        return await self._process_authorized()

    async def _check_authorization(self):
        session = await aiohttp_session.get_session(self.request)
        if "primary_key" not in session:
            raise HTTPUnauthorized
        if "secondary_key" not in session["primary_key"]:
            raise HTTPUnauthorized

        config = self.request.app.config
        if session["primary_key"]["secondary_key"] != config.authorization.login + config.session.launcher_token:
            raise HTTPUnauthorized

    @abstractmethod
    async def _process_authorized(self):
        raise NotImplementedError
