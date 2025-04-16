#import logging
import contextlib
from typing import Union, Annotated

from fastapi import FastAPI, Depends
from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel

from totav.stricken.engine import create_db_and_tables, SessionDep
from totav.stricken.routes import router, RouteBinder
from totav.stricken.auth import router as auth_router

#logging.basicConfig(level=logging.INFO)


@contextlib.asynccontextmanager
async def app_lifespan(app: FastAPI):
    router = RouteBinder().bind_all()
    breakpoint()
    app.include_router(router)
    yield

#app = FastAPI(lifespan=app_lifespan)
app = FastAPI()

app.include_router(auth_router)
app.include_router(router)
app.include_router(RouteBinder().bind_all())

#SessionDep = Annotated[Session, Depends(get_session)]



class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

@app.on_event("startup")
def on_startup():
    create_db_and_tables()