from pydantic import BaseModel
from typing import List

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str

class UserInDB(User):
    hashed_password: str

class Category(BaseModel):
    name: str
    imageUrl: str
    tag: str

class CoursePreview(BaseModel):
    id: int
    imageUrl: str
    name: str
    tag: str

class Lesson(BaseModel):
    name: str
    videoUrl: str

class CoursePage(BaseModel):
    id: int
    imageUrl: str
    name: str
    lessons: List[Lesson]