import asyncio 
from telebot.async_telebot import AsyncTeleBot

from backend.Google_classroom.client import ClientInterface
from backend.Google_classroom.assignments import CourseWork
from backend.Google_classroom.classes import Classroom

bot = AsyncTeleBot()

work  = CourseWork()
classroom = Classroom()

@bot.message_handler(commands=["tasks"])
async def send_tasks(message):
    cache = {}
    work  = CourseWork()
    cred = ClientInterface.fetch_credits()
    classroom = Classroom()
    classes: dict[str : int] = classroom.fetch_classes_and_classId(cred)
    text = ""
    for key, value in classes.items():
            all_assignments = work.fetch_assignments(cred, value)
            cache[key] = all_assignments
    

    for class_name, assignments in cache.items():
        if assignments is None:
            continue

        text += f"\n{class_name}\n"

        for assignment in assignments:
            text += f"• {assignment['title']}\n"

    await bot.reply_to(message, text)

asyncio.run(bot.polling())