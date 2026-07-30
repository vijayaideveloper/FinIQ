from pathlib import Path
from fastapi import FastAPI,Depends,Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.models.model import Users
from sqlalchemy.orm import Session
from app.router import signup
from app.router import login
from app.router import dashboard
from app.router import income
from app.router import expense
from app.utils.database import Base,engine,get_db
from fastapi.staticfiles import StaticFiles


BASE_DIR = Path(__file__).resolve().parent.parent
IMAGE_DIR = BASE_DIR / "image_dashboards"
STATIC_DIR = BASE_DIR / "static"
IMAGE_DIR.mkdir(exist_ok=True)

Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
app.mount("/image_dashboards", StaticFiles(directory=str(IMAGE_DIR)), name="image_dashboards")



@app.get("/")
def home(request : Request):
    return templates.TemplateResponse(
        name="index.html",
        request=request
    )

@app.get("/profile")
def profile(request : Request, db : Session = Depends(get_db)):
    email = request.cookies.get("user_email")
    if not email:
        RedirectResponse("/")

    user = db.query(Users).filter(Users.email==email).first()
    return templates.TemplateResponse(
        name="profile.html",
        request=request,
        context={
            "user" : user
        }
    )

@app.get("/logout")
def logout(request : Request):
    response = RedirectResponse(
        url="/login",
        status_code=303
    )

    response.delete_cookie("user_email")

    return response

app.include_router(signup.router)
app.include_router(login.router)
app.include_router(dashboard.router)
app.include_router(income.router)
app.include_router(expense.router)