from enum import Enum

from pydantic import BaseModel, ConfigDict


class RoleEnum(str, Enum):
    policyholder = "policyholder"
    agent = "agent"
    admin = "admin"


class ClaimStatusEnum(str, Enum):
    submitted = "Submitted"
    under_review = "Under Review"
    approved = "Approved"
    rejected = "Rejected"
    paid = "Paid"
    closed = "Closed"

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
    claim_amount: float
    description: str


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
    claim_amount: float
    status: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class ClaimStatusUpdate(BaseModel):
    status: ClaimStatusEnum
