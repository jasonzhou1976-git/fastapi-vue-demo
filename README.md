# FastAPI + Vue Demo

This project uses a split frontend/backend structure:

- `backend`: FastAPI API server with SQLite database
- `frontend`: Vue app built with Vite

## Run Backend

```powershell
cd backend
..\.venv\Scripts\uvicorn.exe main:app --reload
```

Or:

```powershell
cd backend
..\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

The backend runs at:

```text
http://127.0.0.1:8000
```

## Run Frontend

```powershell
cd frontend
npm install
npm run dev
```

The frontend runs at:

```text
http://127.0.0.1:5173
```

## API

- `GET /api/users`
- `POST /api/users`
- `PUT /api/users/{user_id}`
- `DELETE /api/users/{user_id}`
