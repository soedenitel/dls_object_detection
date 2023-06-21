import aiofiles

from aiohttp.web_response import Response

from backend.web.views.AbstractAuthorizedGetView import AbstractAuthorizedGetView


class PromptDetectionsInJsonView(AbstractAuthorizedGetView):
    async def _process_authorized(self):
        async with aiofiles.open(self.request.app.path_to_test_html_prompt_for_json, mode="r") as html_file:
            html = await html_file.read()
            return Response(text=html, content_type="text/html")
