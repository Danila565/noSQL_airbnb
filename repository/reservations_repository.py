from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorCollection

from utils.mongo_utils import get_reservation_collection, get_filter, map_reservation
from models.reservation import Reservation, UpdateReservationModel


class ReservationRepository:
    _db_collection: AsyncIOMotorCollection

    def __init__(self, db_collection: AsyncIOMotorCollection):
        self._db_collection = db_collection

    async def create(self, reservation: UpdateReservationModel) -> str:
        insert_result = await self._db_collection.insert_one(dict(reservation))
        return str(insert_result.inserted_id)

    async def get_all(self) -> list[Reservation]:
        db_reservations = []
        async for reservation in self._db_collection.find():
            db_reservations.append(map_reservation(reservation))
        return db_reservations
    
    async def get_all_id(self):
        db_reservations = []
        async for reservation in self._db_collection.find():
            db_reservations.append(map_reservation(reservation).id)
        return db_reservations

    async def get_by_id(self, reservation_id: str) -> Reservation | None:
        print(f'Get reservation {reservation_id} from mongo')
        db_reservation = await self._db_collection.find_one(get_filter(reservation_id))
        return map_reservation(db_reservation)
    
    async def get_all_by_apartment_id(self, apartment_id: str):
        db_reservations = []
        async for reservation in self._db_collection.find({"apartment_id" : apartment_id}):
            db_reservations.append(map_reservation(reservation))
        return db_reservations
    

    async def update(self, reservation_id: str, reservation: UpdateReservationModel) -> Reservation | None:
        db_reservation = await self._db_collection.find_one_and_replace(get_filter(reservation_id), dict(reservation))
        return map_reservation(db_reservation)

    async def delete(self, reservation_id: str) -> Reservation | None:
        db_reservation = await self._db_collection.find_one_and_delete(get_filter(reservation_id))
        return map_reservation(db_reservation)
    
    async def delete_all(self):
        async for reservation in self._db_collection.find():
            await self._db_collection.find_one_and_delete(get_filter(str(reservation['_id'])))

    @staticmethod
    def get_reservation_repo_instance(db_collection: AsyncIOMotorCollection = Depends(get_reservation_collection)):
        return ReservationRepository(db_collection)