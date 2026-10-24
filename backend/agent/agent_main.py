import asyncio 
import aiosqlite
import ast
from datetime import datetime
from telebot.async_telebot import AsyncTeleBot

import yaml 

from backend.Google_classroom.client import ClientInterface
from backend.core.scheduler import cache_scheduler


with open("config.yaml", "r") as file:
    Config = yaml.safe_load(file)


bot = AsyncTeleBot(Config["telegram_bot_key"])

async def fetch_work() -> list:
    packed_work = []
    async with aiosqlite.connect(Config["database_file_path"]) as db:
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
                """ SELECT * FROM CourseWork WHERE course_id = ? AND status = 'NOT TURNED IN' AND due_date != 'No Due Date'""", 
                [course_id, ]
            )
            if not assignments:
                continue

            assignment_text = ""
            for assignment in assignments:
                if assignment[3] != "No Due Date":
                    due_date_dict = ast.literal_eval(assignment[3])
                    due = datetime(due_date_dict['year'], due_date_dict['month'], due_date_dict['day'])

                    if due.date() < datetime.now().date():
                        continue
                    
                    due_date = f"{due_date_dict['day']}-{due_date_dict['month']}-{due_date_dict['year']}"

                else: 
                    due_date = "None"

                assignment_text += f"• {assignment[2]} DUE: {due_date}\n"

            if not assignment_text:
                continue

            text = f"\n{course_name} \n\n{assignment_text}"
            packed_work.append(text)

    return packed_work

     

@bot.message_handler(commands=["tasks"])
async def send_tasks(message):
    work_list = await fetch_work()

    for text in work_list:
        await bot.reply_to(message, text)

async def send_scheduled_task():
     work_list = await fetch_work()
     for text in work_list:                     
        bot.send_message(text=text)

async def start():
    await ClientInterface.init_cache()
    scheduler_task =  asyncio.create_task(cache_scheduler())

    print("STARTING POLLING")
    await asyncio.gather(bot.polling())

asyncio.run(start())