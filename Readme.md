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
claims_management/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── dependencies.py
│   └── routers/
│       ├── users.py
│       ├── policies.py
│       ├── claims.py
│       └── admin.py
│
├── tests/
├── requirements.txt
├── Dockerfile
├── .env
└── README.md
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
| policy_id | Foreign Key (Policies) |
| claim_amount | Float |
| description | Text |
| status | Enum |
| created_at | Timestamp |

---

## API Endpoints

### Authentication
- POST /register
- POST /login

### Users
- GET /users (Admin Only)

### Policies
- POST /policies
- GET /policies

### Claims
- POST /claims
- GET /claims
- PATCH /claims/{id}/status

---

## Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/your-username/claimflow.git  
cd claimflow  
```

### 2. Create Virtual Environment

```bash
python -m venv venv  
source venv/bin/activate  (Mac/Linux)  
venv\Scripts\activate     (Windows)
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
uvicorn app.main:app --reload  
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
docker run -p 8000:8000 claimflow
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
