from fastapi import FastAPI, Depends, Request, Form, status, Response, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import timedelta

from app import models, auth
from app.database import engine, get_db
from app.config import settings

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="Team Task Manager", lifespan=lifespan)
templates = Jinja2Templates(directory="templates")

# Dependency for HTMX requests
def is_htmx(request: Request):
    return request.headers.get("HX-Request") == "true"

@app.exception_handler(status.HTTP_401_UNAUTHORIZED)
async def unauth_exception_handler(request: Request, exc: HTTPException):
    if is_htmx(request):
        return Response(status_code=status.HTTP_401_UNAUTHORIZED, headers={"HX-Redirect": "/login"})
    return RedirectResponse(url="/login")

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return RedirectResponse(url="/dashboard")

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html")

@app.post("/login")
def login_action(
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not auth.verify_password(password, user.hashed_password):
        return RedirectResponse(url="/login?error=1", status_code=status.HTTP_302_FOUND)
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    resp = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    resp.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True, samesite="lax")
    return resp

@app.get("/logout")
def logout():
    resp = RedirectResponse(url="/login")
    resp.delete_cookie("access_token")
    return resp

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    if not current_user:
        return RedirectResponse(url="/login")
    
    projects = db.query(models.Project).all()
    tasks = db.query(models.Task).all()
    users = db.query(models.User).all()
    
    return templates.TemplateResponse(request, "dashboard.html", {
        "user": current_user,
        "projects": projects,
        "tasks": tasks,
        "users": users
    })

@app.post("/tasks")
def create_task(
    request: Request,
    title: str = Form(...),
    project_id: int = Form(...),
    description: str = Form(""),
    assigned_to_id: int = Form(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    new_task = models.Task(
        title=title,
        description=description,
        project_id=project_id,
        assigned_to_id=assigned_to_id or None
    )
    db.add(new_task)
    db.commit()
    
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)

@app.patch("/tasks/{task_id}/status")
def update_task_status(
    request: Request,
    task_id: int,
    status: models.TaskStatus = Form(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task:
        task.status = status
        db.commit()
        db.refresh(task)
    
    return templates.TemplateResponse(request, "partials/task_row.html", {"task": task})

@app.post("/projects")
def create_project(
    request: Request,
    name: str = Form(...),
    description: str = Form(""),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_admin_user)
):
    new_project = models.Project(name=name, description=description)
    db.add(new_project)
    db.commit()
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
