import asyncio
import aiosqlite
from datetime import datetime

from backend.Google_classroom.assignments import CourseWork
from backend.core.settings import Config
from backend.Google_classroom.client import ClientInterface


async def update_cache():
    async with aiosqlite.connect(Config.database_file_path) as db:
        await db.commit()

        work  = CourseWork()
        cred = ClientInterface.fetch_credits()

        courses = await db.execute_fetchall(
            """
                SELECT * FROM Courses
            """, 
            )
        
        for course_id, course_name in courses: # in tuple(id, name)
            all_assignments = work.fetch_assignments(cred, course_id)

            if not all_assignments:
                continue

            for assignment in all_assignments:
                await db.execute("""
                    INSERT INTO CourseWork(work_id, course_id, title, due_date, status) 
                    VALUES(?, ?, ?, ?, ?) ON CONFLICT(work_id) DO UPDATE SET status = excluded.status
                """, 
                (str(assignment["id"]),
                    str(course_id), 
                    str(assignment["title"]), 
                    str(assignment["due_date"]), 
                    str(assignment["status"])))
        
        await db.commit()
        print(f"UPDATED DATABASE: {datetime.now()}")
        return

async def cache_scheduler():
    while True:
        now = datetime.now()

        if now.hour == Config.time_hour and now.minute == Config.time_min:
            await update_cache()

            await asyncio.sleep(60)
            continue

        print()
        await asyncio.sleep(60)
