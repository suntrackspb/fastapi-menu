from uuid import UUID

from pydantic import BaseModel, Field, computed_field


class DishComputed(BaseModel):
    id: UUID
    title: str
    description: str
    price: str
    discount: int = Field(exclude=True)

    @computed_field(alias='price')  # type: ignore[misc]
    @property
    def computed_price(self) -> str:
        return str(float(self.price) * (100 - self.discount) / 100)


class SubmenuSchema(BaseModel):
    id: UUID
    title: str
    description: str | None
    dishes: list[DishComputed]


class MenuBase(BaseModel):
    title: str
    description: str | None
    submenus: list[SubmenuSchema]


class MenuFullInDB(MenuBase):
    id: UUID

    class Config:
        from_attributes = True


class MenuSchema(MenuFullInDB):
    id: UUID
    submenus_count: int
    dishes_count: int


class MessageStatus(BaseModel):
    status: str
    message: str
