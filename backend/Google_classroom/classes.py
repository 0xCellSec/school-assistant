import yaml

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

with open("config.yaml", "r") as file:
    Config = yaml.safe_load(file)

class Classroom:
    def is_class_allowed(self, course_name: str):
        allowed_courses: list = Config["allowed_courses"]
        if course_name in allowed_courses:
            return True
        return False
    
    def fetch_classes_and_classId(self, cred: Credentials) -> dict[str : int]:
        data = {}
        try:
            service = build("classroom", "v1", credentials=cred)
            results = service.courses().list(pageSize=10).execute()
            courses = results.get("courses", [])
        
            if not courses:
                return

            for course in courses:
                if self.is_class_allowed(course["name"]):
                    data[course["name"]] = course["id"]

        except(HttpError):
            print("httperror")

        return data

