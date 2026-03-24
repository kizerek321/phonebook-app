# SQLmodel database models
from typing import Optional
from sqlmodel import Field, SQLModel

class ContactBase(SQLModel):
    name: str = Field(index=True)
    phone: str = Field(index=True)

# Physical model in DB
class Contact(ContactBase, table=True): 
    id: Optional[int] = Field(default=None, primary_key=True)

# Input schema for creating (Pydantic - inherits name and phone)
class ContactCreate(ContactBase):
    pass

# Schema for updating (Pydantic - all fields optional)
class ContactUpdate(SQLModel):
    name: Optional[str] = None
    phone: Optional[str] = None