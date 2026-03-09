# How To Run (Docker Full Stack)

This project uses Docker Compose to run both services:
- `api` (FastAPI backend) on port `8000`
- `frontend` (Vue + Vite) on port `5173`

## Option 1: Run From Backend Folder (Recommended)

```powershell
cd D:\ClaimFlow\claims-management\backend
docker compose up --build -d
```

Open in browser:
- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`

## Option 2: Run From Anywhere

```powershell
docker compose -f D:\ClaimFlow\claims-management\backend\docker-compose.yml up --build -d
```

## Check Status

```powershell
cd D:\ClaimFlow\claims-management\backend
docker compose ps
```

## View Logs

```powershell
cd D:\ClaimFlow\claims-management\backend
docker compose logs -f api
docker compose logs -f frontend
```

## Stop Everything

```powershell
cd D:\ClaimFlow\claims-management\backend
docker compose down
```

Or from anywhere:

```powershell
docker compose -f D:\ClaimFlow\claims-management\backend\docker-compose.yml down
```

## Common Error

If you run `docker compose down` from `D:\ClaimFlow` and get an error, it means Docker cannot find `docker-compose.yml` in the current folder.

Use one of these:
- `cd D:\ClaimFlow\claims-management\backend` first, then run compose commands
- or always use `-f D:\ClaimFlow\claims-management\backend\docker-compose.yml`
