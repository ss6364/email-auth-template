from fastapi import FastAPI, Depends, HTTPException, Request, Form, Response
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .firebase import verify_firebase_token
from .auth import get_current_user
from .db import db

app = FastAPI()

users_collection = db["users"]
user_data={}

# Serve static files (CSS/JS) if needed
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup Jinja templates
templates = Jinja2Templates(directory="app/templates")

# ------ Cookies setup ------ #

@app.post("/set_token")
async def set_token(request: Request):
    """
    Set Cookies for authorised requests
    """
    body = await request.json()
    token = body.get("token")
    if not token:
        raise HTTPException(status_code=400, detail="Missing token")

    try:
        decoded_token = verify_firebase_token(token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

    response = JSONResponse({"message": "Login successful"})
    # setting cookie here which will be picked by get_current_user later
    response.set_cookie(key="token", value=token, httponly=True, secure=False)
    return response


# ---- ROUTES ---- #

@app.get("/", response_class=HTMLResponse)
def login_page(request: Request, user=Depends(get_current_user(required=False))):
    """
    Renders the login.html page with Firebase login form.
    """
    is_authorised = False
    if user:
        is_authorised = user["email_verified"]

    return templates.TemplateResponse("login.html", {
        "request": request,
        "is_authorised": is_authorised,
        })

@app.post("/logout")
def logout(response: Response):
    response.delete_cookie(key="token", path="/")
    return {"message": "Logged out successfully"}


# Home page render
@app.get("/home", response_class=HTMLResponse)
async def home(request: Request, user=Depends(get_current_user(required=True))):
    """
    Protected route → requires Firebase token in Authorization header.
    """
    uid = user["uid"]
    is_authorised = user["email_verified"]
    
    data = await users_collection.find_one({"_id": uid})
    if data is None:
        data = {}

    return templates.TemplateResponse("home.html", {
        "request": request,
        "is_authorised": is_authorised,
        "name": data.get("name","User") or user.get("name", "User"),
        "email": user.get("email", ""),
    })

@app.get("/profile", response_class=HTMLResponse)
async def profile(request: Request, user=Depends(get_current_user(required=True))):
    """
    Protected route → requires Firebase token in Authorization header.
    """
    uid = user["uid"]
    print(" decoded token : " , user)
    data = await users_collection.find_one({"_id": uid})
    #data = user_data.get(uid, {"name": user.get("name", ""), "twitter_id": None})
    if data is None:
        data = {}

    return templates.TemplateResponse("profile.html", {
        "request": request,
        "name": data.get("name","User") or user.get("name", "User"),
        "email": user.get("email", ""),
    })

@app.post("/profile")
async def update_profile(
    name: str = Form(None),
    user=Depends(get_current_user(required=True))
):
    uid = user["uid"]

    update_data = {}
    if name:
        update_data["name"] = name

    if update_data:
        await users_collection.update_one(
            {"_id": uid},
            {"$set": update_data},
            upsert=True
        )

    # redirect back to profile page
    return RedirectResponse(url="/profile", status_code=303)


# courses page rendering
@app.get("/courses", response_class=HTMLResponse)
def courses(request: Request, user=Depends(get_current_user(required=False))):
    """
    Renders the course.html page, shows course list if user is not logged in.
    """
    is_authorised = False
    if user:
        is_authorised = user["email_verified"]

    return templates.TemplateResponse("courses.html", {
        "request": request,
        "is_authorised": is_authorised,
        })
