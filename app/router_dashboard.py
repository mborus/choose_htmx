import asyncio
import datetime
import time
from pathlib import Path

from fastapi import APIRouter, Cookie, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import Template
from jinja2.environment import Markup
from sse_starlette.sse import EventSourceResponse

import fake_backend
from model import OrderedPizza
from settings import TEMPLATE_FOLDER, TEMPLATE_PARTIAL_FOLDER

router = APIRouter()

templates = Jinja2Templates(directory=TEMPLATE_FOLDER)


@router.get("/kitchen-dashboard")
async def message_stream(request: Request, session_id: str = Cookie(None)):
    async def event_generator():
        template = Template(
            Path(TEMPLATE_PARTIAL_FOLDER, "dashboard_job.html").read_text()
        )

        while True:
            # If client closes connection, stop sending events
            if await request.is_disconnected():
                break

            current_jobs = []

            order: OrderedPizza
            for order in request.app.state.orders:
                pizza = fake_backend.PIZZAS.get(order.pizza_id)
                age_min, age_sec = divmod(int(time.time() - order.ordered_at), 60)
                age = f"{age_min}:{age_sec:02d}"

                order_html = template.render(
                    email=order.customer_email,
                    age=age,
                    status=order.status,
                    pizza=pizza,
                )
                current_jobs.append(order_html)

            # while loop continues

            if current_jobs:
                body = "\n".join(current_jobs)
            else:
                body = "There are no pizzas ordered at the moment."

            # The time is updated as an out of bound element
            oob_body = (
                '<span id="current-time" hx-swap-oob="true">'
                f"{datetime.datetime.now():%H:%M:%S}"
                "</span>"
            )
            yield oob_body + body

            await asyncio.sleep(1)

    return EventSourceResponse(event_generator())


@router.get("/dash", response_class=HTMLResponse, include_in_schema=False)
def dash(request: Request):
    # allow body to contain html tags
    body = Markup(Path(TEMPLATE_FOLDER, "partials", "dashboard.html").read_text())

    return templates.TemplateResponse(
        name=f"base.html",
        context={
            "request": request,
            "title": "Python Pizza HH 2023",
            "body": body,
        },
    )
