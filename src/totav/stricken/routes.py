import logging
import functools
from typing import Annotated, Callable, Type

from fastapi import HTTPException, Query
from fastapi import APIRouter
from sqlmodel import select

from totav.stricken.models import Organization
from totav.stricken.models import Book
from totav.stricken.models import get_model_registry
from totav.stricken.engine import SessionDep


LOG = logging.getLogger(__name__)
router = APIRouter()

def model_get_factory(model):
    def f(obj_id: str, session: SessionDep):
        obj = session.get(model, obj_id)
        if not obj:
            raise HTTPException(status_code=404, detail=f"{model} not found")
        breakpoint()
        return obj
    return f


class RouteBinder:

    def __init__(self):
        self.router = APIRouter()
        self.registry = get_model_registry()

    def bind_all(self):
        for name, model in self.registry.items():
            self.bind_model(name, model)
        return self.router

    def bind_model(self, name, model):
        LOG.info(f"binding model {model}")
        # default getter
        #f : Callable[[str, SessionDep], Type(model)] = functools.partial(get_model, model)
        self.router.get("/foo%s/{obj_id}" % name, response_model=model)(model_get_factory(model))

# orgs

@router.post("/org/")
def create_organization(org: Organization, session: SessionDep) -> Organization:
    session.add(org)
    session.commit()
    session.refresh(org)
    return org

@router.get("/org/")
def read_organization(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Organization]:
    orgs = session.exec(select(Organization).offset(offset).limit(limit)).all()
    return orgs

@router.get("/org/{org_id}")
def read_hero(org_id: str, session: SessionDep) -> Organization:
    org = session.get(Organization, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Org not found")
    return org

@router.delete("/orgs/{org_id}")
def delete_org(org_id: str, session: SessionDep):
    org = session.get(Organization, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="org not found")
    session.delete(org)
    session.commit()
    return {"ok": True}

# books


@router.post("/book/")
def create_book(book: Book, session: SessionDep) -> Organization:
    session.add(book)
    session.commit()
    session.refresh(book)
    return book

@router.get("/book/")
def read_books(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Book]:
    books = session.exec(select(Book).offset(offset).limit(limit)).all()
    return books

@router.get("/book/{book_id}")
def read_book(book_id: str, session: SessionDep) -> Book:
    book = session.get(book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="book not found")
    return book

@router.delete("/books/{book_id}")
def delete_book(book_id: str, session: SessionDep):
    book = session.get(book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="book not found")
    session.delete(book)
    session.commit()
    return {"ok": True}