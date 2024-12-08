from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .auth import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    user_id = verify_token(token)
    return user_id
