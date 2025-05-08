from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List
from jose import JWTError, jwt
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")
SECRET_KEY = os.getenv("JWT_SECRET", "devsecret")
ALGORITHM = "HS256"

users = []
tasks = []

class User(BaseModel):
    username: str
    password: str

class Task(BaseModel):
    id: int
    title: str
    username: str

class TaskIn(BaseModel):
    title: str

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")

@app.post("/signup")
def signup(user: User):
    if any(u["username"] == user.username for u in users):
        raise HTTPException(status_code=400, detail="User already exists")
    users.append(user.dict())
    return {"message": "User created"}

@app.post("/signin")
def signin(user: User):
    for u in users:
        if u["username"] == user.username and u["password"] == user.password:
            token = jwt.encode({"sub": user.username}, SECRET_KEY, algorithm=ALGORITHM)
            return {"token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/tasks", response_model=List[Task])
def get_tasks(username: str = Depends(get_current_user)):
    return [t for t in tasks if t["username"] == username]

@app.post("/tasks")
def add_task(task_in: TaskIn, username: str = Depends(get_current_user)):
    task_id = len(tasks) + 1
    task = {"id": task_id, "title": task_in.title, "username": username}
    tasks.append(task)
    return {"message": "Task added", "task": task}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, username: str = Depends(get_current_user)):
    for i, t in enumerate(tasks):
        if t["id"] == task_id and t["username"] == username:
            tasks.pop(i)
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: TaskIn, username: str = Depends(get_current_user)):
    for task in tasks:
        if task["id"] == task_id and task["username"] == username:
            task["title"] = updated_task.title
            return {"message": "Task updated", "task": task}
    raise HTTPException(status_code=404, detail="Task not found")