from datetime import datetime, timezone
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from claims import router as claims_router

from database import engine, SessionLocal
from models import Base, User, Claim, Policy
from schemas import (
    UserCreate,
    ClaimCreate,
    ClaimResponse,
    PolicyCreate,
    PolicyResponse,
    ClaimDocumentCreate,
    ClaimTrackingResponse,
)
from auth import hash_password, verify_password
from jwt_handler import create_access_token
from dependencies import get_current_user, require_roles

app = FastAPI()


app.include_router(claims_router)

Base.metadata.create_all(bind=engine)


STATUS_TIMELINE_STEP = {
    "submitted": "Claim Submitted",
    "documents_verified": "Documents Verified",
    "verified": "Documents Verified",
    "under_review": "Under Agent Review",
    "approved": "Final Approval",
    "rejected": "Claim Rejected",
    "paid": "Payment Processed",
}


def build_claim_number(claim_id: int) -> str:
    return f"CLM-{datetime.now(timezone.utc).year}-{claim_id:06d}"


def map_documents(documents: List[ClaimDocumentCreate]) -> list[dict]:
    prepared_documents: list[dict] = []
    for document in documents:
        uploaded_at = document.uploaded_at or datetime.now(timezone.utc)
        prepared_documents.append(
            {
                "fileName": document.file_name,
                "fileUrl": document.file_url,
                "fileType": document.file_type,
                "size": document.size,
                "uploadedAt": uploaded_at.isoformat(),
            }
        )
    return prepared_documents


def build_timeline_entry(status: str) -> dict:
    return {
        "step": STATUS_TIMELINE_STEP.get(status, status.replace("_", " ").title()),
        "date": datetime.now(timezone.utc).isoformat(),
    }


def ensure_claim_access(claim: Claim, current_user: User):
    user_role = (current_user.role or "").lower()
    if user_role in {"admin"}:
        return
    if user_role == "policyholder" and claim.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Cannot access another user's claim")
    if user_role == "agent" and claim.agent_id not in {None, current_user.id}:
        raise HTTPException(status_code=403, detail="Cannot access claims assigned to another agent")


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

    if (user.status or "active").lower() != "active":
        raise HTTPException(status_code=403, detail="User account is not active")

    access_token = create_access_token(data={"sub": user.email})

    user.last_login = datetime.now(timezone.utc)
    user.is_online = True
    db.commit()

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
    policy = db.query(Policy).filter(Policy.policy_number == claim.policy_number).first()
    if policy is None:
        raise HTTPException(status_code=404, detail="Policy not found")

    if policy.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Cannot file claim for another user's policy")

    new_claim = Claim(
        user_id=current_user.id,
        claim_type=claim.claim_type.value,
        policy_number=claim.policy_number,
        incident_date=claim.incident_date,
        estimated_amount=claim.estimated_amount,
        priority=claim.priority.value,
        description=claim.description,
        documents=map_documents(claim.documents),
        status="submitted",
        timeline=[build_timeline_entry("submitted")],
        policy_id=policy.id,
    )

    db.add(new_claim)
    db.flush()
    new_claim.claim_number = build_claim_number(new_claim.id)
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
        claims = db.query(Claim).filter(Claim.user_id == current_user.id).all()

    return claims


@app.get("/claims/{claim_id}", response_model=ClaimResponse)
def get_claim_by_id(
    claim_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if claim is None:
        raise HTTPException(status_code=404, detail="Claim not found")
    ensure_claim_access(claim, current_user)
    return claim


@app.post("/claims/{claim_id}/documents", response_model=ClaimResponse)
def add_claim_document(
    claim_id: int,
    document: ClaimDocumentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["policyholder", "agent", "admin"])),
):
    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if claim is None:
        raise HTTPException(status_code=404, detail="Claim not found")

    user_role = (current_user.role or "").lower()
    if user_role == "policyholder" and claim.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Cannot upload documents for another user's claim")

    documents = claim.documents or []
    documents.extend(map_documents([document]))
    claim.documents = documents
    db.commit()
    db.refresh(claim)
    return claim




@app.get("/claims/{claim_id}/tracking", response_model=ClaimTrackingResponse)
def get_claim_tracking(
    claim_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if claim is None:
        raise HTTPException(status_code=404, detail="Claim not found")

    ensure_claim_access(claim, current_user)

    return {
        "claimId": claim.id,
        "claimNumber": claim.claim_number,
        "status": claim.status,
        "timeline": claim.timeline or [],
    }


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
            "role": user.role,
            "status": user.status,
            "lastLogin": user.last_login,
            "isOnline": user.is_online,
            "createdAt": user.created_at,
        }
        for user in users
    ]
