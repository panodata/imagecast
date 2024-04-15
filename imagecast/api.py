# -*- coding: utf-8 -*-
# (c) 2020-2021 Andreas Motl <andreas@terkin.org>
# License: GNU Affero General Public License, Version 3
import logging
import sys
from dataclasses import dataclass
from functools import lru_cache
from typing import List
from urllib.parse import urlparse

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse, PlainTextResponse, Response
from PIL import Image
from pydantic_settings import BaseSettings
from starlette.status import HTTP_403_FORBIDDEN

from imagecast import __appname__, __version__
from imagecast.core import process


if sys.version_info < (3, 9):
    from typing_extensions import Annotated
else:
    from typing import Annotated


# https://fastapi.tiangolo.com/advanced/settings/
class Settings(BaseSettings):
    allowed_hosts: List[str] = []


@lru_cache
def get_settings():
    return Settings()


app = FastAPI()

log = logging.getLogger(__name__)


# Using pydantic models for GET request query params.
# https://github.com/tiangolo/fastapi/issues/318#issuecomment-584020926
@dataclass
class QueryOptions:
    uri: str = Query(default=None)
    element: str = Query(default=None)
    monochrome: int = Query(default=None)
    grayscale: bool = Query(default=False)
    crop: str = Query(default=None)
    width: int = Query(default=None)
    height: int = Query(default=None)
    dpi: int = Query(default=72)
    format: str = Query(default=None)
    cache_ttl: int = Query(default=300)


@app.get("/")
def index(settings: Annotated[Settings, Depends(get_settings)], options: QueryOptions = Depends(QueryOptions)):
    appname = f"{__appname__} {__version__}"
    about = "Imagecast is like ImageMagick but for Pythonistas. Optionally provides its features via HTTP API."

    if options.uri:

        # Protect the service from accessing arbitrary remote URIs.
        uri_parsed = urlparse(options.uri.encode("utf-8"))
        remote_host = uri_parsed.hostname.decode()
        if (
            "*" not in settings.allowed_hosts
            and remote_host not in settings.allowed_hosts
        ):
            raise HTTPException(status_code=HTTP_403_FORBIDDEN)

        # Mogrify image.
        ie = process(options)

        # Determine output format.
        options.format = options.format or ie.format
        if options.format == "bytes":
            buffer = ie.to_bytes()
        else:
            buffer = ie.to_buffer(options.format, options.dpi)

        # Determine content type.
        mime_type = Image.MIME.get(options.format.upper())
        if mime_type is None:
            mime_type = "application/octet-stream"

        return Response(buffer, media_type=mime_type)

    else:
        return HTMLResponse(
            f"""
        <html>
            <head>
                <title>{appname}</title>
            </head>
            <body>
                <h3>About</h3>
                {about}
                <h3>Examples</h3>
                <ul>
                <li><a href="?uri=https%3A%2F%2Funsplash.com%2Fphotos%2FWvdKljW55rM%2Fdownload%3Fforce%3Dtrue&monochrome=80&crop=850,1925,-950,-900&width=640&format=png">Unsplash example</a></li>
                </ul>
            </body>
        </html>
        """
        )


@app.get("/robots.txt", response_class=PlainTextResponse)
def robots():
    return f"""
User-agent: *
Disallow: /
    """.strip()


def start_service(listen_address, reload: bool = False):
    host, port = listen_address.split(":")
    port = int(port)
    from uvicorn.main import run

    run(app="imagecast.api:app", host=host, port=port, reload=reload)
