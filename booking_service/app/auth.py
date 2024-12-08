# booking_service/auth.py
from datetime import datetime, timedelta
from typing import Union
from jose import JWTError, jwt
from fastapi import HTTPException, status


SECRET_KEY = "qh1cl1oTvSkhmrRS8P9pbzFFfnwB4L2gszqFh2JLsgE="  # Store this securely in production
ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# # Function to create JWT token
# def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# Function to verify JWT token
def verify_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        print("INSIDE VERIFY_TOKEN")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as jwterror:
        print(f"JWTERROR {jwterror}")
        raise credentials_exception
