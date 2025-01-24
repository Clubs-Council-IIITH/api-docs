from os import getenv, path
import os
import subprocess

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

DEBUG = getenv("BACKEND_DEBUG", "True").lower() in ("true", "1", "t")

if DEBUG:
    app = FastAPI(
        debug=DEBUG,
        title="SLC Tech Documentation",
        description="SLC Tech Documentation System",
    )
else:
    app = FastAPI(
        debug=DEBUG,
        title="SLC Tech Documentation System",
        description="SLC Tech Documentation System",
        docs_url=None,
        redoc_url=None,
    )


# Backend Index Page - For checking purposes
@app.get("/ping", tags=["General"])
async def index():
    return {"message": "Backend Running!!"}


# Host /build directory as static files
if path.exists("/build"):
    app.mount("/", StaticFiles(directory="/build", html=True), name="static")
