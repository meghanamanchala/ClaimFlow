from datetime import datetime, timezone
import os
import re
import shutil
from pathlib import Path
from typing import List

from fastapi import FastAPI, Depends, HTTPException, Query, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from claims import router as claims_router

from database import engine, SessionLocal
from models import Base, User, Claim, Policy, Message, PermissionSetting, SystemSetting
from schemas import (
    UserCreate,
    UserProfileResponse,
    UserProfileUpdate,
    UserStatusUpdate,
    ClaimCreate,
    ClaimResponse,
    PolicyCreate,
    PolicyResponse,
    ClaimDocumentCreate,
    ClaimTrackingResponse,
    ClaimDecisionUpdate,
    MessageCreate,
    MessageResponse,
    PermissionConfigUpdate,
    PermissionRoleConfig,
    AdminSettingsResponse,
    AdminSettingsUpdate,
)
from auth import hash_password, verify_password
from jwt_handler import create_access_token
from dependencies import get_current_user, require_roles

app = FastAPI()


def parse_allowed_origins() -> list[str]:
    raw = os.getenv("ALLOWED_ORIGINS", "")
    if not raw.strip():
        return [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ]
    return [origin.strip() for origin in raw.split(",") if origin.strip()]

UPLOADS_DIR = Path(__file__).with_name("uploads")
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=parse_allowed_origins(),
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?|https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory=str(UPLOADS_DIR)), name="uploads")


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

DEFAULT_PERMISSION_ROLES = [
    {
        "role": "Policyholder",
        "items": [
            {"name": "View own claims", "enabled": True},
            {"name": "Submit new claims", "enabled": True},
            {"name": "Upload documents", "enabled": True},
            {"name": "View claim history", "enabled": True},
            {"name": "Edit submitted claims", "enabled": False},
            {"name": "Delete claims", "enabled": False},
        ],
    },
    {
        "role": "Agent",
        "items": [
            {"name": "View assigned claims", "enabled": True},
            {"name": "Review & update status", "enabled": True},
            {"name": "Verify documents", "enabled": True},
            {"name": "Message policyholders", "enabled": True},
            {"name": "Reassign claims", "enabled": False},
            {"name": "View all claims", "enabled": False},
        ],
    },
    {
        "role": "Administrator",
        "items": [
            {"name": "Full system access", "enabled": True},
            {"name": "Manage users", "enabled": True},
            {"name": "Assign claims", "enabled": True},
            {"name": "View analytics", "enabled": True},
            {"name": "Manage permissions", "enabled": True},
            {"name": "System settings", "enabled": True},
        ],
    },
]

DEFAULT_SYSTEM_SETTINGS = {
    "general": {
        "company_name": "ClaimFlow Inc.",
        "support_email": "support@claimflow.com",
    },
    "notifications": {
        "email_notifications_for_new_claims": True,
        "sms_alerts_for_status_updates": False,
        "daily_summary_reports": True,
        "agent_assignment_notifications": True,
    },
    "claim_processing": {
        "auto_assign_threshold": 5000,
        "review_deadline_days": 7,
        "auto_assignment": True,
    },
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


def sanitize_file_name(file_name: str) -> str:
    base_name = Path(file_name or "document").name
    safe_name = re.sub(r"[^A-Za-z0-9._-]", "_", base_name).strip("._")
    return safe_name or "document"


def extract_upload_relative_path(file_url: str | None) -> str | None:
    if not file_url:
        return None
    marker = "/uploads/"
    index = file_url.find(marker)
    if index == -1:
        return None
    return file_url[index + len(marker):].lstrip("/")


def ensure_claim_access(claim: Claim, current_user: User):
    user_role = (current_user.role or "").lower()
    if user_role in {"admin"}:
        return
    if user_role == "policyholder" and claim.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Cannot access another user's claim")
    if user_role == "agent" and claim.agent_id not in {None, current_user.id}:
        raise HTTPException(status_code=403, detail="Cannot access claims assigned to another agent")


def append_timeline_if_new(claim: Claim, status: str):
    timeline = claim.timeline or []
    step_name = STATUS_TIMELINE_STEP.get(status, status.replace("_", " ").title())

    last_step = (timeline[-1] or {}).get("step") if timeline else None
    if last_step == step_name:
        return

    timeline.append(build_timeline_entry(status))
    claim.timeline = timeline


def hydrate_permission_settings(db: Session):
    existing = db.query(PermissionSetting).all()
    if existing:
        return existing

    for role in DEFAULT_PERMISSION_ROLES:
        db.add(PermissionSetting(role=role["role"], permissions=role["items"]))
    db.commit()
    return db.query(PermissionSetting).all()


def get_or_create_system_settings(db: Session):
    settings = db.query(SystemSetting).first()
    if settings:
        return settings

    settings = SystemSetting(
        general=DEFAULT_SYSTEM_SETTINGS["general"],
        notifications=DEFAULT_SYSTEM_SETTINGS["notifications"],
        claim_processing=DEFAULT_SYSTEM_SETTINGS["claim_processing"],
    )
    db.add(settings)
    db.commit()
    db.refresh(settings)
    return settings


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
    normalized_email = user.email.strip().lower()

    existing_user = db.query(User).filter(User.email == normalized_email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        name=user.name,
        email=normalized_email,
        password=hash_password(user.password),
        role=user.role.value
    )

    db.add(new_user)
    db.commit()

    return {"message": "User Registered Successfully"}


# 🔹 Login
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    normalized_email = form_data.username.strip().lower()

    user = db.query(User).filter(User.email == normalized_email).first()

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
@app.get("/me", response_model=UserProfileResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role,
    }


@app.put("/me", response_model=UserProfileResponse)
def update_me(
    payload: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_user = db.query(User).filter(User.id == current_user.id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    new_name = payload.name.strip()
    if len(new_name) < 2:
        raise HTTPException(status_code=400, detail="Name must be at least 2 characters")

    new_email = payload.email.strip().lower()
    existing_user = db.query(User).filter(User.email == new_email, User.id != db_user.id).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already in use")

    db_user.name = new_name
    db_user.email = new_email
    db.commit()
    db.refresh(db_user)

    return {
        "id": db_user.id,
        "name": db_user.name,
        "email": db_user.email,
        "role": db_user.role,
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


@app.post("/claims/{claim_id}/documents/upload", response_model=ClaimResponse)
async def upload_claim_document_file(
    claim_id: int,
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["policyholder", "agent", "admin"])),
):
    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if claim is None:
        raise HTTPException(status_code=404, detail="Claim not found")

    ensure_claim_access(claim, current_user)

    safe_name = sanitize_file_name(file.filename or "document")
    claim_dir = UPLOADS_DIR / f"claim_{claim.id}"
    claim_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
    stored_name = f"{timestamp}_{safe_name}"
    target_path = claim_dir / stored_name

    try:
        with target_path.open("wb") as output:
            shutil.copyfileobj(file.file, output)
    finally:
        await file.close()

    file_size_mb = round(target_path.stat().st_size / (1024 * 1024), 3)
    extension = Path(safe_name).suffix.lstrip(".").upper() or "FILE"
    relative_path = target_path.relative_to(UPLOADS_DIR).as_posix()
    file_url = f"{str(request.base_url).rstrip('/')}/uploads/{relative_path}"

    uploaded_doc = {
        "fileName": safe_name,
        "fileUrl": file_url,
        "fileType": extension,
        "size": file_size_mb,
        "uploadedAt": datetime.now(timezone.utc).isoformat(),
    }

    documents = claim.documents or []
    documents.append(uploaded_doc)
    claim.documents = documents

    db.commit()
    db.refresh(claim)
    return claim


@app.delete("/claims/{claim_id}/documents", response_model=ClaimResponse)
def delete_claim_document(
    claim_id: int,
    file_name: str = Query(..., alias="fileName"),
    file_url: str | None = Query(default=None, alias="fileUrl"),
    uploaded_at: str | None = Query(default=None, alias="uploadedAt"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["policyholder", "agent", "admin"])),
):
    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if claim is None:
        raise HTTPException(status_code=404, detail="Claim not found")

    ensure_claim_access(claim, current_user)

    documents = claim.documents or []

    def matches(document: dict) -> bool:
        if document.get("fileName") != file_name:
            return False
        if file_url is not None and document.get("fileUrl") != file_url:
            return False
        if uploaded_at is not None and document.get("uploadedAt") != uploaded_at:
            return False
        return True

    removed_documents = [doc for doc in documents if matches(doc)]
    remaining_documents = [doc for doc in documents if not matches(doc)]
    if not removed_documents:
        raise HTTPException(status_code=404, detail="Document not found")

    for removed in removed_documents:
        relative_path = extract_upload_relative_path(removed.get("fileUrl"))
        if not relative_path:
            continue
        path = UPLOADS_DIR / relative_path
        if path.exists() and path.is_file():
            path.unlink()

    claim.documents = remaining_documents
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


@app.patch("/admin/users/{user_id}/status")
def update_user_status(
    user_id: int,
    payload: UserStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin"])),
):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if current_user.id == user.id and payload.status != "active":
        raise HTTPException(status_code=400, detail="Admin cannot deactivate their own account")

    user.status = payload.status
    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "status": user.status,
        "lastLogin": user.last_login,
        "isOnline": user.is_online,
        "createdAt": user.created_at,
    }


@app.patch("/claims/{claim_id}/decision", response_model=ClaimResponse)
def update_claim_decision(
    claim_id: int,
    payload: ClaimDecisionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["agent", "admin"])),
):
    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if claim is None:
        raise HTTPException(status_code=404, detail="Claim not found")

    ensure_claim_access(claim, current_user)

    decision = payload.decision.lower()
    now = datetime.now(timezone.utc)
    user_role = (current_user.role or "").lower()

    if user_role == "agent" and claim.agent_id is None:
        claim.agent_id = current_user.id
        claim.assigned_at = now

    if payload.agent_notes is not None:
        claim.agent_notes = payload.agent_notes

    claim.reviewed_by = current_user.id
    claim.reviewed_at = now
    claim.decision = decision

    if decision == "approved":
        claim.status = "approved"
        claim.approved_amount = payload.approved_amount or claim.estimated_amount
        claim.approved_at = now
        claim.rejection_reason = None
        claim.resolved_at = now
    elif decision == "rejected":
        claim.status = "rejected"
        claim.approved_amount = None
        claim.approved_at = None
        claim.rejection_reason = payload.rejection_reason or "No reason provided"
        claim.resolved_at = now
    else:
        claim.status = "under_review"
        claim.resolved_at = None

    append_timeline_if_new(claim, claim.status)

    db.commit()
    db.refresh(claim)
    return claim


@app.post("/messages", response_model=MessageResponse)
def create_message(
    payload: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["policyholder", "agent", "admin"])),
):
    claim = db.query(Claim).filter(Claim.id == payload.claim_id).first()
    if claim is None:
        raise HTTPException(status_code=404, detail="Claim not found")

    ensure_claim_access(claim, current_user)

    receiver_id = payload.receiver_id
    user_role = (current_user.role or "").lower()

    if receiver_id is None:
        if user_role == "policyholder":
            if claim.agent_id is None:
                raise HTTPException(status_code=400, detail="No agent assigned to this claim")
            receiver_id = claim.agent_id
        else:
            receiver_id = claim.user_id

    receiver = db.query(User).filter(User.id == receiver_id).first()
    if receiver is None:
        raise HTTPException(status_code=404, detail="Receiver not found")

    message = Message(
        claim_id=payload.claim_id,
        sender_id=current_user.id,
        receiver_id=receiver_id,
        content=payload.content,
    )
    db.add(message)
    db.commit()
    db.refresh(message)

    return {
        "id": message.id,
        "claimId": message.claim_id,
        "senderId": message.sender_id,
        "receiverId": message.receiver_id,
        "content": message.content,
        "senderName": current_user.name,
        "createdAt": message.created_at,
    }


@app.get("/messages", response_model=List[MessageResponse])
def get_messages(
    claim_id: int | None = Query(default=None, alias="claimId"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["policyholder", "agent", "admin"])),
):
    query = db.query(Message)
    if claim_id is not None:
        query = query.filter(Message.claim_id == claim_id)

    messages = query.order_by(Message.created_at.asc()).all()
    sender_map = {user.id: user.name for user in db.query(User).all()}

    visible_messages: list[dict] = []
    for message in messages:
        claim = db.query(Claim).filter(Claim.id == message.claim_id).first()
        if claim is None:
            continue

        try:
            ensure_claim_access(claim, current_user)
        except HTTPException:
            continue

        visible_messages.append(
            {
                "id": message.id,
                "claimId": message.claim_id,
                "senderId": message.sender_id,
                "receiverId": message.receiver_id,
                "content": message.content,
                "senderName": sender_map.get(message.sender_id),
                "createdAt": message.created_at,
            }
        )

    return visible_messages


@app.get("/admin/permissions")
def get_admin_permissions(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin"])),
):
    rows = hydrate_permission_settings(db)
    return {
        "roles": [
            {
                "role": row.role,
                "items": row.permissions or [],
            }
            for row in rows
        ]
    }


@app.put("/admin/permissions")
def update_admin_permissions(
    payload: PermissionConfigUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin"])),
):
    for role_config in payload.roles:
        row = db.query(PermissionSetting).filter(PermissionSetting.role == role_config.role).first()
        items = [item.model_dump() for item in role_config.items]
        if row is None:
            row = PermissionSetting(role=role_config.role, permissions=items)
            db.add(row)
        else:
            row.permissions = items

    db.commit()
    return payload.model_dump(by_alias=True)


@app.get("/admin/settings", response_model=AdminSettingsResponse)
def get_admin_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin"])),
):
    row = get_or_create_system_settings(db)
    return {
        "general": row.general,
        "notifications": row.notifications,
        "claimProcessing": row.claim_processing,
    }


@app.put("/admin/settings", response_model=AdminSettingsResponse)
def update_admin_settings(
    payload: AdminSettingsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin"])),
):
    row = get_or_create_system_settings(db)
    payload_dict = payload.model_dump()
    row.general = payload_dict["general"]
    row.notifications = payload_dict["notifications"]
    row.claim_processing = payload_dict["claim_processing"]
    db.commit()
    db.refresh(row)

    return {
        "general": row.general,
        "notifications": row.notifications,
        "claimProcessing": row.claim_processing,
    }
