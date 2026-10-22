
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from backend.core.settings import Config

class Classroom:
    def is_class_allowed(self, course_name: str):
        allowed_courses: list = Config.allowed_courses
        if course_name in allowed_courses:
            return True
        return False
    
    def fetch_classes_and_classId(self, cred: Credentials) -> dict:
        data = {}
        try:
            service = build("classroom", "v1", credentials=cred)
            results = service.courses().list(pageSize=10).execute()
            courses = results.get("courses", [])
        
            if not courses:
                print("NONE")
                return
            print("Courses:")

            for course in courses:
                if self.is_class_allowed(course["name"]):
                    print(course["name"], course["id"])
                    data[course["name"]] = course["id"]

                    print(data)

        except(HttpError):
            print("httperror")

        return data

