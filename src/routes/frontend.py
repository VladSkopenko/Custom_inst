from pathlib import Path
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates

# the path to the templates directory
templates_path = Path(__file__).resolve().parent.parent.joinpath("templates")
if not templates_path:
    raise RuntimeError("TEMPLATES_DIRECTORY does not exist")
templates = Jinja2Templates(directory=templates_path)

# Create a router for the home page
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Route to render the home page.
    This route renders the index.html template as the home page.
    Parameters:
    - request (Request): The incoming request object.
    Returns:
    - HTMLResponse: HTML response containing the rendered template.
    """
    try:
        context = {"request": request, "title": "Welcomу to PhotoShare"}
        return templates.TemplateResponse("index.html", context)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error rendering template: {e}")
