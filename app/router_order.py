import logging
from pathlib import Path
from random import choice
from typing import Optional

from fastapi import APIRouter, Cookie, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import Template
from starlette.responses import RedirectResponse

import fake_backend
from model import OrderedPizza
from settings import MAX_SEARCH_RESULTS, TEMPLATE_FOLDER, TEMPLATE_PARTIAL_FOLDER

templates = Jinja2Templates(directory=TEMPLATE_FOLDER)


router = APIRouter()


@router.get("/search_pizza", response_class=HTMLResponse, include_in_schema=False)
def search_pizza(request: Request, pq: str, session_id: str = Cookie(None)):
    matched_pizzas = fake_backend.find_pizzas(
        search_text=pq, max_results=MAX_SEARCH_RESULTS + 1
    )

    if pq and not matched_pizzas:
        return HTMLResponse("No pizza found. Try other ingredients.")

    html_parts = []

    template = Template(Path(TEMPLATE_PARTIAL_FOLDER, "search_pizza.html").read_text())
    for pizza in matched_pizzas[:MAX_SEARCH_RESULTS]:
        html_parts.append(template.render(pizza=pizza))

    if not matched_pizzas:
        html_parts.append("Why not try this pizza?<p/>")
        pizza = fake_backend.PIZZAS.get(choice(list(fake_backend.PIZZAS.keys())))
        html_parts.append(template.render(pizza=pizza))

    if len(matched_pizzas) > MAX_SEARCH_RESULTS:
        html_parts.append("<p/>There are more. Enter more search terms...")

    body = "\n".join(html_parts)
    return HTMLResponse(body)


@router.get(
    "/order_pizza/{order_id}", response_class=HTMLResponse, include_in_schema=False
)
def order_id(
    request: Request, order_id: Optional[str] = None, session_id: str = Cookie(None)
):
    if session_id is None:
        logging.info(f"No session_id - redirecting to login.")
        return RedirectResponse(url=f"login", status_code=303)

    email = request.app.state.sessions.get(session_id)

    logging.info(f"email: {email}, session_id: {session_id}")

    if email is None:
        logging.info(f"No email - redirecting to login.")
        return RedirectResponse(url=f"login", status_code=303)

    pizza = fake_backend.PIZZAS.get(order_id)

    # store the order in globals
    new_order = OrderedPizza(order_id=order_id, customer_email=email)
    request.app.state.orders.append(new_order)

    template = Template(Path(TEMPLATE_PARTIAL_FOLDER, "order_pizza.html").read_text())
    body = template.render(email=email, pizza=pizza)

    return HTMLResponse(body)
