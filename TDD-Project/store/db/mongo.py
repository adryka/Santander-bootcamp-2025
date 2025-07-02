from motor.motor_asyncio import AsyncIOMotorClient

from store. core. config import settings

class MongoClient:
    def _init_(self) -> None:
        self.client: AsyncIOMotorClient = AsyncIOMotorClient(settings.DATABASE_URL)

    def get(self) -> AsyncIOMotorClient:
        return self.client

db_client = MongoClient()