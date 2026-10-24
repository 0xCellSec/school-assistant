import asyncio 
import aiosqlite
import ast
from datetime import datetime

from backend.core.settings import Config




async def test_cache_fetching():
    async with aiosqlite.connect(Config.database_file_path) as db:
            courses = await db.execute_fetchall(
            """
                SELECT * FROM Courses
            """, 
            )


            print(f"COURSES: {courses}")
            for course_id, course_name in courses: # every tuple in list
                text = ""
                print(f"{course_id} - {course_name}\n")
                assignments = await db.execute_fetchall(
                    """ SELECT * FROM CourseWork WHERE course_id = ? AND status = 'NOT TURNED IN' AND due_date != 'No Due Date' """, 
                    [course_id, ]
                )
                if assignments is None:
                    continue
                text += f"\n{course_name}\n"

                for assignment in assignments:
                    if assignment[3] != "No Due Date":
                        due_date_dict = ast.literal_eval(assignment[3])
                        due = datetime(due_date_dict['year'], due_date_dict['month'], due_date_dict['day'])

                        if due.date() < datetime.now().date():
                            continue
                        
                        due_date = f"{due_date_dict['day']}-{due_date_dict['month']}-{due_date_dict['year']}"

                    else: 
                         due_date = "None"

                    text += f"• {assignment[2]} DUE: {due_date}\n"

                    if not text:
                        print("text error")

                print(text)


asyncio.run(test_cache_fetching())