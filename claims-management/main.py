from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from database import engine, SessionLocal
from models import Base, User, Claim
from schemas import UserCreate, Token, ClaimCreate
from auth import hash_password, verify_password
from jwt_handler import create_access_token, decode_access_token

app = FastAPI()

Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# 🔹 Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔹 Get Current User
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    email = payload.get("sub")

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user


@app.get("/")
def home():
    return {"message": "Claims Management API Running"}


# 🔹 Register
@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        role=user.role
    )

    db.add(new_user)
    db.commit()

    return {"message": "User Registered Successfully"}


# 🔹 Login
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# 🔹 Protected Route
@app.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "email": current_user.email,
        "role": current_user.role
    }


# 🔹 Create Claim
@app.post("/claims")
def create_claim(
    claim: ClaimCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    new_claim = Claim(
        claim_amount=claim.claim_amount,
        description=claim.description,
        user_id=current_user.id
    )

    db.add(new_claim)
    db.commit()
    db.refresh(new_claim)

    return {"message": "Claim submitted successfully"}


# 🔹 View My Claims
@app.get("/claims")
def get_my_claims(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    claims = db.query(Claim).filter(Claim.user_id == current_user.id).all()

    return claims