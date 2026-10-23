import asyncio 
from telebot.async_telebot import AsyncTeleBot

from backend.Google_classroom.client import ClientInterface
from backend.Google_classroom.assignments import CourseWork
from backend.Google_classroom.classes import Classroom
from backend.core.settings import Config

bot = AsyncTeleBot(Config.telegram_bot_key)

work  = CourseWork()
classroom = Classroom()

@bot.message_handler(commands=["tasks"])
async def send_tasks(message):
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
                        """ SELECT * FROM CourseWork WHERE course_id = ? AND status = 'NOT TURNED IN'""", 
                        [course_id, ]
                    )
                    if assignments is None:
                        continue
                    text += f"\n{course_name}\n"
    
                    for assignment in assignments:
                        if assignment[3] != "No Due Date":
                            due_date_dict = ast.literal_eval(assignment[3])
                            due_date = f"{due_date_dict['day']}-{due_date_dict['month']}-{due_date_dict['year']}"
    
                        else: 
                             due_date = "None"
    
                        text += f"• {assignment[2]} DUE: {due_date}\n"
    
                        if not text:
                            print("text error")
    
                    print(text)
                    await bot.reply_to(message, text)


async def start():
    await asyncio.gather(bot.polling(), ClientInterface.init_cache())

asyncio.run(start())