# Needed modules
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


class Task(BaseModel):
    task_title: str
    task_desc: str
    is_finished: bool = False


task_db = [
    {"task_id": 1, 
     "task_title": "Laboratory Activity", 
     "task_desc": "Create Lab Act 2", 
     "is_finished": False}
]

# GET implementation 
@app.get("/tasks/{task_id}")
def get_task(task_id: Optional[int] = None):
    if task_id:
        # Look for the task by it's  task_id
        for u in task_db:
            if u["task_id"] == task_id:
                return {"status": "ok", "result": u}
        # If task is not found, return an error
        raise HTTPException(status_code=404, detail={"error": "Task not found"})
    
    # Return all tasks if no task_id is provided
    return {"status": "ok", "result": task_db}

# POST implementation
@app.post("/tasks")
def create_task(task: Task):
    # generate a new task ID
    new_task_id = max([u["task_id"] for u in task_db], default=0) + 1

    # Create a new task with the generated new ID
    new_task = {"task_id": new_task_id, **task.dict()}
    task_db.append(new_task)
    
    return {"status": "ok", "task": new_task}

# DELETE implementation
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int): 
    for idx, u in enumerate(task_db):
        if u["task_id"] == task_id:
            # Remove the task from the database task_db
            removed_task = task_db.pop(idx)
            return {"status": "ok", "removed_data": removed_task}

    # If task is not found, return an error
    raise HTTPException(status_code=404, detail={"error": "Task not found. Record can not be deleted"})

# PATCH implementation to update parts of a task by ID
@app.patch("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    for idx, u in enumerate(task_db):
        if u["task_id"] == task_id:
            # Update the task details
            task_db[idx]["task_title"] = task.task_title
            task_db[idx]["task_desc"] = task.task_desc
            task_db[idx]["is_finished"] = task.is_finished
            
            return {"status": "ok", "updated_data": task_db[idx]}
    
    # If task is not found, return an error
    raise HTTPException(status_code=404, detail={"error": "Task not found. Record can not be deleted"})
