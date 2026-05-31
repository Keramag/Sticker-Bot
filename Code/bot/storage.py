"""Storage layer for the Sticker Bot.

This file is FULLY IMPLEMENTED for you. As a student you don't need to change
anything here — you just *call* these functions from your command files:

    from bot import storage

    student = storage.add_student("John Smith")
    total   = storage.award_stickers(student.id, 2)
    table   = storage.get_leaderboard()

The data is stored in a small SQLite database file inside the data folder, so
sticker counts survive even after the bot restarts (see the PRD).
"""

import os
import sqlite3
from dataclasses import dataclass

# The database lives in the data directory (a Docker volume in production), so
# nothing is lost when the bot restarts.
DATA_DIR = os.environ.get("DATA_DIR", "data")
DB_PATH = os.path.join(DATA_DIR, "stickers.db")


@dataclass
class Student:
    """One student and how many stickers they have. Matches the PRD data model."""

    id: int
    name: str
    sticker_count: int


def _connect():
    """Open a connection to the database (and make sure the folder exists)."""
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # lets us read columns by name
    return conn


def init_db():
    """Create the students table the first time the bot runs."""
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                name          TEXT    NOT NULL,
                sticker_count INTEGER NOT NULL DEFAULT 0
            )
            """
        )


def add_student(name: str) -> Student:
    """Add a new student with 0 stickers and return them."""
    with _connect() as conn:
        cursor = conn.execute("INSERT INTO students (name) VALUES (?)", (name,))
        return Student(id=cursor.lastrowid, name=name, sticker_count=0)


def list_students() -> list[Student]:
    """Return every student, sorted by name (handy for showing buttons)."""
    with _connect() as conn:
        rows = conn.execute("SELECT * FROM students ORDER BY name ASC").fetchall()
        return [Student(**dict(row)) for row in rows]


def get_student(student_id: int) -> Student | None:
    """Return one student by id, or None if there is no such student."""
    with _connect() as conn:
        row = conn.execute(
            "SELECT * FROM students WHERE id = ?", (student_id,)
        ).fetchone()
        return Student(**dict(row)) if row else None


def award_stickers(student_id: int, amount: int) -> int:
    """Add `amount` stickers to a student and return their NEW total."""
    with _connect() as conn:
        conn.execute(
            "UPDATE students SET sticker_count = sticker_count + ? WHERE id = ?",
            (amount, student_id),
        )
        row = conn.execute(
            "SELECT sticker_count FROM students WHERE id = ?", (student_id,)
        ).fetchone()
        return row["sticker_count"] if row else 0


def get_leaderboard() -> list[Student]:
    """Return all students sorted by sticker count, highest first."""
    with _connect() as conn:
        rows = conn.execute(
            "SELECT * FROM students ORDER BY sticker_count DESC, name ASC"
        ).fetchall()
        return [Student(**dict(row)) for row in rows]
