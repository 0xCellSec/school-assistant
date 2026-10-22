import asyncio

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

class CourseWork:
    def is_assignment_turned_in(self, cred, class_id, assignment_id) -> bool:
        service = build("classroom", "v1", credentials=cred)
        results = service.courses().courseWork().studentSubmissions().list(courseId=class_id, courseWorkId=assignment_id).execute()
        assignment = results.get("studentSubmissions", [])

        #print(assignment)
        status = assignment[0]["state"]
        if status == "TURNED_IN":
            return True

        return False


    def fetch_assignments(self, cred: Credentials, id) -> dict:
        
        service = build("classroom", "v1", credentials=cred)
        results = service.courses().courseWork().list(courseId=id).execute()
        assignments = results.get("courseWork", [])

        assignments_dict = []
        due_date = None
        status = "NOT TURNED IN"
        for i, item in enumerate(assignments):
            assignment_id  = assignments[i]["id"]
            title = assignments[i]["title"]

            if self.is_assignment_turned_in(cred, id, assignment_id):
                status = "TURNED IN"
                return

            try: 
                due_date = assignments[0]["dueDate"]
            except(KeyError):
                due_date = "No Due Date"

            
            assignments_dict.append({"id": assignment_id, "title": title, "due_date": due_date})

            if not assignments:
                return
        
        return assignments_dict
        