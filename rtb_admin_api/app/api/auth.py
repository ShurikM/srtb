from fastapi import APIRouter, Response, HTTPException, Cookie, Depends
from pydantic import BaseModel
from itsdangerous import TimestampSigner, BadSignature
from shared.config import SECRET_KEY

router = APIRouter()

signer = TimestampSigner(SECRET_KEY)

class LoginForm(BaseModel):
    username: str
    password: str

def set_login_cookie(response: Response, username: str):
    signed = signer.sign(username.encode()).decode()
    response.set_cookie("session", signed, httponly=True)

def get_logged_user(session: str = Cookie(None)) -> str:
    try:
        username = signer.unsign(session, max_age=3600)
        return username.decode()
    except BadSignature:
        raise HTTPException(status_code=401, detail="Invalid or expired session")

@router.post("/login")
def login(form: LoginForm, response: Response):
    if form.username == "admin" and form.password == "password":
        set_login_cookie(response, form.username)
        return {"status": "ok"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")