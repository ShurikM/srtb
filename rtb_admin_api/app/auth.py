from fastapi import Request, Response, HTTPException, Cookie, Depends
from itsdangerous import TimestampSigner, BadSignature
from shared.config import SECRET_KEY

signer = TimestampSigner(SECRET_KEY)

def set_login_cookie(response: Response, username: str):
    signed = signer.sign(username.encode()).decode()
    response.set_cookie("session", signed, httponly=True)

def get_logged_user(session: str = Cookie(None)) -> str:
    try:
        username = signer.unsign(session, max_age=3600)
        return username.decode()
    except BadSignature:
        raise HTTPException(status_code=401, detail="Invalid or expired session")
