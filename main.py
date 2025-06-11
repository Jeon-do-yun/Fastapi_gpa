from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List
from fastapi.responses import JSONResponse

app = FastAPI()

# 학점 변환표
grade_to_point = {
    "A+": 4.5,
    "A": 4.0,
    "B+": 3.5,
    "B": 3.0,
    "C+": 2.5,
    "C": 2.0,
    "D+": 1.5,
    "D": 1.0,
    "F": 0.0
}

class Course(BaseModel):
    course_code: str
    course_name: str
    credits: int
    grade: str

class StudentRequest(BaseModel):
    student_id: str
    name: str
    courses: List[Course]

class StudentSummary(BaseModel):
    student_id: str
    name: str
    gpa: float
    total_credits: int

@app.post("/score")
async def student_summary(data: StudentRequest):
    total_credits = 0
    total_points = 0.0
    for course in data.courses:
        credits = course.credits
        grade = course.grade
        point = grade_to_point.get(grade, 0.0)
        total_credits += credits
        total_points += point * credits
    gpa = round(total_points / total_credits, 2) if total_credits > 0 else 0.0
    # 소수점 셋째자리에서 반올림
    gpa = round(total_points / total_credits + 1e-8, 2) if total_credits > 0 else 0.0
    summary = {
        "student_summary": {
            "student_id": data.student_id,
            "name": data.name,
            "gpa": round(total_points / total_credits + 1e-8, 2) if total_credits > 0 else 0.0,
            "total_credits": total_credits
        }
    }
    return JSONResponse(content=summary)
