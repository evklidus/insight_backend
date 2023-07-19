from pydantic import BaseModel
from typing import List
from typing import Optional

class User(BaseModel):
    id: int
    username: str
    email: Optional[str]
    avatar_url: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]


class UserInDB(User):
    hashed_password: str

    def to_user(self):
        return User(
            username=self.username,
            email=self.email,
            avatar_url=self.avatar_url,
            first_name=self.first_name,
            last_name=self.last_name,
        )


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
