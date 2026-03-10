from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class ItemBase(BaseModel):
    itemname: str
    quantity: int

def getdb():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependancy = Annotated[Session,Depends(getdb)]


@app.get("/items/{item_id}",status_code=status.HTTP_200_OK)
async def read_item(item_id: int, db: db_dependancy):
    item = db.query(models.Item).filter(models.Item.id==item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail='Item not found.')
    return item

@app.post("/items", status_code=status.HTTP_201_CREATED)
async def add_item(item: ItemBase, db: db_dependancy):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()

@app.delete("/items/{item_id}",status_code=status.HTTP_200_OK)
async def delete_item(item_id: int, db: db_dependancy):
    item = db.query(models.Item).filter(models.Item.id==item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail='Item not found.')
    db.delete(item)
    db.commit()