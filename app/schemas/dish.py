from uuid import UUID

from pydantic import BaseModel, Field, computed_field


class DishBase(BaseModel):
    title: str
    description: str
    price: str
    discount: int = Field(exclude=True)

    @computed_field(alias='price')  # type: ignore[misc]
    @property
    def computed_price(self) -> str:
        return str(float(self.price) * (100 - self.discount) / 100)


class DishCreate(BaseModel):
    title: str
    description: str
    price: str


class DishUpdate(DishCreate):
    pass


class DishInDB(DishBase):
    class Config:
        from_attributes = True


class DishGet(DishInDB):
    id: UUID
    description: str
    price: str
