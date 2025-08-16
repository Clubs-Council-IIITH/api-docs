from os import getenv
from fastapi import APIRouter, Request, Response
from fastapi.responses import RedirectResponse

from typing import Optional

from cas import CASClient
from jwt import encode, decode
from urllib.parse import quote_plus

router = APIRouter()

SECURE_COOKIES = getenv("SECURE_COOKIES", "False").lower() in (
    "true",
    "1",
    "t",
)
CAS_SERVER_URL = getenv("CAS_SERVER_URL")
SERVICE_URL = getenv("SERVICE_URL")
REDIRECT_URL = getenv("REDIRECT_URL", "/")
JWT_SECRET = getenv("JWT_SECRET", "jwt-secret-very-very-secret")
service_url_formatted = "%s?next=%s"

# instantiate CAS client
cas_client = CASClient(
    version=3,
    service_url=service_url_formatted % (SERVICE_URL, quote_plus(REDIRECT_URL)),
    server_url=CAS_SERVER_URL,
)


@router.post("/login")
@router.get("/login")
@router.get("/login")
@router.post("/login")
@router.get("/login/{back_to:path}")
@router.post("/login/{back_to:path}")
async def login(request: Request, back_to: Optional[str] = None):
    path = back_to or request.url.path
    # print(f"path: {path}")

    # Already logged in
    if request.cookies.get("Authorization"):
        return RedirectResponse(path or REDIRECT_URL)

    next = request.query_params.get("next") or None
    # print(f"next: {next}")

    cas_client.service_url = service_url_formatted % (
        SERVICE_URL,
        quote_plus(next or path or REDIRECT_URL),
    )
    next = next or REDIRECT_URL

    ticket = request.query_params.get("ticket")
    if not ticket:
        # No ticket, the request come from end user, send to CAS login
        cas_login_url = cas_client.get_login_url()
        return RedirectResponse(cas_login_url)

    # Validate CAS ticket
    user, attributes, pgtiou = cas_client.verify_ticket(ticket)
    uid = attributes["uid"]
    # print(
    #     f"CAS verify ticket response: user: {user}, attributes: {attributes}, pgtiou: {pgtiou}"
    # )

    with open("allowed_users.txt") as f:
        allowed_users = f.read().splitlines()

    if not user:
        return RedirectResponse(REDIRECT_URL)
    elif uid not in allowed_users:
        return RedirectResponse(REDIRECT_URL)
    else:
        token = encode({"uid": uid}, JWT_SECRET, algorithm="HS256")
        response = RedirectResponse(next)
        response.set_cookie(
            "Authorization",
            token,
            secure=SECURE_COOKIES,
            max_age=86400,
        )
        return response

@router.get("/logout")
def logout_callback():
    response = RedirectResponse(REDIRECT_URL)
    response.delete_cookie("Authorization")
    return response


def validate_token(token: str):
    try:
        payload = decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload.get("uid")
    except:
        return None
