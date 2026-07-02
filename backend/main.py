import sqlite3
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


DB_PATH = Path(__file__).resolve().parent / "test.db"

app = FastAPI(title="User API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserCreate(BaseModel):
    username: str
    city: str
    age: int


class User(UserCreate):
    id: int


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def row_to_user(row: sqlite3.Row) -> User:
    return User(
        id=row["id"],
        username=row["username"],
        city=row["city"],
        age=row["age"],
    )


def ensure_schema():
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS "user" (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                city TEXT NOT NULL,
                age INTEGER NOT NULL
            )
            """
        )


@app.on_event("startup")
async def startup():
    ensure_schema()


@app.get("/")
async def root():
    return {"message": "FastAPI backend is running", "users_api": "/api/users"}


@app.get("/api/users", response_model=list[User])
async def list_users():
    with get_connection() as conn:
        rows = conn.execute(
            'SELECT id, username, city, age FROM "user" ORDER BY id'
        ).fetchall()
    return [row_to_user(row) for row in rows]


@app.post("/api/users", response_model=User, status_code=201)
async def create_user(user: UserCreate):
    with get_connection() as conn:
        cursor = conn.execute(
            'INSERT INTO "user" (username, city, age) VALUES (?, ?, ?)',
            (user.username, user.city, user.age),
        )
        row = conn.execute(
            'SELECT id, username, city, age FROM "user" WHERE id = ?',
            (cursor.lastrowid,),
        ).fetchone()
    return row_to_user(row)


@app.put("/api/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserCreate):
    with get_connection() as conn:
        cursor = conn.execute(
            'UPDATE "user" SET username = ?, city = ?, age = ? WHERE id = ?',
            (user.username, user.city, user.age, user_id),
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")

        row = conn.execute(
            'SELECT id, username, city, age FROM "user" WHERE id = ?',
            (user_id,),
        ).fetchone()
    return row_to_user(row)


@app.delete("/api/users/{user_id}", status_code=204)
async def delete_user(user_id: int):
    with get_connection() as conn:
        cursor = conn.execute('DELETE FROM "user" WHERE id = ?', (user_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
