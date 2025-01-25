from os import getenv
import json

from fastapi import FastAPI, status, Request, Response, Header, HTTPException
from fastapi.responses import RedirectResponse

from utils import run_build, verify_signature
from login import router as login_router, validate_token

DEBUG = getenv("BACKEND_DEBUG", "False").lower() in ("true", "1", "t")
WEBHOOK_SECRET = getenv("WEBHOOK_SECRET")
BUILD_DIR = getenv("BUILD_DIR", "/app/build")
SERVICES_DIR = getenv("SERVICES_DIR", "/app/services")

if DEBUG:
    app = FastAPI(
        debug=DEBUG,
        title="SLC Tech Documentation",
        description="SLC Tech Documentation System",
        # lifespan=lifespan,
    )
else:
    app = FastAPI(
        debug=DEBUG,
        title="SLC Tech Documentation System",
        description="SLC Tech Documentation System",
        docs_url=None,
        redoc_url=None,
        # lifespan=lifespan,
    )


# Backend Index Page - For checking purposes
@app.get("/ping", tags=["General"], status_code=status.HTTP_200_OK)
async def index():
    return {"message": "Backend Running!!"}


@app.post("/webhook", tags=["Admin"], status_code=status.HTTP_204_NO_CONTENT)
async def webhook(
    request: Request,
    x_hub_signature_256: str = Header(None),
):
    """
    GitHub webhook handler to trigger run_build on push events to the master branch.
    """
    # Get raw payload
    payload = await request.body()

    # Validate webhook signature
    verify_signature(payload, WEBHOOK_SECRET, x_hub_signature_256)

    # Parse JSON payload
    try:
        event_data = json.loads(payload)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload!")

    # Check if it's a push event on the master branch
    if event_data.get("ref") == "refs/heads/master" and event_data.get("pusher"):
        before = event_data.get("before")
        after = event_data.get("after")
        print(f"Updated commit code: {before} -> {after}")
        run_build(app, BUILD_DIR, SERVICES_DIR)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.on_event("startup")
async def startup_event():
    run_build(app, BUILD_DIR, SERVICES_DIR)


@app.middleware("http")
async def check_login(request: Request, call_next):
    if request.url.path.startswith("/apis"):
        token = request.cookies.get("Authorization")
        if not token:
            return RedirectResponse(f"/login{request.url.path}")
        uid = validate_token(token)
        if not uid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

    response = await call_next(request)
    return response


app.include_router(login_router)
