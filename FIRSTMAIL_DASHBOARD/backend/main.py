from pathlib import Path

from fastapi import FastAPI
from fastapi import Request
from fastapi import Form

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from imap_client import check_accounts
from services import get_services

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI()

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)

app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static"
)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "services": get_services()
        }
    )

@app.post("/check", response_class=HTMLResponse)
async def check_mail(
    request: Request,
    service: str = Form(...),
    accounts_text: str = Form(...)
):

    accounts = []

    for line in accounts_text.splitlines():

        line = line.strip()

        if not line:
            continue

        parts = line.split(":")

        if len(parts) < 2:
            continue

        accounts.append({
            "email": parts[0].strip(),
            "password": ":".join(parts[1:]).strip()
        })

    results = check_accounts(
        accounts,
        service,
        max_workers=20
    )

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "results": results,
            "service": service
        }
    )

@app.get("/health")
async def health():

    return {
        "status": "ok"
    }

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )