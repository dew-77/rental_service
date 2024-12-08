from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from . import auth

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials - incorrect id",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        print("STARTING CHECK PAYLOAD")
        payload = auth.verify_token(token)
        print("ENDED CHECK PAYLOAD")

        user_id = payload.get("user_id")
        print(payload)
        if user_id is None:
            raise credentials_exception
        return {"user_id": user_id}
    except JWTError:
        raise credentials_exception