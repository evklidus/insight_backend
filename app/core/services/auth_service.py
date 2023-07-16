from typing import Annotated, Optional
from fastapi import HTTPException, Depends, status
from jose import jwt
from passlib.context import CryptContext
from starlette.responses import JSONResponse
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm
from app.common.database.database import Database

from models import UserInDB

SECRET_KEY = "MY_SUPER_SECRET_KEY" # Вынести в сикрет/env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 1

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    async def register(username: str, password: str) -> JSONResponse:
        if username in Database.users:
            raise HTTPException(status_code=400, detail="Username already registered")
        hashed_password = get_password_hash(password)
        Database.users[username] = {"username": username, "hashed_password": hashed_password}
        return JSONResponse(content={"message": "User registered successfully"})

    async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> JSONResponse:
        if not (authenticated_user := authenticate_user(form_data.username, form_data.password)):
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
        access_token = create_access_token(
            data={"sub": authenticated_user.username},
            expires_delta=access_token_expires
        )
        return JSONResponse(content={"access_token": access_token, "token_type": "bearer"})

    async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
    ) -> JSONResponse:
        user = authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_DAYS)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
    
###
# Utils
###

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str):
    if username not in Database.users:
        return None
    db_user = UserInDB(**Database.users[username])
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

