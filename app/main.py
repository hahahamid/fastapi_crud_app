from fastapi import FastAPI, HTTPException
from . import schemas
from typing import List, Optional

app = FastAPI()

items = []
last_id = 0

@app.get("/items", response_model=List[schemas.Item])
async def read_items(skip: int = 0, limit: int = 10, name: Optional[str] = None):
    filtered_items = items
    if name:
        filtered_items = [item for item in items if name.lower() in item.name.lower()]
    return filtered_items[skip: skip + limit]


@app.get("/items/{item_id}", response_model=schemas.Item)
async def read_item(item_id: int):
    for item in items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")


@app.post("/items", response_model=schemas.Item, status_code=201)
async def create_item(item: schemas.Item):
    global last_id
    last_id += 1
    item_dict = item.dict()
    item_dict["id"] = last_id
    new_item = schemas.Item(**item_dict)
    items.append(new_item)
    return new_item

@app.put("/items/{item_id}", response_model=schemas.Item)
async def update_item(item_id: int, item: schemas.Item):
    for i, stored_item in enumerate(items):
        if stored_item.id == item_id:
            items[i] = item
            items[i].id = item_id  
            return items[i]
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    for i, stored_item in enumerate(items):
        if stored_item.id == item_id:
            del items[i]
            return {"message": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")