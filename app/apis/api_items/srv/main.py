from typing import List, Optional

from sqlalchemy import select

from app.apis.api_items.model.items import Item as ItemResponse
from app.db.database import get_session
from app.db.schema.items import Item


class ItemService:
    def __init__(self) -> None:
        self.session = get_session

    def to_item_response(self, item: Item) -> ItemResponse:
        return ItemResponse(**item.__dict__)

    async def get_all_items(self) -> List[ItemResponse]:
        async with self.session() as db:
            result = await db.execute(select(Item))
            items = result.scalars().all()
            return [self.to_item_response(item) for item in items]

    async def create_item(self, data: Item) -> Optional[ItemResponse]:
        async with self.session() as db:
            new_item = Item(**data.model_dump())
            db.add(new_item)
            await db.commit()
            await db.refresh(new_item)
            return self.to_item_response(new_item)
