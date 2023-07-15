from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse
from app.core.models.token import Token
from typing import Annotated
from app.core.services.auth_service import AuthService, oauth2_scheme

router = APIRouter()

@router.post("/register")
async def register(username: str, password: str) -> JSONResponse:
    return await AuthService.register(username, password)

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> JSONResponse:
    return await AuthService.login(form_data)

@router.get("/get_user")
async def get_user(token: str = Depends(oauth2_scheme)) -> JSONResponse:
    return AuthService.get_user(token)


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> JSONResponse:
    return AuthService.login_for_access_token(form_data)