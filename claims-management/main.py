from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from claims import router as claims_router

from database import engine, SessionLocal
from models import Base, User, Claim, Policy
from schemas import UserCreate, ClaimCreate, ClaimResponse, ClaimStatusUpdate, PolicyCreate, PolicyResponse
from auth import hash_password, verify_password
from jwt_handler import create_access_token
from dependencies import get_current_user, require_roles

app = FastAPI()


app.include_router(claims_router)

Base.metadata.create_all(bind=engine)


# 🔹 Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
        role=user.role.value
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


@app.post("/policies", response_model=PolicyResponse)
def create_policy(
    policy: PolicyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin"]))
):
    user = db.query(User).filter(User.id == policy.user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Target user not found")

    existing_policy = db.query(Policy).filter(Policy.policy_number == policy.policy_number).first()
    if existing_policy:
        raise HTTPException(status_code=400, detail="Policy number already exists")

    new_policy = Policy(
        policy_number=policy.policy_number,
        coverage_amount=policy.coverage_amount,
        user_id=policy.user_id
    )

    db.add(new_policy)
    db.commit()
    db.refresh(new_policy)
    return new_policy


@app.get("/policies", response_model=List[PolicyResponse])
def get_policies(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_role = (current_user.role or "").lower()
    if user_role in {"agent", "admin"}:
        policies = db.query(Policy).all()
    else:
        policies = db.query(Policy).filter(Policy.user_id == current_user.id).all()

    return policies


# 🔹 Create Claim
@app.post("/claims", response_model=ClaimResponse)
def create_claim(
    claim: ClaimCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["policyholder"]))
):
    policy = db.query(Policy).filter(Policy.id == claim.policy_id).first()
    if policy is None:
        raise HTTPException(status_code=404, detail="Policy not found")

    if policy.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Cannot file claim for another user's policy")

    new_claim = Claim(
        claim_amount=claim.claim_amount,
        description=claim.description,
        policy_id=claim.policy_id
    )

    db.add(new_claim)
    db.commit()
    db.refresh(new_claim)

    return new_claim


# 🔹 View My Claims
@app.get("/claims", response_model=List[ClaimResponse])
def get_my_claims(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_role = (current_user.role or "").lower()
    if user_role in {"agent", "admin"}:
        claims = db.query(Claim).all()
    else:
        claims = db.query(Claim).join(Policy).filter(Policy.user_id == current_user.id).all()

    return claims


@app.patch("/claims/{claim_id}/status", response_model=ClaimResponse)
def update_claim_status(
    claim_id: int,
    payload: ClaimStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["agent", "admin"]))
):
    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if claim is None:
        raise HTTPException(status_code=404, detail="Claim not found")

    claim.status = payload.status.value
    db.commit()
    db.refresh(claim)
    return claim


@app.get("/users")
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin"]))
):
    users = db.query(User).all()
    return [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
        for user in users
    ]