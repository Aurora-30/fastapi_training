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
class User(BaseModel):
    name: str
    age: int
    grade: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    grade: Optional[str] = None

# Fake database
users_db = []
next_id = 1

# CREATE - POST method
@app.post("/users", tags=["Create"])
async def create_user(user: User):
    global next_id
    new_user = {
        "id": next_id,
        "name": user.name,
        "age": user.age,
        "grade": user.grade
    }
    users_db.append(new_user)
    next_id += 1
    return {"message": "User created", "user": new_user}

    # READ - GET methods
@app.get("/users", tags=["Read"])
async def get_all_users():
    return {"users": users_db}

@app.get("/users/{user_id}", tags=["Read"])
async def get_user(user_id: int):
    for user in users_db:
        if user["id"] == user_id:
            return {"user": user}
    return {"error": "User not found"}

    # UPDATE - PUT method (complete update)
@app.put("/users/{user_id}", tags=["Update"])
async def update_user(user_id: int, user_updates: UserUpdate):
    for i, user in enumerate(users_db):
        if user["id"] == user_id:
            # Only update fields that are provided
            if user_updates.name is not None:
                users_db[i]["name"] = user_updates.name
            if user_updates.age is not None:
                users_db[i]["age"] = user_updates.age
            if user_updates.grade is not None:
                users_db[i]["grade"] = user_updates.grade
            return {"message": "User updated", "user": users_db[i]}
    return {"error": "User not found"}

    # DELETE - DELETE method
@app.delete("/users/{user_id}", tags=["Delete"])
async def delete_user(user_id: int):
    for i, user in enumerate(users_db):
        if user["id"] == user_id:
            deleted_user = users_db.pop(i)
            return {"message": "User deleted", "user": deleted_user}
    return {"error": "User not found"}