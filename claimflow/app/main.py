from fastapi import FastAPI
from app.routers import users, policies, claims, admin

app = FastAPI()

# Include routers
app.include_router(users.router)
app.include_router(policies.router)
app.include_router(claims.router)
app.include_router(admin.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the ClaimFlow API"}