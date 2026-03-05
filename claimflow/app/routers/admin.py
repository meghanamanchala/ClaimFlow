from fastapi import APIRouter, Depends
from app.dependencies import get_current_user
from app.models import User
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()

@router.get("/users", response_model=list[User], tags=["admin"])
async def get_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "Admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    users = db.query(User).all()
    return users

# Additional admin routes can be added here as needed.