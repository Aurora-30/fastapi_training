from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

# Initialize FastAPI app
app = FastAPI(
    title="Student Management API (In-Memory)",
    description="API to Manage Student Records",
    version="0.1.0",
)

# Data model
class student(BaseModel):
    name: str
    age: int
    grade: str

class studentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    grade: Optional[str] = None

# Fake database
student_db = []
next_id = 1

# CREATE - POST method
@app.post("/student", tags=["Create"])
async def create_student(student: student):
    global next_id
    new_student = {
        "id": next_id,
        "name": student.name,
        "age": student.age,
        "grade": student.grade
    }
    student_db.append(new_student)
    next_id += 1
    return {"message": "student created", "student": new_student}

    # READ - GET methods
@app.get("/student", tags=["Read"])
async def get_all_student():
    return {"student": student_db}

@app.get("/student/{student_id}", tags=["Read"])
async def get_student(student_id: int):
    for student in student_db:
        if student["id"] == student_id:
            return {"student": student}
    return {"error": "student not found"}

    # UPDATE - PUT method (complete update)
@app.put("/student/{student_id}", tags=["Update"])
async def update_student(student_id: int, student_updates: studentUpdate):
    for i, student in enumerate(student_db):
        if student["id"] == student_id:
            # Only update fields that are provided
            if student_updates.name is not None:
                student_db[i]["name"] = student_updates.name
            if student_updates.age is not None:
                student_db[i]["age"] = student_updates.age
            if student_updates.grade is not None:
                student_db[i]["grade"] = student_updates.grade
            return {"message": "student updated", "student": student_db[i]}
    return {"error": "student not found"}

    # DELETE - DELETE method
@app.delete("/student/{student_id}", tags=["Delete"])
async def delete_student(student_id: int):
    for i, student in enumerate(student_db):
        if student["id"] == student_id:
            deleted_student = student_db.pop(i)
            return {"message": "student deleted", "student": deleted_student}
    return {"error": "student not found"}