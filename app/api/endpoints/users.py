from fastapi import APIRouter, Depends, HTTPException, status
from app.utils.utils import get_token
from app.schemas.user import UserLogin, UserSession
from app.repository.user_repository import UserRepository, AuthenticationError

router = APIRouter()

@router.get("/")
def get_user(token: str = Depends(get_token)):
    user_repo = UserRepository()

    try:
        return user_repo.get_user(token)
    except AuthenticationError as e:
        raise HTTPException(status_code=401, detail=e.message)


@router.post("/login", response_model=UserSession)
def login(credentials: UserLogin):
    user_repo = UserRepository()
    try:
        user_session = user_repo.login_user(credentials.email, credentials.password)
        return user_session
    except AuthenticationError as e:
        raise HTTPException(status_code=401, detail=e.message)