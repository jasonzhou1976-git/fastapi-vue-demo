# FastAPI Vue Demo Runbook

## Overview

This application has two parts:

- `frontend`: Vue app built by Vite and served by Nginx.
- `backend`: FastAPI API server using SQLite at `backend/test.db`.

Production-like local deployment uses Kubernetes on Docker Desktop:

```text
Browser -> frontend Service NodePort 30080 -> frontend Pod / Nginx
        -> /api proxy -> backend Service -> backend Pod / FastAPI
        -> SQLite file inside backend container image
```

## Important URLs

| Purpose | URL |
| --- | --- |
| Local Vue dev server | `http://127.0.0.1:5173` |
| Local FastAPI dev server | `http://127.0.0.1:8000` |
| Docker Compose frontend | `http://127.0.0.1:8080` |
| Docker Compose backend API | `http://127.0.0.1:8000/api/users` |
| Kubernetes frontend | `http://localhost:30080` |
| Argo CD UI | `https://localhost:8082` |

## Local Development

Start backend:

```powershell
cd C:\projects\fastapi\backend
..\.venv\Scripts\uvicorn.exe main:app --reload
```

Start frontend:

```powershell
cd C:\projects\fastapi\frontend
npm install
npm run dev
```

Verify:

```powershell
Invoke-WebRequest http://127.0.0.1:8000/api/users
```

Open:

```text
http://127.0.0.1:5173
```

## Docker Compose

Start:

```powershell
cd C:\projects\fastapi
docker compose up --build
```

Stop:

```powershell
docker compose down
```

Check containers:

```powershell
docker compose ps
docker compose logs backend
docker compose logs frontend
```

The Docker Compose backend mounts the database file:

```text
Host:      backend/test.db
Container: /app/test.db
```

## Kubernetes Deployment

Current Kubernetes manifests:

```text
k8s/backend.yaml
k8s/frontend.yaml
k8s/argocd-app.yaml
```

Services:

- `backend`: `ClusterIP`, internal only, port `8000`.
- `frontend`: `NodePort`, external local access on port `30080`.

Check cluster:

```powershell
kubectl config current-context
kubectl get nodes
kubectl get all
```

Apply manually:

```powershell
kubectl apply -f k8s/backend.yaml
kubectl apply -f k8s/frontend.yaml
```

Check app:

```powershell
kubectl get deployments
kubectl get pods -o wide
kubectl get svc
kubectl get endpoints backend
kubectl get endpoints frontend
```

Open:

```text
http://localhost:30080
```

## Argo CD GitOps Flow

Argo CD Application:

```text
Application: fastapi-vue-demo
Namespace:   argocd
Repo:        https://github.com/jasonzhou1976-git/fastapi-vue-demo.git
Branch:      master
Path:        k8s
Destination: default namespace
```

Check Argo CD status:

```powershell
kubectl get application fastapi-vue-demo -n argocd
kubectl describe application fastapi-vue-demo -n argocd
```

Start Argo CD UI port-forward:

```powershell
Start-Job -Name argocd-port-forward -ScriptBlock {
  kubectl port-forward svc/argocd-server -n argocd 8082:443
}
```

Stop Argo CD UI port-forward:

```powershell
Stop-Job -Name argocd-port-forward
Remove-Job -Name argocd-port-forward
```

Get initial admin password:

```powershell
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | % { [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($_)) }
```

## Release Process

The GitHub Actions workflow is:

```text
.github/workflows/docker-build.yml
```

It runs on pushes to `master` when these paths change:

```text
backend/**
frontend/**
.github/workflows/docker-build.yml
```

Release flow:

```text
1. Developer changes backend or frontend code.
2. Developer commits and pushes to master.
3. GitHub Actions builds backend and frontend images.
4. Images are pushed to GHCR with the commit SHA as tag.
5. GitHub Actions updates k8s/backend.yaml and k8s/frontend.yaml image tags.
6. GitHub Actions commits those YAML changes back to master.
7. Argo CD detects the k8s/ change.
8. Argo CD syncs Kubernetes to the new image tags.
```

Current image format:

```text
ghcr.io/jasonzhou1976-git/fastapi-backend:<commit-sha>
ghcr.io/jasonzhou1976-git/fastapi-frontend:<commit-sha>
```

## Common Operations

Restart frontend:

```powershell
kubectl rollout restart deployment/frontend
kubectl rollout status deployment/frontend
```

Restart backend:

```powershell
kubectl rollout restart deployment/backend
kubectl rollout status deployment/backend
```

Scale frontend:

```powershell
kubectl scale deployment frontend --replicas=3
kubectl get pods -l app=frontend -o wide
```

Scale backend:

```powershell
kubectl scale deployment backend --replicas=1
kubectl get pods -l app=backend -o wide
```

View logs:

```powershell
kubectl logs deployment/frontend
kubectl logs deployment/backend
```

Enter a pod:

```powershell
kubectl exec -it deployment/frontend -- sh
kubectl exec -it deployment/backend -- sh
```

## Troubleshooting

### Page Does Not Show Latest Frontend Change

Check the image tag in Kubernetes:

```powershell
kubectl get deployment frontend -o jsonpath="{.spec.template.spec.containers[0].image}"
```

Check Argo CD:

```powershell
kubectl get application fastapi-vue-demo -n argocd
```

If the app is `Synced` but the page is stale:

```powershell
kubectl rollout restart deployment/frontend
```

Then force-refresh browser with `Ctrl+F5`.

### Pod Shows ImagePullBackOff

Inspect the pod:

```powershell
kubectl get pods
kubectl describe pod <pod-name>
```

Common causes:

- GHCR image does not exist.
- GHCR package is private and Kubernetes has no `imagePullSecret`.
- Image tag in `k8s/*.yaml` is wrong.

Test image manually:

```powershell
docker pull ghcr.io/jasonzhou1976-git/fastapi-frontend:<tag>
docker pull ghcr.io/jasonzhou1976-git/fastapi-backend:<tag>
```

### Frontend Loads But API Fails

Check backend:

```powershell
kubectl get pods -l app=backend
kubectl logs deployment/backend
kubectl get svc backend
kubectl get endpoints backend
```

Check frontend Nginx proxy config in `frontend/nginx.conf`:

```nginx
proxy_pass http://backend:8000/api/;
```

Inside Kubernetes, `backend` resolves to the backend Service.

### Git Push Rejected Because Remote Has New Work

This can happen because GitHub Actions commits updated image tags back to `master`.

Fix:

```powershell
git pull --rebase
git push
```

If conflicts happen, check:

```text
k8s/backend.yaml
k8s/frontend.yaml
```

### Argo CD Is OutOfSync

Check details:

```powershell
kubectl describe application fastapi-vue-demo -n argocd
```

Force sync from UI, or run:

```powershell
kubectl annotate application fastapi-vue-demo -n argocd argocd.argoproj.io/refresh=hard --overwrite
```

## Rollback

View rollout history:

```powershell
kubectl rollout history deployment/frontend
kubectl rollout history deployment/backend
```

Rollback frontend:

```powershell
kubectl rollout undo deployment/frontend
kubectl rollout status deployment/frontend
```

Rollback backend:

```powershell
kubectl rollout undo deployment/backend
kubectl rollout status deployment/backend
```

For strict GitOps rollback, revert the commit that changed image tags in
`k8s/*.yaml` and push to `master`. Argo CD will sync the reverted desired state.

## Data Notes

Docker Compose mounts SQLite from the host:

```text
backend/test.db -> /app/test.db
```

Kubernetes currently does not mount a persistent volume for SQLite. The database
file comes from the backend image at build time. Pod recreation may lose runtime
changes. This is acceptable for the learning demo, but production should use an
external database such as PostgreSQL or MySQL.
