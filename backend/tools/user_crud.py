import argparse
import sqlite3
import sys
from pathlib import Path


DB_PATH = Path(__file__).resolve().parents[1] / "test.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


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


def create_user(username, city, age):
    with get_connection() as conn:
        cursor = conn.execute(
            'INSERT INTO "user" (username, city, age) VALUES (?, ?, ?)',
            (username, city, age),
        )
        return cursor.lastrowid


def list_users():
    with get_connection() as conn:
        return conn.execute(
            'SELECT id, username, city, age FROM "user" ORDER BY id'
        ).fetchall()


def get_user(user_id):
    with get_connection() as conn:
        return conn.execute(
            'SELECT id, username, city, age FROM "user" WHERE id = ?',
            (user_id,),
        ).fetchone()


def update_user(user_id, username=None, city=None, age=None):
    updates = []
    values = []

    if username is not None:
        updates.append("username = ?")
        values.append(username)
    if city is not None:
        updates.append("city = ?")
        values.append(city)
    if age is not None:
        updates.append("age = ?")
        values.append(age)

    if not updates:
        return 0

    values.append(user_id)
    with get_connection() as conn:
        cursor = conn.execute(
            f'UPDATE "user" SET {", ".join(updates)} WHERE id = ?',
            values,
        )
        return cursor.rowcount


def delete_user(user_id):
    with get_connection() as conn:
        cursor = conn.execute('DELETE FROM "user" WHERE id = ?', (user_id,))
        return cursor.rowcount


def print_user(row):
    print(
        f"id={row['id']}, username={row['username']}, "
        f"city={row['city']}, age={row['age']}"
    )


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="CRUD tool for test.db users.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List all users.")

    get_parser = subparsers.add_parser("get", help="Get one user by id.")
    get_parser.add_argument("id", type=int)

    create_parser = subparsers.add_parser("create", help="Create a user.")
    create_parser.add_argument("--username", required=True)
    create_parser.add_argument("--city", required=True)
    create_parser.add_argument("--age", type=int, required=True)

    update_parser = subparsers.add_parser("update", help="Update a user.")
    update_parser.add_argument("id", type=int)
    update_parser.add_argument("--username")
    update_parser.add_argument("--city")
    update_parser.add_argument("--age", type=int)

    delete_parser = subparsers.add_parser("delete", help="Delete a user.")
    delete_parser.add_argument("id", type=int)

    args = parser.parse_args()
    ensure_schema()

    if args.command == "list":
        for row in list_users():
            print_user(row)
    elif args.command == "get":
        row = get_user(args.id)
        if row is None:
            print(f"user id={args.id} not found")
        else:
            print_user(row)
    elif args.command == "create":
        user_id = create_user(args.username, args.city, args.age)
        print(f"created user id={user_id}")
    elif args.command == "update":
        changed = update_user(args.id, args.username, args.city, args.age)
        print(f"updated rows={changed}")
    elif args.command == "delete":
        changed = delete_user(args.id)
        print(f"deleted rows={changed}")


if __name__ == "__main__":
    main()
