from fastapi import APIRouter,Request,Form,Depends,HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.models.model import Income


router = APIRouter(prefix="/income",tags=['Income'])
templates = Jinja2Templates(directory="templates")


@router.get("/")
def income(request : Request):
    email = request.cookies.get("user_email")
    
    if not email:
        return RedirectResponse('/', status_code=303)
    return templates.TemplateResponse(
        name="income.html",
        request=request
    )


@router.post("/create_button")
def create_button(request : Request):
    email = request.cookies.get("user_email")
    
    if not email:
        return RedirectResponse('/', status_code=303)
    return templates.TemplateResponse(
        name="income.html",
        request=request,
        context={
            "method" : "create"
        }
    )




@router.post("/read_button")
def read_button(request : Request):
    email = request.cookies.get("user_email")
    
    if not email:
        return RedirectResponse('/', status_code=303)
    return templates.TemplateResponse(
        name="income.html",
        request=request,
        context={
            "method" : "read"
        }
    )

@router.post("/read_all_button")
def read_all_button(
    request: Request,
    db: Session = Depends(get_db)
):
    email = request.cookies.get("user_email")

    if not email:
        return RedirectResponse("/", status_code=303)

    records = (
        db.query(Income)
        .filter(Income.email == email)
        .all()
    )

    return templates.TemplateResponse(
        name="income.html",
        request=request,
        context={
            "method": "read_all",
            "records": records
        }
    )

@router.post("/update_button")
def update_button(request : Request):
    email = request.cookies.get("user_email")
    
    if not email:
        return RedirectResponse('/', status_code=303)
    return templates.TemplateResponse(
        name="income.html",
        request=request,
        context={
            "method" : "update"
        }
    )

@router.post("/delete_button")
def delete_button(request : Request):
    email = request.cookies.get("user_email")
    
    if not email:
        return RedirectResponse('/',  status_code=303)
    return templates.TemplateResponse(
        name="income.html",
        request=request,
        context={
            "method" : "delete"
        }
    )




@router.post("/create")
def create(request : Request,
           title : str = Form(...),
           amount : float = Form(...),
           db : Session = Depends(get_db)):

    email = request.cookies.get("user_email")

    if not email:
        return RedirectResponse('/', status_code=303)

    new_income = Income(
        title=title,
        email=email,
        amount=amount
    )

    db.add(new_income)
    db.commit()

    return templates.TemplateResponse(
        name="income.html",
        request=request,
        context={
            "method" : "create",
            "message" : "Created successfully"
        }
    )

@router.post("/update")
def update(request : Request,
           id : int = Form(...),
           title : str = Form(...),
           amount : float = Form(...),
           db : Session = Depends(get_db)):

    email = request.cookies.get("user_email")

    if not email:
        return RedirectResponse('/', status_code=303)

    income = db.query(Income).filter(and_(Income.id==id ,Income.email==email)).first()
    if not income:
        return templates.TemplateResponse(
                name="income.html",
                request=request,
                context={
                    "method" : "update",
                    "message" : "id or email not found"
                }
            )

    income.title=title
    income.amount=amount
    db.commit()

    return templates.TemplateResponse(
        name="income.html",
        request=request,
        context={
            "method" : "update",
            "message" : "updated successfully"
        }
    )


@router.post("/read")
def read(request : Request,
           id : int = Form(...),
           db : Session = Depends(get_db)):

    email = request.cookies.get("user_email")

    if not email:
        return RedirectResponse('/')

    record = db.query(Income).filter(Income.id==id ).first()
    if not record:
        return templates.TemplateResponse(
                name="income.html",
                request=request,
                context={
                    "method" : "read",
                    "message" : "id not found"
                }
            )


    return templates.TemplateResponse(
        name="income.html",
        request=request,
        context={
            "method" : "read",
            "record" : record
        }
    )




@router.post("/delete")
def delete(request : Request,
             id : int = Form(...),
           db : Session = Depends(get_db)):

    email = request.cookies.get("user_email")

    if not email:
        return RedirectResponse('/')

    record = db.query(Income).filter(and_(Income.email==email, Income.id==id) ).first()
    if not record:
        return templates.TemplateResponse(
                name="income.html",
                request=request,
                context={
                    "method" : "delete",
                    "message" : "record not found"
                }
            )
    db.delete(record)
    db.commit()

    return templates.TemplateResponse(
        name="income.html",
        request=request,
        context={
            "method" : "delete",
            "message" : "deleted successfully"
        }
    )