
from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, Field
from starlette import status
from sqlalchemy import select

from .routers import auth
from . import models
from .models import Todos
from .database import engine
from .dependencies import db_dependency


class TodoDTO(BaseModel):
  id: int | None = Field(default=None, gt=0)
  title: str = Field(min_length=3, max_length=50)
  description: str = Field(min_length=3, max_length=100)
  priority: int = Field(gt=0, le=5)
  completed: bool = False

  class Config:
      orm_mode = True


def create_app():
  app = FastAPI()
  app.include_router(auth.router, prefix="/auth", tags=["auth"])
  
  return app


models.Base.metadata.create_all(bind=engine)

app = create_app()

@app.get("/", status_code=status.HTTP_200_OK)
async def get_all_todos(db: db_dependency) -> list[TodoDTO]:
  return db.query(Todos).all()


@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo(db: db_dependency, todo_id: int = Path(gt=0)) -> TodoDTO:
  found_todo = db.query(Todos).filter(Todos.id == todo_id).first()
  if found_todo is not None:
    return found_todo
  raise HTTPException(status_code=404, detail="Todo not found")


@app.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo: TodoDTO):
  new_todo = Todos(**todo.model_dump())
  
  db.add(new_todo)
  db.commit()
  db.refresh(new_todo)
  return new_todo


@app.put("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def update_todo(db: db_dependency, todo: TodoDTO, todo_id: int = Path(gt=0)) -> TodoDTO:
  found_todo = db.query(Todos).filter(Todos.id == todo_id).first()
  if found_todo is None:
    raise HTTPException(status_code=404, detail="Todo not found")

  found_todo.title = todo.title
  found_todo.description = todo.description
  found_todo.priority = todo.priority
  found_todo.completed = todo.completed
  
  db.add(found_todo)
  db.commit()
  db.refresh(found_todo)
  return found_todo

@app.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
  found_todo = db.query(Todos).filter(Todos.id == todo_id).first()
  if found_todo is None:
    raise HTTPException(status_code=404, detail="Todo not found")

  db.delete(found_todo)
  db.commit()
  return None