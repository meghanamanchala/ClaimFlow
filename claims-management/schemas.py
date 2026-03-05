from pydantic import BaseModel, ConfigDict

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class ClaimCreate(BaseModel):
    claim_amount: float
    description: str


class ClaimResponse(BaseModel):
    id: int
    claim_amount: float
    status: str
    description: str

    model_config = ConfigDict(from_attributes=True)
