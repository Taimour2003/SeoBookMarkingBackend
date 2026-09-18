from auth import verify_webagent
from fastapi import Depends, FastAPI
from services.google_sheets import fetch_bookmarking_urls

app = FastAPI(title="WebAgent Backend", version="1.0.0")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/api/bookmarking-urls", dependencies=[Depends(verify_webagent)])
async def get_bookmarking_urls():
    urls = fetch_bookmarking_urls()

    return {"success": True, "count": len(urls), "urls": urls}
