from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorCollection

from utils.mongo_utils import get_apartment_collection, get_filter, map_apartment
from models.apartment import Apartment, UpdateApartmentModel


class ApartmentRepository:
    _db_collection: AsyncIOMotorCollection

    def __init__(self, db_collection: AsyncIOMotorCollection):
        self._db_collection = db_collection

    async def create(self, apartment: UpdateApartmentModel) -> str:
        insert_result = await self._db_collection.insert_one(dict(apartment))
        return str(insert_result.inserted_id)

    async def get_all(self) -> list[Apartment]:
        db_apartments = []
        async for apartment in self._db_collection.find():
            db_apartments.append(map_apartment(apartment))
        return db_apartments
    
    async def get_all_id(self):
        db_apartments = []
        async for apartment in self._db_collection.find():
            print(apartment)
            db_apartments.append(map_apartment(apartment).id)
        return db_apartments

    async def get_by_id(self, apartment_id: str) -> Apartment | None:
        print(f'Get client {apartment_id} from mongo')
        db_apartment = await self._db_collection.find_one(get_filter(apartment_id))
        return map_apartment(db_apartment)
    

    async def get_all_by_state(self, state: str):
        db_apartments = []
        async for apartment in self._db_collection.find({"state" : state}):
            db_apartments.append(map_apartment(apartment))
        return db_apartments
    
    async def get_all_by_sbw(self, state: str, bedrooms: int, wifi: str):
        db_apartments = []
        async for apartment in self._db_collection.find({"state" : state, "bedrooms" : bedrooms, "wifi" : wifi}):
            db_apartments.append(map_apartment(apartment))
        return db_apartments
    

    async def update(self, apartment_id: str, apartment: UpdateApartmentModel) -> Apartment | None:
        db_apartment = await self._db_collection.find_one_and_replace(get_filter(apartment_id), dict(apartment))
        return map_apartment(db_apartment)

    async def delete(self, apartment_id: str) -> Apartment | None:
        db_apartment = await self._db_collection.find_one_and_delete(get_filter(apartment_id))
        return map_apartment(db_apartment)
    
    async def delete_all(self):
        async for apartment in self._db_collection.find():
            await self._db_collection.find_one_and_delete(get_filter(str(apartment['_id'])))

    @staticmethod
    def get_apartment_repo_instance(db_collection: AsyncIOMotorCollection = Depends(get_apartment_collection)):
        return ApartmentRepository(db_collection)