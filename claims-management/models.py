from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date, DateTime, JSON, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String)  # policyholder / agent / admin
    status = Column(String, default="active", nullable=False)  # active / inactive / suspended
    is_online = Column(Boolean, default=False, nullable=False)
    last_login = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    policies = relationship("Policy", back_populates="user")
    claims = relationship("Claim", back_populates="user", foreign_keys="Claim.user_id")
    assigned_claims = relationship("Claim", back_populates="agent", foreign_keys="Claim.agent_id")
    reviewed_claims = relationship("Claim", back_populates="reviewer", foreign_keys="Claim.reviewed_by")


class Policy(Base):
    __tablename__ = "policies"

    id = Column(Integer, primary_key=True)
    policy_number = Column(String)
    coverage_amount = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="policies")
    claims = relationship("Claim", back_populates="policy")


class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True)
    claim_number = Column(String, unique=True, index=True, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    agent_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    claim_type = Column(String, nullable=False)
    policy_number = Column(String, nullable=False)
    incident_date = Column(Date, nullable=False)
    estimated_amount = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    priority = Column(String, default="medium", nullable=False)
    documents = Column(JSON, default=list, nullable=False)
    status = Column(String, default="submitted", nullable=False)
    timeline = Column(JSON, default=list, nullable=False)
    agent_notes = Column(String, nullable=True)
    decision = Column(String, nullable=True)
    reviewed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    approved_amount = Column(Float, nullable=True)
    approved_at = Column(DateTime(timezone=True), nullable=True)
    rejection_reason = Column(String, nullable=True)
    assigned_at = Column(DateTime(timezone=True), nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    policy_id = Column(Integer, ForeignKey("policies.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="claims", foreign_keys=[user_id])
    agent = relationship("User", back_populates="assigned_claims", foreign_keys=[agent_id])
    reviewer = relationship("User", back_populates="reviewed_claims", foreign_keys=[reviewed_by])
    policy = relationship("Policy", back_populates="claims")
