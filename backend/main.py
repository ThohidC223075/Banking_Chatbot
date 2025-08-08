from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from models import LoginForm, SignupForm, ChatRequest, User
from database import async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import bcrypt

import toml
from openai import OpenAI
from convert_query_to_english import clean_query
from fetch_info import answer_query


app = FastAPI()

# ✅ Dependency to get async db session
async def get_db() -> AsyncSession:#this is not an error
    async with async_session() as session:
        yield session



app.mount("/static", StaticFiles(directory="../static"), name="static")
templates = Jinja2Templates(directory="../templates")

# Demo "database"
users_db = {
    "test@example.com": "password123",
    "user@gmail.com": "123456"
}
#Login Part Start
@app.get("/", response_class=HTMLResponse)
async def login(request: Request):
   return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login_user(form: LoginForm, db: AsyncSession = Depends(get_db)):
    email = form.email
    password = form.password

    # Query the user from DB
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Check password match (assuming password is hashed)
    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid credentials")

        # ✅ Login success: Set a session cookie
    response = JSONResponse(content={"message": "Login successful!"})
    response.set_cookie(
        key="user_email",
        value=email,
        httponly=True,        # Protects cookie from JS access
        max_age=60 * 60 * 24 * 365  # Expires in 1year
    )
    return response
#Login Part End

#Signup Part Start
@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})
  
@app.post("/signup")
async def sign_user(form: SignupForm, db: AsyncSession = Depends(get_db)):
    # ✅ Check if email already exists
    result = await db.execute(select(User).where(User.email == form.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    # ✅ Hash password before storing
    hashed_password = bcrypt.hashpw(form.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # ✅ Create and add new user
    new_user = User(email=form.email, password=hashed_password)
    db.add(new_user)
    await db.commit()

    return JSONResponse(content={"message": "Create Account Successfully"})

#Signup Part End

#Chatbot Part Start

@app.get("/chatbot", response_class=HTMLResponse)
async def chatbot(request: Request):
    user_email = request.cookies.get("user_email")

    if not user_email:
        return RedirectResponse(url="/")  # Redirect to login if not authenticated

    # If cookie exists, show chatbot page
    return templates.TemplateResponse("chatbot.html", {"request": request})
 
@app.post("/chatbot")
async def chatbot_endpoint(chat_req: ChatRequest):
    user_message = chat_req.message
    cleaned_query = clean_query(user_message)
    answer, sources = answer_query(cleaned_query, user_message)
    motivational_speech = """
      In the name of Allah, the Most Merciful, the Most Compassionate, remember that every hardship you face is a test from Him.
      The Prophet Muhammad (peace be upon him) taught us that after every difficulty comes ease, so never lose hope.
      Put your trust in Allah and strive with patience, for He is the best of planners.
      """
    print("\n=== Retrieved Sources ===")
    for i, src in enumerate(sources, 1):
        print(f"Source {i}:\n{src}\n")
    # Demo reply logic — এখানে আপনার AI logic বসাবেন
    reply_text = f"{answer}"
    return JSONResponse(content={"reply": reply_text})
 #Chatbot Part end