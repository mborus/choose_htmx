import logging
from pathlib import Path

from fastapi import APIRouter, Cookie, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import Template
from jinja2.environment import Markup
from starlette.responses import RedirectResponse

from settings import TEMPLATE_FOLDER, TEMPLATE_PARTIAL_FOLDER

router = APIRouter()

templates = Jinja2Templates(directory=TEMPLATE_FOLDER)


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
@router.get("/index.html", response_class=HTMLResponse, include_in_schema=False)
def main_index(request: Request, session_id: str = Cookie(None)):
    logging.info(f"Checking session_id from Cookie: {session_id=}")

    if session_id is None:
        logging.info(f"No session_id - redirecting to login.")
        return RedirectResponse(url=f"login", status_code=303)

    email = request.app.state.sessions.get(session_id)

    logging.info(f"email: {email}, session_id: {session_id}")

    if email is None:
        logging.info(f"No email - redirecting to login.")
        return RedirectResponse(url=f"login", status_code=303)

    body_html = Path(TEMPLATE_PARTIAL_FOLDER, "index.html").read_text()
    template = Template(body_html)
    body = Markup(template.render(email=email))

    return templates.TemplateResponse(
        name=f"base.html",
        context={
            "request": request,
            "title": "Python Pizza HH 2023",
            "body": body,
        },
    )
