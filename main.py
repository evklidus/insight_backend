import re
from fastapi import FastAPI, HTTPException, Request, Response
from starlette.responses import StreamingResponse
from models import *
from fastapi.responses import StreamingResponse
from pathlib import Path
from app.core.controllers.router import api_router

app = FastAPI()

app.include_router(api_router)

categories = [
    Category(name= "Спорт", image_url= "https://images.unsplash.com/photo-1518611012118-696072aa579a?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=3540&q=80", tag= "sport"),
    Category(name= "Программирование", image_url= "https://images.unsplash.com/photo-1605379399642-870262d3d051?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=3893&q=80", tag= "programming")
]

coursePreviews = [
    CoursePreview(id= 1, image_url= "https://www.apple.com/v/apple-fitness-plus/l/images/meta/apple-fitness-plus__eafl9rq9woom_og.png", name= "Пилатес от Веты", tag= "sport"),
    CoursePreview(id= 2, image_url= "https://avatars.yandex.net/get-music-content/118603/e9de54a9.p.4465783/m1000x1000", name= "Mr. Miyagi", tag= "sport"),
    CoursePreview(id= 3, image_url= "https://logowik.com/content/uploads/images/flutter5786.jpg", name= "Flutter", tag= "programming")
]

coursePages = [
    CoursePage(id= 1, image_url= "https://media1.popsugar-assets.com/files/thumbor/v8KPX6IRPz1wie9wQvhB4iYTdcw/fit-in/2048xorig/filters:format_auto-!!-:strip_icc-!!-/2018/07/30/638/n/1922564/8d1b02c5595eaf1f_GettyImages-1007595384/i/Kim-Kardashian-Blue-PVC-Heels-From-Yeezy.jpg", name= "Пилатес от Веты", lessons= [Lesson(name= "Первый день", video_url= "http://0.0.0.0:8080/videos/0")]),
    CoursePage(id= 2, image_url= "https://news.store.rambler.ru/img/dc3b4493acdf7bb2208582027eb15ebd?img-format=auto&img-1-resize=height:355,fit:max&img-2-filter=sharpen", name= "Mr. Miyagi", lessons= [Lesson(name= "Minor", video_url= "http://0.0.0.0:8080/videos/1")])
]

videos = [
    "The Kardashians _ Season 3 Returns May 25 _ Hulu.mp4",
    "Miyagi & Andy Panda - Minor (Mood Video).mp4"
]

@app.get("/categories")
async def get_categories():
    return categories
    
@app.get("/course_previews/{category_tag}")
async def get_course_previews_by_category(category_tag: str):
    course_previews_by_category = []
    for coursePreview in coursePreviews:
        if coursePreview.tag == category_tag:
            course_previews_by_category.append(coursePreview)
    if len(course_previews_by_category) != 0:
        return course_previews_by_category
    else:
        return {"message": "Course previews not found"}

@app.get("/courses/{courseId}")
async def get_course_page_by_id(courseId: int):
    for coursePage in coursePages:
        if coursePage["id"] == courseId:
            return coursePage
    return {"message": "Please course is still building..."}

@app.get("/course_pages/{id}")
def get_course_page_by_id(id: int):
    for course_page in coursePages:
        if course_page.id == id:
            return course_page
    raise HTTPException(status_code=404, detail="Course page not found")
    
@app.get("/videos/{index}")
def get_video_by_id(request: Request, index: int):
    video_path = Path("assets/videos/" + videos[index])

    if not video_path.exists():
        return Response(status_code=404)

    range_header = request.headers.get('Range')

    if range_header:
        range_match = re.match(r'bytes=(\d+)-(\d*)', range_header)

        if range_match:
            start = int(range_match.group(1))
            end = int(range_match.group(2)) if range_match.group(2) else None
            file_size = video_path.stat().st_size

            if end is None or end >= file_size:
                end = file_size - 1

            headers = {
                'Content-Range': f'bytes {start}-{end}/{file_size}',
                'Accept-Ranges': 'bytes',
                'Content-Length': str(end - start + 1),
                'Content-Type': 'video/mp4',
            }

            return StreamingResponse(
                iter_video_chunks(video_path, start, end),
                media_type='video/mp4',
                headers=headers,
                status_code=206
            )

    headers = {
        'Content-Length': str(video_path.stat().st_size),
        'Content-Type': 'video/mp4',
    }

    return StreamingResponse(
        video_path.open('rb'),
        media_type='video/mp4',
        headers=headers,
        status_code=200
    )


def iter_video_chunks(video_path: Path, start: int, end: int, chunk_size: int = 8192):
    with video_path.open('rb') as video_file:
        video_file.seek(start)
        remaining_bytes = end - start + 1

        while remaining_bytes > 0:
            chunk = video_file.read(min(chunk_size, remaining_bytes))
            if not chunk:
                break
            yield chunk
            remaining_bytes -= len(chunk)