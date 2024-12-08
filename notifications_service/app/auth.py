from jose import jwt, JWTError
from fastapi import HTTPException, status

SECRET_KEY = "qh1cl1oTvSkhmrRS8P9pbzFFfnwB4L2gszqFh2JLsgE="
ALGORITHM = "HS256"

def verify_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        return user_id
    except JWTError as jwterror:
        raise credentials_exception
