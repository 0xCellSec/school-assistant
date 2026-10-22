from pydantic import BaseModel

class Courses(BaseModel):
    class_id: int
    name: str


class CourseWork(BaseModel):
    work_id: int
    title: str
    due_date: dict
    status: str