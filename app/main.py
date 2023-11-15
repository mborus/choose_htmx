import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import router_login
import router_main
import router_order
import router_dashboard
from settings import APP_HTTP_PORT

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # setting some global state on startup
    app.state.sessions = {}  # user sessions
    app.state.orders = []  # ordered pizzas
    yield


app = FastAPI(
    title="HTMX First Steps",
    description="Demonstration for Python Pizza HH 2023.",
    lifespan=lifespan,
    debug=True,
)

app.mount("/static", StaticFiles(directory="static_files", html=True), name="static")
app.include_router(router=router_main.router)
app.include_router(router=router_login.router)
app.include_router(router=router_order.router)
app.include_router(router=router_dashboard.router)

if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=APP_HTTP_PORT,
        workers=1,
    )
