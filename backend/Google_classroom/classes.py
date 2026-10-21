
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError




class Classroom:
    def fetch_classes_and_classId(cred: Credentials) -> dict:
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
                print(course["name"], course["id"])
                data[course["name"]] = course["id"]

            print(data)

        except(HttpError):
            print("httperror")

        return data

