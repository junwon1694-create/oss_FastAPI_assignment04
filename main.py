import json
from pathlib import Path
from typing import Any, Dict, List

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()
DATA_FILE = Path("courses.json")


class Course(BaseModel):
    course_name: str
    year: str
    semester: str
    grade: str


def load_courses() -> List[Dict[str, Any]]:
    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="courses.json 파일 형식이 올바르지 않습니다.")

    if not isinstance(data, list):
        raise HTTPException(status_code=500, detail="courses.json의 최상위 구조는 list여야 합니다.")

    return data


def save_courses(courses: List[Dict[str, Any]]) -> None:
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(courses, f, ensure_ascii=False, indent=2)


@app.get("/")
async def welcome() -> Dict[str, str]:
    return {"msg": "FastAPI course records server"}


@app.get("/courses")
async def get_courses() -> List[Dict[str, Any]]:
    return load_courses()


@app.post("/courses")
async def add_course(course: Course) -> Dict[str, Any]:
    courses = load_courses()

    if hasattr(course, "model_dump"):
        new_course = course.model_dump()
    else:
        new_course = course.dict()

    courses.append(new_course)
    save_courses(courses)

    return {
        "msg": "course added successfully",
        "course": new_course,
        "count": len(courses),
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)