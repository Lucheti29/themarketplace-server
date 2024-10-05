from app.schemas.user import UserSession

import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv(dotenv_path='stage.env')

class AuthenticationError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class UserRepository:
    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)

    def login_user(self, email: str, password: str):
        try:
            response = self.supabase.auth.sign_in_with_password(
                {"email": email, "password": password}
            )
            
            return UserSession(
                access_token=response.session.access_token, 
                token_type=response.session.token_type, 
                expires_in=response.session.expires_in, 
                refresh_token=response.session.refresh_token)
        except Exception as e:
            raise AuthenticationError(str(e))

    def get_user(self, jwt: str):
        try:
            return self.supabase.auth.get_user(jwt)
        except Exception as e:
            raise AuthenticationError(str(e))