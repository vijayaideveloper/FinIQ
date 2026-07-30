from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.models.model import Income
from graph import create_dashboard   

router = APIRouter(prefix="/dashboard", tags=['Income'])
templates = Jinja2Templates(directory="templates")


@router.get("")
def generate(request: Request):
    email = request.cookies.get("user_email")

    if not email:
        return RedirectResponse('/', status_code=303)

    try:
        result = create_dashboard()   
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dashboard generation failed: {e}")

    return templates.TemplateResponse(
        name="dashboard.html",
        request=request,
        context={"image": result["image"]}
    )