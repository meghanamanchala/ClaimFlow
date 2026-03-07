# ClaimFlow – Insurance Claims Management API

ClaimFlow is a role-based backend system built using FastAPI that manages the complete lifecycle of insurance claims — from submission to approval and payout.

It simulates a real-world insurance backend system used by policyholders, agents, and administrators.

---

## Overview

ClaimFlow provides secure authentication, structured claim workflows, and role-based access control to ensure proper processing of insurance claims.

The system uses Supabase (managed PostgreSQL) as the cloud database backend.

---

## Features

### Authentication & Authorization
- JWT-based authentication
- Password hashing with bcrypt
- Role-based access control (RBAC)
- Roles: Policyholder, Agent, Admin

### User Management
- User registration and login
- Role assignment
- Secure token-based sessions

### Policy Management
- Create insurance policies
- Assign policies to users
- View active policies

### Claims Management
- Submit claim against a policy
- View claim history
- Update claim status (Agent/Admin)
- Claim lifecycle tracking

### Claim Status Workflow

Submitted → Under Review → Approved / Rejected → Paid → Closed

---

## Architecture Overview

ClaimFlow follows a layered backend architecture:

```text
Client (Swagger UI / Future Frontend)
        ↓
FastAPI Application Layer
        ↓
Service Layer (Business Logic)
        ↓
SQLAlchemy ORM
        ↓
Supabase (Managed PostgreSQL Cloud Database)
```

This design ensures separation of concerns, scalability, and maintainability.

---

## Project Structure

```text
claimflow/
│
├── Readme.md
└── claims-management/
        ├── main.py
        ├── database.py
        ├── models.py
        ├── schemas.py
        ├── auth.py
        ├── dependencies.py
        ├── claims.py
        ├── jwt_handler.py
        ├── requirements.txt
        ├── tests/
        └── .env
```

---

## Tech Stack

### Backend
- Python 3.11
- FastAPI
- Uvicorn

### Database
- Supabase (Managed PostgreSQL)
- SQLAlchemy ORM

### Authentication
- JWT (python-jose)
- Passlib (bcrypt hashing)

### DevOps
- Docker
- Environment variables (.env)

### Testing
- Pytest

---

## Database Schema

### Users Table

| Field | Type |
|-------|------|
| id | Integer (Primary Key) |
| name | String |
| email | String (Unique) |
| password | Hashed String |
| role | Enum (Policyholder, Agent, Admin) |

### Policies Table

| Field | Type |
|-------|------|
| id | Integer (Primary Key) |
| policy_number | String |
| coverage_amount | Float |
| user_id | Foreign Key (Users) |

### Claims Table

| Field | Type |
|-------|------|
| id | Integer (Primary Key) |
| claim_number | String (Unique) |
| user_id | Foreign Key (Users) |
| policy_id | Foreign Key (Policies) |
| claim_type | String (Auto/Health/Property) |
| policy_number | String |
| incident_date | Date |
| estimated_amount | Float |
| approved_amount | Float (Nullable) |
| approved_at | Timestamp (Nullable) |
| documents | JSON Array |
| timeline | JSON Array |
| description | Text |
| status | String |
| created_at | Timestamp |

---

## API Endpoints

### Authentication
- POST /register
- POST /login

### Users
- GET /users (Admin Only)

### Policies
- POST /policies (Admin Only)
- GET /policies (Policyholder: Own Policies, Agent/Admin: All Policies)

### Claims
- POST /claims (Policyholder Only)
- GET /claims   (Policyholder: Own Claims, Agent/Admin: All Claims)
- POST /claims/{id}/documents (Policyholder Owner / Agent / Admin)
- PATCH /claims/{id}/status (Agent/Admin Only)
- GET /claims/{id}/tracking (Owner / Agent / Admin)

Claim create payload example:

```json
{
        "claimType": "Auto",
        "policyNumber": "POL-1234-0001",
        "incidentDate": "2026-03-02",
        "estimatedAmount": 4500,
        "description": "Front bumper damage",
        "documents": [
                {
                        "fileName": "police-report.pdf",
                        "fileUrl": "https://storage.example/police-report.pdf",
                        "fileType": "PDF",
                        "size": 2.4,
                        "uploadedAt": "2026-03-02T10:30:00Z"
                }
        ]
}
```

---

## Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/your-username/claimflow.git  
cd claimflow
cd claims-management
```

### 2. Create Virtual Environment

```bash
python -m venv venv  
source venv/bin/activate  (Mac/Linux)  
source venv/Scripts/Activate     (Windows)
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Supabase

1. Create a project at https://supabase.com
2. Go to Settings → Database
3. Copy the connection string

Create a `.env` file:

```env
DATABASE_URL=postgresql://username:password@db.supabase.co:5432/postgres  
SECRET_KEY=your_secret_key  
ALGORITHM=HS256  
ACCESS_TOKEN_EXPIRE_MINUTES=60  
```

### 5. Run Server

```bash
uvicorn main:app --reload
```

Access API documentation at:  
http://127.0.0.1:8000/docs  

---

## Docker Setup

### Build Image

```bash
docker build -t claimflow .
```

### Run Container

```bash
docker run --env-file .env -p 8000:8000 claimflow
docker compose up --build```

### Run With Docker Compose

```bash
docker compose up --build
```

To stop:

```bash
docker compose down
```

---

## Running Tests

```bash
pytest
```

---

## Future Improvements

- File upload for claim documents (Supabase Storage)
- Email notifications
- Fraud detection logic
- Admin dashboard
- Microservices architecture
- CI/CD integration
- Deployment on AWS or Render
- Frontend application (Vue)
