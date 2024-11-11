from pydantic import BaseModel, PositiveFloat


class Item(BaseModel):
    id: int
    name: str
    price: PositiveFloat


class ItemCreate(BaseModel):
    name: str
    price: PositiveFloat


class ItemUpdate(BaseModel):
    name: str | None = None
    price: PositiveFloat | None = None
