from fastapi import APIRouter,Request,Form,Depends,HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.models.model import Users
from app.utils.hashing import verify_password

router = APIRouter(tags=['Login'])
templates = Jinja2Templates(directory='templates')

@router.get("/login")
def signup(request : Request):
    return templates.TemplateResponse(
        name="login.html",
        request=request
    )

@router.post("/login")
def create(request : Request, 
           email : str = Form(...),
           password : str = Form(...),
           db : Session = Depends(get_db)):
    user = db.query(Users).filter(Users.email==email).first()
    if not user:
        raise HTTPException(status_code=404, detail='user not found try to signup')

    if verify_password(password, user.password):
        response = RedirectResponse(
            url='/dashboard',
            status_code=303
        )

        response.set_cookie(
            key="user_email",
            value=email,
            httponly=True,
            max_age=3600,
            samesite="lax"
        )


        return response

    raise HTTPException(status_code=402, detail="wrong password")

