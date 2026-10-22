import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


from backend.Google_classroom.classes import Classroom
from backend.Google_classroom.assignments import CourseWork

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
if __name__ == "__main__":
    cache = {}
    work  = CourseWork()
    cred = ClientInterface.fetch_credits()
    classroom = Classroom()
    classes: dict[str : int] = classroom.fetch_classes_and_classId(cred)
    for key, value in classes.items():
        all_assignments = work.fetch_assignments(cred, value)
        cache[key] = all_assignments

    print(cache)