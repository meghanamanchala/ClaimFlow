from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app import models, schemas, dependencies

router = APIRouter()

@router.post("/policies", response_model=schemas.Policy)
def create_policy(policy: schemas.PolicyCreate, db: Session = Depends(dependencies.get_db)):
    db_policy = models.Policy(**policy.dict())
    db.add(db_policy)
    db.commit()
    db.refresh(db_policy)
    return db_policy

@router.get("/policies", response_model=list[schemas.Policy])
def get_policies(skip: int = 0, limit: int = 10, db: Session = Depends(dependencies.get_db)):
    policies = db.query(models.Policy).offset(skip).limit(limit).all()
    return policies