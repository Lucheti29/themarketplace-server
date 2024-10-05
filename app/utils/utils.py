from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def get_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    return token