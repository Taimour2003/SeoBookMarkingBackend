import secrets

from app.config import settings
from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer()


async def verify_webagent(
    authorization: str | None = Header(default=None),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    print("entered")
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

    token = credentials.credentials
    print(f"Token received: {token}")  # Debugging line to print the token
    if token != settings.web_agent_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Token",
        )
    return token
