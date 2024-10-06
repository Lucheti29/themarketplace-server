from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.repository.user_repository import UserRepository, AuthenticationError

security = HTTPBearer()

def get_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    repository = UserRepository()

    try:
        return repository.get_user(token)
    except AuthenticationError as e:
        raise HTTPException(status_code=401, detail=e.message)