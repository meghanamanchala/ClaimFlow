from enum import Enum
from datetime import date, datetime
from typing import Literal

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


class UserProfileResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str


class UserProfileUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: str


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


class ClaimDecisionUpdate(BaseModel):
    decision: Literal["approved", "rejected", "under_review"]
    agent_notes: str | None = Field(default=None, alias="agentNotes")
    approved_amount: float | None = Field(default=None, alias="approvedAmount")
    rejection_reason: str | None = Field(default=None, alias="rejectionReason")

    model_config = ConfigDict(populate_by_name=True)


class MessageCreate(BaseModel):
    claim_id: int = Field(alias="claimId")
    receiver_id: int | None = Field(default=None, alias="receiverId")
    content: str

    model_config = ConfigDict(populate_by_name=True)


class MessageResponse(BaseModel):
    id: int
    claim_id: int = Field(alias="claimId")
    sender_id: int = Field(alias="senderId")
    receiver_id: int | None = Field(default=None, alias="receiverId")
    content: str
    sender_name: str | None = Field(default=None, alias="senderName")
    created_at: datetime = Field(alias="createdAt")

    model_config = ConfigDict(populate_by_name=True)


class PermissionItem(BaseModel):
    name: str
    enabled: bool


class PermissionRoleConfig(BaseModel):
    role: str
    items: list[PermissionItem]


class PermissionConfigUpdate(BaseModel):
    roles: list[PermissionRoleConfig]


class GeneralSettings(BaseModel):
    company_name: str = Field(alias="companyName")
    support_email: str = Field(alias="supportEmail")

    model_config = ConfigDict(populate_by_name=True)


class NotificationSettings(BaseModel):
    email_notifications_for_new_claims: bool = Field(alias="emailNotificationsForNewClaims")
    sms_alerts_for_status_updates: bool = Field(alias="smsAlertsForStatusUpdates")
    daily_summary_reports: bool = Field(alias="dailySummaryReports")
    agent_assignment_notifications: bool = Field(alias="agentAssignmentNotifications")

    model_config = ConfigDict(populate_by_name=True)


class ClaimProcessingSettings(BaseModel):
    auto_assign_threshold: float = Field(alias="autoAssignThreshold")
    review_deadline_days: int = Field(alias="reviewDeadlineDays")
    auto_assignment: bool = Field(alias="autoAssignment")

    model_config = ConfigDict(populate_by_name=True)


class AdminSettingsResponse(BaseModel):
    general: GeneralSettings
    notifications: NotificationSettings
    claim_processing: ClaimProcessingSettings = Field(alias="claimProcessing")

    model_config = ConfigDict(populate_by_name=True)


class AdminSettingsUpdate(BaseModel):
    general: GeneralSettings
    notifications: NotificationSettings
    claim_processing: ClaimProcessingSettings = Field(alias="claimProcessing")

    model_config = ConfigDict(populate_by_name=True)


