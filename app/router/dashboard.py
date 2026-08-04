from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from graph import create_dashboard

templates = Jinja2Templates(directory="templates")

router = APIRouter()


def _render_dashboard(request: Request, image: str | None = None):
    return templates.TemplateResponse(
        name="dashboard.html",
        request=request,
        context={"image": image},
    )


@router.get("/dashboard")
def dashboard(request: Request):
    email = request.cookies.get("user_email")

    if not email:
        return RedirectResponse("/", status_code=303)

    try:
        result = create_dashboard(email)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Dashboard generation failed: {exc}") from exc

    return _render_dashboard(request, image=result["image"])


@router.get("/dashboard/generate")
def generate_dashboard(request: Request):
    email = request.cookies.get("user_email")

    if not email:
        return RedirectResponse("/", status_code=303)

    try:
        result = create_dashboard(email=email)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Dashboard generation failed: {exc}") from exc

    return _render_dashboard(request, image=result["image"])
