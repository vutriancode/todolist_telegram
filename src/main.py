from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from api.task import Task
from fastapi.middleware.cors import CORSMiddleware
from pydantic import validator
from datetime import datetime
from api.db import save_task, get_tasks, get_task_by_id, update_task, delete_task

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # or specify certain domains, e.g., ["https://yourdomain.com"]
    allow_credentials=True,
    allow_methods=["*"],      # or specify ["GET", "POST", "OPTIONS"] etc.
    allow_headers=["*"],      # or specify the needed headers
)

class TaskModel(BaseModel):
    id: Optional[int] = 0
    title: str
    description: str
    due_date: datetime
    priority: Optional[str] = "Normal"
    tags: List[str] = []
    completed: bool = False
    recurrence: str = "once"
    # @validator("recurrence")
    # def validate_recurrence(cls, value):
    #     if value not in ["once", "daily", "weekly", "monthly", "yearly"]:
    #         raise ValueError("Invalid recurrence value")
    #     return value

@app.get("/tasks")
def list_tasks():
    tasks = get_tasks()
    print([t.__dict__ for t in tasks])
    return [t.__dict__ for t in tasks]

@app.post("/tasks")
def create_task(task_data: TaskModel):
    new_task = Task(**task_data.dict())
    save_task(new_task)
    return {"message": "Task created", "task": new_task.__dict__}

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = get_task_by_id(task_id)
    return task.__dict__

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_data: TaskModel):
    task = Task(**task_data.dict())
    update_task(task_id, task)
    return {"message": "Task updated"}

@app.delete("/tasks/{task_id}")
def delete_task_with_id(task_id: int):
    delete_task(task_id)
    return {"message": "Task deleted"}
#run by uvicorn python code
#uvicorn main:app --reload
#http://localhost:8000/docs
