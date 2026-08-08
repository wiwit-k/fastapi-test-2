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
    id: int
    name: str

data = [
    {
        "id": 101,
        "name": "television"
    },
    {
        "id": 102,
        "name": "radio"
    }
]

@app.get('/')
def home():
    return {"Hello": "World"}

@app.get('/items')
def get_items():
    return data

@app.get('/mile-to-kilometer')
def mileToKilometer(mile: float):
    return mile/0.621371

@app.get('/fahrenheit-to-celsius')
def fahrenheitToCelsius(f: float):
    return (f - 32.0)*5.0/9.0

@app.post('/items')
def create_item(item: Item):
    data.append(item)
    return item

@app.delete('/items/{pos}')
def delete_item(pos: int):
    data.pop(pos)
    return data


""" @app.post('/items')
async def create_item(request: Request):
    body = await request.json()
    return {"request body": body} """

