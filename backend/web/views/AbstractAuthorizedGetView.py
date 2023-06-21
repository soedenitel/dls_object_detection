from abc import abstractmethod

from backend.web.views.AbstractAuthorizedPostView import AbstractAuthorizedPostView


class AbstractAuthorizedGetView(AbstractAuthorizedPostView):
    async def get(self):
        await self._check_authorization()
        return await self._process_authorized()

    @abstractmethod
    async def _process_authorized(self):
        raise NotImplementedError

    async def post(self):
        raise PermissionError
