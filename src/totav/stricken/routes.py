from typing import Annotated

from fastapi import HTTPException, Query
from fastapi import APIRouter
from sqlmodel import select

from totav.stricken.models import Organization
from totav.stricken.models import Book
from totav.stricken.engine import SessionDep

router = APIRouter()

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