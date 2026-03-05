from sqlalchemy import Column, Integer, String, Float, Text, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
import enum
import datetime

class UserRole(enum.Enum):
    POLICYHOLDER = "Policyholder"
    AGENT = "Agent"
    ADMIN = "Admin"

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(Enum(UserRole))

    policies = relationship("Policy", back_populates="owner")

class Policy(Base):
    __tablename__ = 'policies'

    id = Column(Integer, primary_key=True, index=True)
    policy_number = Column(String, index=True)
    coverage_amount = Column(Float)
    user_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User", back_populates="policies")
    claims = relationship("Claim", back_populates="policy")

class ClaimStatus(enum.Enum):
    SUBMITTED = "Submitted"
    UNDER_REVIEW = "Under Review"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    PAID = "Paid"
    CLOSED = "Closed"

class Claim(Base):
    __tablename__ = 'claims'

    id = Column(Integer, primary_key=True, index=True)
    policy_id = Column(Integer, ForeignKey('policies.id'))
    claim_amount = Column(Float)
    description = Column(Text)
    status = Column(Enum(ClaimStatus))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    policy = relationship("Policy", back_populates="claims")