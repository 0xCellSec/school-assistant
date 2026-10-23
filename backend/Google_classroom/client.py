import os
import aiosqlite

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


from backend.Google_classroom.classes import Classroom
from backend.Google_classroom.assignments import CourseWork
from backend.core.settings import Config
from backend.core import database

SCOPES = ["https://www.googleapis.com/auth/classroom.courses.readonly", "https://www.googleapis.com/auth/classroom.coursework.me",]

class ClientInterface():
    def fetch_credits() -> Credentials:
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", scopes=SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                 "cred.json", SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open("token.json", "w") as token:
                token.write(creds.to_json())

        return creds

    async def init_cache():
        async with aiosqlite.connect(Config.database_file_path) as db:
            await db.executescript(database.SCHEMA)
            await db.commit()

            work  = CourseWork()
            cred = ClientInterface.fetch_credits()
            classroom = Classroom()
            classes: dict[str : int] = classroom.fetch_classes_and_classId(cred)
            for course_name, course_id in classes.items():
                all_assignments = work.fetch_assignments(cred, course_id)
                await db.execute(""" INSERT INTO Courses(course_id, course_name) 
                                    VALUES(?, ?) ON CONFLICT(course_id) DO NOTHING""", (course_id, course_name)) 

                if not all_assignments:
                    continue

                for assignment in all_assignments:
                    await db.execute("""
                        INSERT INTO CourseWork(work_id, course_id, title, due_date, status) 
                        VALUES(?, ?, ?, ?, ?) ON CONFLICT(work_id) DO NOTHING
                    """, 
                    (str(assignment["id"]),
                     str(course_id), 
                     str(assignment["title"]), 
                     str(assignment["due_date"]), 
                     str(assignment["status"])))
            
            await db.commit()
            print("DATABASE CAHCE STARTUP COMPLETE")
            return


"""if __name__ == "__main__":
    cache = {}
    work  = CourseWork()
    cred = ClientInterface.fetch_credits()
    classroom = Classroom()
    classes: dict[str : int] = classroom.fetch_classes_and_classId(cred)
    for key, value in classes.items():
        all_assignments = work.fetch_assignments(cred, value)
        cache[key] = all_assignments

    print(cache)"""