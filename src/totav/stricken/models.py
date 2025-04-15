from typing import Annotated, ClassVar

from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy.orm import declared_attr


class TotavModelRegistry:

    def __init__(self):
        self.registry = {}

    def register(self, subclass, name=None):
        name = name or subclass.model_name
        self.registry[name] = subclass
        return subclass

TOTAV_MODEL_REGISTRY = TotavModelRegistry()



class TotavModel(SQLModel):

    model_name : str = ""   # subclass responsibility
    id : str = Field(primary_key=True)


@TOTAV_MODEL_REGISTRY.register
class Organization(TotavModel, table=True):

    model_name : str = "organization"
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str

    books: list["Book"] = Relationship(back_populates="organization")



@TOTAV_MODEL_REGISTRY.register
class Book(TotavModel, table=True):

    model_name : str = "book"
    name: str = Field(index=True)
    organization_id: str = Field(foreign_key="organization.id")

    organization: Organization = Relationship(back_populates="books")


