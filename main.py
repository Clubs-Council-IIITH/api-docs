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


@app.post("/update", tags=["Admin"])
async def update1():
    # Git Clone
    result_git = subprocess.run(
        [
            "git",
            "clone",
            "-j8",
            "--recurse-submodules",
            "--remote-submodules",
            "git@github.com:Clubs-Council-IIITH/services.git",
            "/services",
        ],
        capture_output=True,
        text=True,
    )

    # print(result_git)
    returncode = result_git.returncode
    stderr = result_git.stderr

    if returncode != 0 and "already exists" in stderr:
        curr_dir = os.getcwd()
        os.chdir("/services")

        subprocess.run(
            ["git", "pull", "origin", "master"], capture_output=True, text=True
        )

        result_pull = subprocess.run(
            ["git", "submodule", "foreach", "git", "pull", "origin", "master"],
            capture_output=True,
            text=True,
        )

        os.chdir(curr_dir)

        # print(result_pull)
        returncode = result_pull.returncode
        stderr = result_pull.stderr

    if returncode == 0:
        # Run the mkdocs build command
        result = subprocess.run(
            ["mkdocs", "build", "-d", "/build"], capture_output=True, text=True
        )

        # print("Build Result: ", result)

        if result.returncode == 0:
            # If the build is successful, remount the static files
            app.router.routes = [
                route
                for route in app.router.routes
                if not (hasattr(route, "name") and route.name == "static")
            ]
            app.mount("/", StaticFiles(directory="/build", html=True), name="static")
            return {"message": "Update Successful!!"}
        else:
            # If the build fails, return the error
            return JSONResponse(
                content={"error": "Build failed", "details": result.stderr},
                status_code=500,
            )
    else:
        # If the git clone fails, return the error
        return JSONResponse(
            content={"error": "Git clone failed", "details": stderr},
            status_code=500,
        )


# Host /build directory as static files
if path.exists("/build"):
    app.mount("/", StaticFiles(directory="/build", html=True), name="static")
