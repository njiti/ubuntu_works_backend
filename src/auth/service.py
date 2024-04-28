from fastapi import Depends
from sqlalchemy.orm import Session

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta, datetime

from .models import User

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="v1/auth/token")
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"  # encode jwt
TOKEN_EXPIRE_MINS = 60 * 24 * 30  # 30 days


# check for existing user
async def existing_user(db: Session, username: str, email: str):
    db_user = db.query(User).filter(User.username == username).first()
    db_user = db.query(User).filter(User.email == email).first()
    return db_user


# create access token
async def create_access_token(username: str, id: int):
    encode = {"sub": username, "id": id}
    expires = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINS)
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


# get current user from token
async def get_current_user(db: Session, token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        id: str = payload.get("id")
        expires: datetime = payload.get("exp")
        if datetime(expires) < datetime.now():
            return None
        if username is None or id is None:
            return None
        return db.query(User).filter(User.id == id).first()
    except JWTError:
        return None


# get user from user id
async def get_user_from_user_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()
