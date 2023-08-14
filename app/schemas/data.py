from pydantic import BaseModel, Field, computed_field


class DishComputed(BaseModel):
    title: str
    description: str
    price: str
    discount: int = Field(exclude=True)

    @computed_field(alias='price')  # type: ignore[misc]
    @property
    def computed_price(self) -> str:
        return str(float(self.price) * (100 - self.discount) / 100)


class SubmenuSchema(BaseModel):
    title: str
    description: str | None
    dishes: list[DishComputed]


class MenuSchema(BaseModel):
    title: str
    description: str | None
    submenus: list[SubmenuSchema]


class MessageStatus(BaseModel):
    status: str
    message: str
