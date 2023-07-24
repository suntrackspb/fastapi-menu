from uuid import UUID

from pydantic import BaseModel


class MenuBase(BaseModel):
    title: str
    description: str


class MenuCreate(MenuBase):
    pass


class MenuUpdate(MenuBase):
    pass


class MenuInDB(MenuBase):
    id: UUID

    class Config:
        from_attributes = True


class MenuGet(MenuInDB):
    id: UUID
    submenus_count: int
    dishes_count: int
