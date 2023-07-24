from uuid import UUID

from pydantic import BaseModel


class DishBase(BaseModel):
    title: str
    description: str
    price: str


class DishCreate(DishBase):
    description: str
    price: str


class DishUpdate(DishBase):
    pass


class DishInDB(DishBase):

    class Config:
        from_attributes = True


class DishGet(DishInDB):
    id: UUID
    description: str
    price: str
