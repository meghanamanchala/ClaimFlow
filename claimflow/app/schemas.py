from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    role: str

    class Config:
        orm_mode = True

class PolicyBase(BaseModel):
    policy_number: str
    coverage_amount: float

class PolicyCreate(PolicyBase):
    pass

class Policy(PolicyBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class ClaimBase(BaseModel):
    policy_id: int
    claim_amount: float
    description: str

class ClaimCreate(ClaimBase):
    pass

class Claim(ClaimBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        orm_mode = True

class ClaimStatusUpdate(BaseModel):
    status: str