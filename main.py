from os import getenv
import json

from fastapi import FastAPI, status, Request, Response, Header, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse

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
            return RedirectResponse(f"/login?redirect={request.url.path}")
        
        valid_uid = validate_token(token)
        if not valid_uid:
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Access Denied</title>
                <meta http-equiv="refresh" content="5;url=/">
                <style>
                    body {{ font-family: Arial, sans-serif; text-align: center; margin-top: 100px; background-color: #f8f9fa; }}
                    .error-container {{ max-width: 600px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                    .go-back-btn {{ background-color: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 20px; }}
                    .countdown {{ color: #666; margin-top: 10px; }}
                </style>
                <script>
                    let countdown = 5;
                    function updateCountdown() {{
                        document.getElementById('countdown').innerText = countdown;
                        countdown--;
                        if (countdown < 0) {{
                            window.location.href = '/';
                        }}
                    }}
                    setInterval(updateCountdown, 1000);
                </script>
            </head>
            <body onload="updateCountdown()">
                <div class="error-container">
                    <h1>🔒 Access Denied</h1>
                    <p><strong>You are not allowed to visit this page.</strong></p>
                    <p>This content is part of internal documentation and requires special authorization.</p>
                    <p>Only users with limited access permissions can view this resource.</p>
                    <p><em>Attempted path: {request.url.path}</em></p>
                    <a href="/" class="go-back-btn">Go Back to Home</a>
                    <p class="countdown">Redirecting automatically in <span id="countdown">5</span> seconds...</p>
                </div>
            </body>
            </html>
            """
            return HTMLResponse(content=html_content, status_code=403)

    response = await call_next(request)
    return response


app.include_router(login_router)
