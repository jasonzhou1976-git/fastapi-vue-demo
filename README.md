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

## Run With Docker

From the project root:

```powershell
docker compose up --build
```

The Docker frontend runs at:

```text
http://127.0.0.1:8080
```

The Docker backend also exposes:

```text
http://127.0.0.1:8000
```

In Docker, the frontend Nginx container proxies `/api` requests to the backend
container. The SQLite database is mounted from `backend/test.db`.

## Deploy To Local Kubernetes

The Kubernetes manifests use GHCR images:

```text
ghcr.io/jasonzhou1976-git/fastapi-backend:<commit-sha>
ghcr.io/jasonzhou1976-git/fastapi-frontend:<commit-sha>
```

GitHub Actions builds and pushes those images when `backend/**` or
`frontend/**` changes, then commits the new image tags into `k8s/*.yaml`.
Argo CD watches the `k8s/` directory on the `master` branch and syncs those
changes into the local Kubernetes cluster.

To deploy the current manifests manually:

```powershell
kubectl apply -f k8s/backend.yaml
kubectl apply -f k8s/frontend.yaml
```

Check status:

```powershell
kubectl get pods
kubectl get svc
```

Open the frontend:

```text
http://localhost:30080
```

The frontend Service exposes NodePort `30080`. The backend Service is internal
only and is reached by the frontend through `http://backend:8000`.

## API

- `GET /api/users`
- `POST /api/users`
- `PUT /api/users/{user_id}`
- `DELETE /api/users/{user_id}`
