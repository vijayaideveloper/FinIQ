from fastapi import APIRouter,Request,Form,Depends,HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.models.model import Users
from app.utils.hashing import hash_password

router = APIRouter(tags=['Signup'])
templates = Jinja2Templates(directory='templates')

@router.get("/signup")
def signup(request : Request):
    return templates.TemplateResponse(
        name="signup.html",
        request=request
    )

@router.post("/signup")
def create(request : Request, 
           name : str = Form(...),
           email : str = Form(...),
           password : str = Form(...),
           db : Session = Depends(get_db)):
    user = db.query(Users).filter(Users.email==email).first()
    if user:
        raise HTTPException(status_code=402, detail='user found try to login')

    new_user = Users(
        name=name,
        email=email,
        password=hash_password(password)
    )
    db.add(new_user)
    db.commit()

    response = RedirectResponse(
        url="login",
        status_code=303
    )


    return response

