from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from ecommerce.user import router as user_router

app = FastAPI(
    title="Order management system",
    description="Order management system application",
    version="1.0.0",
    degug=True,
    # docs_url=None,
)
app.include_router(user_router.router)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"message": "Hello FastAPI!"})


@app.get("/hello/{name}")
async def hello(name: str):
    return {"message": f"Hello {name}"}
