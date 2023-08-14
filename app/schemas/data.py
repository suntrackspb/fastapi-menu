from pydantic import BaseModel


class DishSchema(BaseModel):
    title: str
    description: str
    price: str


class SubmenuSchema(BaseModel):
    title: str
    description: str | None
    dishes: list[DishSchema]


class MenuSchema(BaseModel):
    title: str
    description: str | None
    submenus: list[SubmenuSchema]


class MessageStatus(BaseModel):
    status: str
    message: str
