from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Step 1 Create SQLAlchemy engine


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # หรือใส่ URL ของ Frontend เช่น ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # อนุญาตทุก Method (GET, POST, PUT, DELETE ฯลฯ)
    allow_headers=["*"],
)


class Item(BaseModel):
    name: str
    price: float

data = [
    {
        "id": 1,
        "name": "television"
    },
    {
        "id": 2,
        "name": "radio"
    }
]

@app.get('/')
def home():
    return {"Hello": "World"}


@app.get('/hello')
def hello():
    return {"message": "Hello"}

@app.get('/items')
def get_items():
    return data

@app.post('/items')
def create_item(item: Item):
    print(item.name, item.price)
    return item

@app.delete('/items/{id}')
def delete_item(id: int):
    return {"message": ""}


""" @app.post('/items')
async def create_item(request: Request):
    body = await request.json()
    return {"request body": body} """

