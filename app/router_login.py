import logging
from pathlib import Path
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Cookie, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import Template
from jinja2.environment import Markup


import fake_backend
from settings import TEMPLATE_FOLDER, TEMPLATE_PARTIAL_FOLDER

router = APIRouter()

templates = Jinja2Templates(directory=TEMPLATE_FOLDER)


@router.get("/login", response_class=HTMLResponse, include_in_schema=False)
def login_form(request: Request):
    # allow body to contain html tags
    body = Markup(Path(TEMPLATE_PARTIAL_FOLDER, "login.html").read_text())

    # if it's a HTMX request, return just the part
    if request.headers.get("hx-request") == "true":
        return HTMLResponse(body)

    # if it's not a HTMX request, return a full page
    return templates.TemplateResponse(
        name=f"base.html",
        context={
            "request": request,
            "title": "Python Pizza HH 2023",
            "body": body,
        },
    )


@router.post("/login", response_class=HTMLResponse, include_in_schema=False)
def login(
    request: Request, email: Annotated[str, Form()], password: Annotated[str, Form()]
):
    # it's a not HTMX request, display JavaScript missing warning
    if request.headers.get("hx-request") != "true":
        body = Markup(Path(TEMPLATE_FOLDER, "partials", "no_htmx.html").read_text())
        return templates.TemplateResponse(
            name=f"base.html",
            context={
                "request": request,
                "title": "Python Pizza HH 2023",
                "body": body,
            },
        )

    if fake_backend.user_login_possible(email=email, password=password):
        body_html = Path(TEMPLATE_PARTIAL_FOLDER, "login_success.html").read_text()
        template = Template(body_html)
        session_id = str(uuid4())
        request.app.state.sessions[session_id] = email
        body = template.render(session_id=session_id)
        return HTMLResponse(body, 200)
    else:
        # allow body to contain html tags
        body = Markup(Path(TEMPLATE_PARTIAL_FOLDER, "login_failed.html").read_text())

        # Note: alternative for this at https://htmx.org/extensions/response-targets/
        #       as of 2023.11.15 this doesn't yet work with 1.9.8, use 1.9.7 instead

        # originally requested: #login-area
        # but I can send the response somewhere else
        response = HTMLResponse(body, status_code=200)
        response.headers["HX-Retarget"] = "#login-fail"
        return response


@router.get("/logout", response_class=HTMLResponse, include_in_schema=False)
def logout(request: Request, session_id: str = Cookie(None)):
    # remove session if exists
    # TODO - Cancel pizza orders

    _ = request.app.state.sessions.pop(session_id, None)

    logging.info(f"Logging out session_id {session_id} - redirecting to login.")
    body = Markup(Path(TEMPLATE_PARTIAL_FOLDER, "logout_success.html").read_text())
    return HTMLResponse(body)
