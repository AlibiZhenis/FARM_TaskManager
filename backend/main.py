from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

from database import *

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/todo")
async def read_todo():
    response = await fetch_all()
    return response


@app.get("/todo/{todo_title}", response_model=Todo)
async def read_todo_title(todo_title: str):
    response = await fetch_one(todo_title)
    if response:
        return response
    raise HTTPException(404, f"There is no todo with the title {todo_title}")


@app.post("/todo", response_model=Todo)
async def create_todo(todo: Todo):
    response = await create_one(todo.dict())
    if response:
        return response
    raise HTTPException(400, "Something went wrong")


@app.put("/todo/{todo_title}", response_model=Todo)
async def update_todo(todo_title: str, desc: str):
    response = await update_one(todo_title, desc)
    if response:
        return response
    raise HTTPException(404, f"There is no todo with the title {todo_title}")


@app.delete("/todo/{todo_title}")
async def delete_todo_id(todo_title: str):
    response = await remove_one(todo_title)
    if response:
        return "Successfully deleted todo"
    raise HTTPException(404, f"There is no todo with the title {todo_title}")
