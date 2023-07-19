from fastapi import APIRouter

from . import auth_controller

router = APIRouter()
router.include_router(
    auth_controller.router,
    prefix='/auth',
    tags=['auth'],
)