from enum import Enum
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class RoleEnum(str, Enum):
    policyholder = "policyholder"
    agent = "agent"
    admin = "admin"


class ClaimStatusEnum(str, Enum):
    submitted = "submitted"
    documents_verified = "documents_verified"
    verified = "verified"
    under_review = "under_review"
    approved = "approved"
    rejected = "rejected"
    paid = "paid"


class ClaimTypeEnum(str, Enum):
    auto = "Auto"
    health = "Health"
    property = "Property"


class ClaimPriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: RoleEnum


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class ClaimCreate(BaseModel):
    claim_type: ClaimTypeEnum = Field(alias="claimType")
    policy_number: str = Field(alias="policyNumber")
    incident_date: date = Field(alias="incidentDate")
    estimated_amount: float = Field(alias="estimatedAmount")
    description: str
    priority: ClaimPriorityEnum = ClaimPriorityEnum.medium
    documents: list["ClaimDocumentCreate"] = Field(default_factory=list)

    model_config = ConfigDict(populate_by_name=True)


class ClaimDocumentCreate(BaseModel):
    file_name: str = Field(alias="fileName")
    file_url: str = Field(alias="fileUrl")
    file_type: str = Field(alias="fileType")
    size: float
    uploaded_at: datetime | None = Field(default=None, alias="uploadedAt")

    model_config = ConfigDict(populate_by_name=True)


class ClaimTimelineItem(BaseModel):
    step: str
    date: datetime


class PolicyCreate(BaseModel):
    policy_number: str
    coverage_amount: float
    user_id: int


class PolicyResponse(BaseModel):
    id: int
    policy_number: str
    coverage_amount: float
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class ClaimResponse(BaseModel):
    id: int
    claim_number: str | None = Field(default=None, alias="claimNumber")
    user_id: int = Field(alias="userId")
    agent_id: int | None = Field(default=None, alias="agentId")
    policy_id: int = Field(alias="policyId")
    claim_type: str = Field(alias="claimType")
    policy_number: str = Field(alias="policyNumber")
    incident_date: date = Field(alias="incidentDate")
    estimated_amount: float = Field(alias="estimatedAmount")
    priority: str
    assigned_at: datetime | None = Field(default=None, alias="assignedAt")
    resolved_at: datetime | None = Field(default=None, alias="resolvedAt")
    agent_notes: str | None = Field(default=None, alias="agentNotes")
    decision: str | None = None
    reviewed_by: int | None = Field(default=None, alias="reviewedBy")
    reviewed_at: datetime | None = Field(default=None, alias="reviewedAt")
    approved_amount: float | None = Field(default=None, alias="approvedAmount")
    approved_at: datetime | None = Field(default=None, alias="approvedAt")
    rejection_reason: str | None = Field(default=None, alias="rejectionReason")
    status: str
    description: str
    documents: list[ClaimDocumentCreate] = Field(default_factory=list)
    timeline: list[ClaimTimelineItem] = Field(default_factory=list)
    created_at: datetime | None = Field(default=None, alias="createdAt")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class ClaimTrackingResponse(BaseModel):
    claim_id: int = Field(alias="claimId")
    claim_number: str | None = Field(default=None, alias="claimNumber")
    status: str
    timeline: list[ClaimTimelineItem] = Field(default_factory=list)

    model_config = ConfigDict(populate_by_name=True)


