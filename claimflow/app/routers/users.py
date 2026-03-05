from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app import models, schemas, dependencies

router = APIRouter()

@router.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
    db_user = models.User(name=user.name, email=user.email, password=user.password)  # Password should be hashed in a real implementation
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login")
def login_user(user: schemas.UserLogin, db: Session = Depends(dependencies.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not db_user.verify_password(user.password):  # Implement password verification
        raise HTTPException(status_code=400, detail="Invalid credentials")
    # Generate and return JWT token here
    return {"access_token": "token", "token_type": "bearer"}

@router.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(dependencies.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user