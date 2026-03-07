from typing import Iterable

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import SessionLocal
from models import User
from jwt_handler import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Get current logged in user
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )

    payload = decode_access_token(token)

    if payload is None:
        raise credentials_exception

    email = payload.get("sub")

    if email is None:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise credentials_exception

    return user


def require_roles(allowed_roles: Iterable[str]):
    normalized_roles = {role.lower() for role in allowed_roles}

    def role_checker(current_user: User = Depends(get_current_user)):
        user_role = (current_user.role or "").lower()
        if user_role not in normalized_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user

    return role_checker