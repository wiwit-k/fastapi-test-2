from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Todo
from schemas import TodoCreate, TodoResponse, TodoUpdate


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # หรือใส่ URL ของ Frontend เช่น ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # อนุญาตทุก Method (GET, POST, PUT, DELETE ฯลฯ)
    allow_headers=["*"],
)


"""class Item(BaseModel):
    id: int
    name: str

items = [
    {
        "id": 101,
        "name": "television"
    },
    {
        "id": 102,
        "name": "radio"
    }
]"""

todos = [
    {"name": "Sports", "description": "Go to the gym"},
    {"name": "Read", "description": "Read 10 pages"},
]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def index():
    return {"Hello": "World"}


@app.get('/todos', response_model=List[TodoResponse])
def get_all_todos(db: Session = Depends(get_db)):
    return db.query(Todo).all()


@app.get('/todos/{todo_id}', response_model=TodoResponse)
def get_todo_by_id(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@app.post('/todos', status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = Todo(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return {"id": db_todo.id, "message": "Created successfully"}


@app.put('/todos/{todo_id}', response_model=TodoResponse)
def update_todo(todo_id: int, todo_update: TodoUpdate, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    update_data = todo_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_todo, key, value)

    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.delete('/todos/{todo_id}')
def delete_todo_by_id(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return {"message": "Todo deleted"}



""" @app.get('/mile-to-kilometer')
def mileToKilometer(mile: float):
    return mile/0.621371

@app.get('/fahrenheit-to-celsius')
def fahrenheitToCelsius(f: float):
    return (f - 32.0)*5.0/9.0 """

"""@app.post('/items')
def create_item(item: Item):
    items.append(item)
    return item

@app.delete('/items/{pos}')
def delete_item(pos: int):
    items.pop(pos)
    return items"""

""" @app.post('/items')
async def create_item(request: Request):
    body = await request.json()
    return {"request body": body} """

