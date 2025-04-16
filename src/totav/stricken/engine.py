from typing import Annotated
import os
import logging 
from contextlib import contextmanager

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

LOG = logging.getLogger(__name__)

db_url = os.environ.get("STRICKEN_ALCHEMY_URL", "sqlite:///database.db")

connect_args = {"check_same_thread": False}
engine = create_engine(db_url, connect_args=connect_args)

def create_db_and_tables():
    LOG.info(f"init tables for {engine}")
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

@contextmanager
def with_session():
    session = Session(engine)
    yield session
    session.commit()