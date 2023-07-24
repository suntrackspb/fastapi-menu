from uuid import UUID

from pydantic import BaseModel


class SubmenuBase(BaseModel):
    title: str
    description: str


class SubmenuCreate(SubmenuBase):
    description: str


class SubmenuUpdate(SubmenuBase):
    pass


class SubmenuInDB(SubmenuBase):

    class Config:
        from_attributes = True


class SubmenuGet(SubmenuInDB):
    dishes_count: int
    description: str
    id: UUID
