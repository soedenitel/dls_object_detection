import aiofiles

from aiohttp.web_response import Response
from backend.web.views.View import View


class EnterView(View):
    async def get(self):
        async with aiofiles.open(self.request.app.path_to_enter_html, mode="r") as html_file:
            html = await html_file.read()
            return Response(text=html, content_type="text/html")
