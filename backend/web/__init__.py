import json
from io import BytesIO
from typing import Any, Optional
from PIL.Image import Image

from aiohttp.web import (
    run_app as aiohttp_run_app,
    json_response as aiohttp_json_response,
    middleware
)
from aiohttp.web_response import Response
from aiohttp.web_exceptions import HTTPException, HTTPUnprocessableEntity
from aiohttp_session import setup as setup_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aiohttp_apispec import setup_aiohttp_apispec, validation_middleware

from backend.accessors import setup_accessors
from backend.web.Application import Application
from backend.web.config import setup_config
from backend.web.routes import setup_routes


HTTP_ERROR_CODES = {
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    405: "not_implemented",
    409: "conflict",
    500: "internal_server_error",
}


def json_response(data: Any = None, status: str = "ok") -> Response:
    if data is None:
        data = {}
    return aiohttp_json_response(data={
        "status": status,
        "data": data
    })


def error_json_response(
        http_status: int, status: str = "error", message: Optional[str] = None, data: Optional[dict] = None
):
    if data is None:
        data = {}
    return aiohttp_json_response(
        status=http_status,
        data={
            "status": status,
            "message": str(message),
            "data": data
        }
    )


def jpeg_response(image: Image) -> Response:
    stream = BytesIO()
    image.save(stream, "JPEG")
    return Response(body=stream.getvalue(), content_type="image/jpeg")


@middleware
async def error_handling_middleware(request, handler):
    try:
        response = await handler(request)
        return response
    except HTTPUnprocessableEntity as e:
        return error_json_response(
            http_status=400,
            status="bad_request",
            message=e.reason,
            data=json.loads(e.text),
        )
    except HTTPException as e:
        return error_json_response(
            http_status=e.status,
            status=HTTP_ERROR_CODES[e.status] if e.status in HTTP_ERROR_CODES.keys() else "bad request",
            message=str(e)
        )
    except Exception as e:
        return error_json_response(
            http_status=500,
            status=HTTP_ERROR_CODES[500],
            message=str(e)
        )


def setup_middlewares(app: Application):
    app.middlewares.append(error_handling_middleware)
    app.middlewares.append(validation_middleware)


def run_app(app: Application, config_path: str):
    setup_config(app, config_path)
    setup_session(app, EncryptedCookieStorage(app.config.session.key))
    setup_routes(app)
    setup_aiohttp_apispec(app, title="Object detection project for DLS", url="/docs/json", swagger_path="/docs")
    setup_middlewares(app)
    setup_accessors(app)
    aiohttp_run_app(app)
