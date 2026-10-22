import aiosqlite

from collections.abc import AsyncIterator
from backend.core.settings import Config


DATABASE_PATH = Config.database_file_path

SCHEMA = """
CREATE TABLE IF NOT EXISTS Courses (
    course_id   TEXT PRIMARY KEY,
    course_name TEXT NOT NULL,
);

CREATE TABLE IF NOT EXISTS CourseWork (
    work_id      TEXT NOT NULL UNIQUE,
    course_id    TEXT NOT NULL, 
    title        TEXT NOT NULL,
    due_date     TEXT NOT NULL,
    status       TEXT NOT NULL,
    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
);

"""


async def init_db() -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.executescript(SCHEMA)
        await db.execute("PRAGMA journal_mode=WAL")
        await db.execute("PRAGMA foreign_keys=ON")
        await db.commit()

async def get_db() -> AsyncIterator[aiosqlite.Connection]:
    db = await aiosqlite.connect(DATABASE_PATH)
    db.row_factory = aiosqlite.Row
    await db.execute("PRAGMA foreign_keys=ON")
    try:
        yield db
    finally:
        await db.close()