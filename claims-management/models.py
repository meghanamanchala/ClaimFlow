from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String)  # policyholder / agent / admin

    claims = relationship("Claim", back_populates="user")


class Policy(Base):
    __tablename__ = "policies"

    id = Column(Integer, primary_key=True)
    policy_number = Column(String)
    coverage_amount = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"))


class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True)
    claim_amount = Column(Float)
    status = Column(String, default="Submitted")
    description = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="claims")