from fastapi import FastAPI, Request
from pydantic import BaseModel

# Step 1 Create SQLAlchemy engine

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.get('/')
def home():
    return {"Hello": "World"}


@app.get('/hello')
def hello():
    return {"message": "Hello"}


@app.post('/items')
def create_item(item: Item):
    print(item.name, item.price)
    return item

""" @app.post('/items')
async def create_item(request: Request):
    body = await request.json()
    return {"request body": body} """

