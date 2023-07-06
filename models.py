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

    def to_user(self):
        return User(username=self.username)


class Category(BaseModel):
    name: str
    image_url: str
    tag: str

class CoursePreview(BaseModel):
    id: int
    image_url: str
    name: str
    tag: str

class Lesson(BaseModel):
    name: str
    video_url: str

class CoursePage(BaseModel):
    id: int
    image_url: str
    name: str
    lessons: List[Lesson]