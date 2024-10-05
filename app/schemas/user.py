## Create User schema with pydantic

from pydantic import BaseModel

class UserLogin(BaseModel):
    email: str
    password: str

class UserSession(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str