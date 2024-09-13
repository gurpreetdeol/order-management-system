from celery import Celery
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from ecommerce.auth import router as auth_router
from ecommerce.user import router as user_router
from ecommerce.products import router as product_router
from ecommerce.cart import router as cart_router
from ecommerce.orders import router as order_router

from ecommerce import config

app = FastAPI(name="FastAPI AWS EKS and K8s",
              version="1.0.0",
              description="FastAPI AWS EKS and K8s",
              docs_url="/private_docs",
              redoc_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(product_router.router)
app.include_router(cart_router.router)
app.include_router(order_router.router)

# Celery
celery = Celery(
    __name__,
    broker=f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}/{config.REDIS_DB}",
    backend=f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}/{config.REDIS_DB}"
)

celery.conf.imports = [
    "ecommerce.orders.tasks"
]

# https://github.com/mukulmantosh/FastAPI_EKS_Kubernetes

# @app.get("/")
# async def home(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})
#
#
# @app.get("/hello/{name}")
# async def hello(name: str):
#     return {"message": name}
#
#
# @app.post("/about", response_class=HTMLResponse)
# async def about(request: Request):
#     return templates.TemplateResponse("about.html", {"request": request})
#
#
# @app.get("/contact", response_class=HTMLResponse)
# async def contact(request: Request):
#     return templates.TemplateResponse("contact.html", {"request": request})
