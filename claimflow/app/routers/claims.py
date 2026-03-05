from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app import models, schemas, dependencies

router = APIRouter()

@router.post("/claims", response_model=schemas.Claim)
def submit_claim(claim: schemas.ClaimCreate, db: Session = Depends(dependencies.get_db), current_user: models.User = Depends(dependencies.get_current_user)):
    db_claim = models.Claim(**claim.dict(), user_id=current_user.id)
    db.add(db_claim)
    db.commit()
    db.refresh(db_claim)
    return db_claim

@router.get("/claims", response_model=list[schemas.Claim])
def get_claims(skip: int = 0, limit: int = 10, db: Session = Depends(dependencies.get_db), current_user: models.User = Depends(dependencies.get_current_user)):
    claims = db.query(models.Claim).filter(models.Claim.user_id == current_user.id).offset(skip).limit(limit).all()
    return claims

@router.patch("/claims/{id}/status", response_model=schemas.Claim)
def update_claim_status(id: int, status: schemas.ClaimStatusUpdate, db: Session = Depends(dependencies.get_db), current_user: models.User = Depends(dependencies.get_current_user)):
    claim = db.query(models.Claim).filter(models.Claim.id == id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    if claim.user_id != current_user.id and current_user.role != "Admin":
        raise HTTPException(status_code=403, detail="Not authorized to update this claim")
    
    claim.status = status.status
    db.commit()
    db.refresh(claim)
    return claim