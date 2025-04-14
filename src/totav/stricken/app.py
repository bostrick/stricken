#import logging
from typing import Union, Annotated

from fastapi import FastAPI, Depends
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Session, select
from pydantic import BaseModel

from totav.stricken.engine import create_db_and_tables, SessionDep
from totav.stricken.models import Organization

#logging.basicConfig(level=logging.INFO)


app = FastAPI()

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

@app.post("/org/")
def create_organization(org: Organization, session: SessionDep) -> Organization:
    session.add(org)
    session.commit()
    session.refresh(org)
    return org

@app.get("/org/")
def read_organization(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Organization]:
    orgs = session.exec(select(Organization).offset(offset).limit(limit)).all()
    return orgs

@app.get("/org/{org_id}")
def read_hero(org_id: str, session: SessionDep) -> Organization:
    org = session.get(Organization, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Org not found")
    return org

@app.delete("/orgs/{org_id}")
def delete_org(org_id: int, session: SessionDep):
    org = session.get(Organization, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="org not found")
    session.delete(org)
    session.commit()
    return {"ok": True}



@app.on_event("startup")
def on_startup():
    create_db_and_tables()