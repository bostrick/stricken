from typing import Annotated, ClassVar

from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy.orm import declared_attr

import uuid


class TotavModelRegistry(dict):

    def register(self, subclass, name=None):
        name = name or subclass.get_model_name()
        self[name] = subclass
        return subclass

    def new(self, model_name, **kwargs):
        M = self[model_name]
        return M(**kwargs)


TOTAV_MODEL_REGISTRY = TotavModelRegistry()


class TotavModel(SQLModel):

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)

    @classmethod
    def get_model_name(cls):
        return cls.__name__.lower()

    @classmethod
    def load(cls, doc, session):
        books = doc.pop("book_list", [])
        obj = cls(**doc)
        session.add(obj)
        return obj

def get_model_registry() -> TotavModelRegistry:
    return TOTAV_MODEL_REGISTRY

def get_model(name: str) -> TotavModel:
    return TOTAV_MODEL_REGISTRY.get(name)


@TOTAV_MODEL_REGISTRY.register
class Organization(TotavModel, table=True):

    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str | None

    books: list["Book"] = Relationship(back_populates="organization")

    @classmethod
    def load(cls, doc, session):
        books = doc.pop("book_list", [])
        org = cls(**doc)
        session.add(org)
        if books:
            M = get_model("book")
            for book_doc in books:
                book_doc["organization_id"] = org.id
                assert book_doc.pop("model_name", "book") == "book"
                M.load(book_doc, session)
        return org


@TOTAV_MODEL_REGISTRY.register
class Book(TotavModel, table=True):

    name: str = Field(index=True)
    organization_id: str = Field(foreign_key="organization.id")

    organization: Organization = Relationship(back_populates="books")


