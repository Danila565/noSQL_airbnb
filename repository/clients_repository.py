from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorCollection

from utils.mongo_utils import get_client_collection, get_filter, map_client
from models.client import Client, UpdateClientModel


class ClientRepository:
    _db_collection: AsyncIOMotorCollection

    def __init__(self, db_collection: AsyncIOMotorCollection):
        self._db_collection = db_collection

    async def create(self, client: UpdateClientModel) -> str:
        insert_result = await self._db_collection.insert_one(dict(client))
        return str(insert_result.inserted_id)

    async def get_all(self) -> list[Client]:
        db_clients = []
        async for client in self._db_collection.find():
            print(client)
            db_clients.append(map_client(client))
        return db_clients
    
    async def get_all_id(self):
        db_clients = []
        async for client in self._db_collection.find():
            db_clients.append(map_client(client).id)
        return db_clients

    async def get_by_id(self, client_id: str) -> Client | None:
        print(f'Get client {client_id} from mongo')
        db_client = await self._db_collection.find_one(get_filter(client_id))
        return map_client(db_client)

    async def update(self, client_id: str, client: UpdateClientModel) -> Client | None:
        db_client = await self._db_collection.find_one_and_replace(get_filter(client_id), dict(client))
        return map_client(db_client)

    async def delete(self, client_id: str) -> Client | None:
        db_client = await self._db_collection.find_one_and_delete(get_filter(client_id))
        return map_client(db_client)
    
    async def delete_all(self):
        async for client in self._db_collection.find():
            await self._db_collection.find_one_and_delete(get_filter(str(client['_id'])))

    @staticmethod
    def get_client_repo_instance(db_collection: AsyncIOMotorCollection = Depends(get_client_collection)):
        return ClientRepository(db_collection)