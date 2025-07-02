from decimal import Decimal
from typing import List, Optional
from uuid import UUID
from bson import Decimal128
from motor.motor_asyncio import AsyncIOMotorClient
import pymongo
from store.db.mongo import db_client
from store.models.product import ProductModel
from store.schemas.product import ProductIn, ProductOut, ProductUpdate
from store.core.exceptions import NotFoundException
from datetime import datetime, timezone

class ProductUsecase:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = db_client.get()
        self.database: AsyncIOMotorClient = self.client.get_database()
        self.collection = self.database.get_collection("products")

    async def create(self, body: ProductIn) -> ProductOut:
        product_model = ProductModel(**body.model_dump())
        await self.collection.insert_one(product_model.model_dump())

        return ProductOut(**product_model.model_dump())

    async def get(self, id:UUID) -> ProductOut:
        result = await self.collection.find_one({"id": id})

        if not result:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        return ProductOut(**result)
    
    async def query(self, min_price: Optional[Decimal] = None, max_price: Optional[Decimal] = None) -> List[ProductOut]:
        filter_query = {}
        if min_price is not None and max_price is not None:
            filter_query["price"] = {"$gt": Decimal128(str(min_price)), "$lt": Decimal128(str(max_price))}
        elif min_price is not None:
            filter_query["price"] = {"$gt": Decimal128(str(min_price))}
        elif max_price is not None:
            filter_query["price"] = {"$lt": Decimal128(str(max_price))}

        return [ProductOut(**item) async for item in self.collection.find(filter_query)]
    
    async def update(self, id: UUID, body: ProductUpdate) -> ProductOut:
        update_data = body.model_dump(exclude_none=True)
        update_data["updated_at"] = datetime.now(timezone.utc)

        result = await self.collection.find_one_and_update(
            filter={"id": id},
            update={"$set": update_data},
            return_document=pymongo.ReturnDocument.AFTER
        )
        if not result:
            raise NotFoundException(message=f"Product not found with filter: {id}")
        
        return ProductOut(**result)
    
    async def delete(self, id: UUID) -> bool:
        product = await self.collection.find_one({"id": id})
        if not product:
            raise NotFoundException(message=f"Product not found with filter: {id}")
        
        result = await self.collection.delete_one({"id": id})

        return True if result.deleted_count > 0 else False

product_usecase = ProductUsecase()