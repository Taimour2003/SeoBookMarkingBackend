import secrets

from config import settings
from fastapi import Header, HTTPException


async def verify_webagent(authorization: str | None = Header(default=None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    prefix = "Bearer "

    if not authorization.startswith(prefix):
        raise HTTPException(
            status_code=401, detail="Invalid authorization header format"
        )

    supplied_token = authorization[len(prefix) :]

    if not secrets.compare_digest(supplied_token, settings.web_agent_token):
        raise HTTPException(status_code=403, detail="Invalid API Token")
