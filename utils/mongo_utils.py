import os
from typing import Any
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from models.client import Client, UpdateClientModel
from models.apartment import Apartment, UpdateApartmentModel
from models.reservation import Reservation, UpdateReservationModel

db_client: AsyncIOMotorClient = None

date_format = '%Y-%m-%d'

async def get_client_collection() -> AsyncIOMotorCollection:
    mongo_db = os.getenv('MONGO_DB')
    mongo_collection = os.getenv('MONGO_CLIENT_COLLECTION')

    return db_client.get_database(mongo_db).get_collection(mongo_collection)


async def get_apartment_collection() -> AsyncIOMotorCollection:
    mongo_db = os.getenv('MONGO_DB')
    mongo_collection = os.getenv('MONGO_APARTMENT_COLLECTION')

    return db_client.get_database(mongo_db).get_collection(mongo_collection)


async def get_reservation_collection() -> AsyncIOMotorCollection:
    mongo_db = os.getenv('MONGO_DB')
    mongo_collection = os.getenv('MONGO_RESERVATION_COLLECTION')

    return db_client.get_database(mongo_db).get_collection(mongo_collection)


async def connect_and_init_mongo():
    global db_client
    mongo_uri = os.getenv('MONGO_URI')
    try:
        db_client = AsyncIOMotorClient(mongo_uri)
        await db_client.list_databases()
        print('Connected to mongo')
    except Exception as e:
        print(f'Exception was catched {e}')

async def close_mongo_connect():
    global db_client
    if db_client is None:
        return
    
    db_client.close()

def get_filter(id: str) -> dict:
    return {'_id': ObjectId(id)}


def map_client(client: Any) -> Client | None:
    if client is None:
        return None

    return Client(
        id=str(client['_id']), 
        name=client['name'], 
        surname=client['surname'], 
        age=int(client['age']), 
        phone=client['phone'], 
        email=client['email']
    )


def map_update_client(client) -> UpdateClientModel | None:
    if client is None:
        return None

    return UpdateClientModel(
        name=client['name'], 
        surname=client['surname'], 
        age=int(client['age']), 
        phone=client['phone'], 
        email=client['email']
    )


def map_apartment(apartment: Any) -> Apartment | None:
    if apartment is None:
        return None
    
    return Apartment(
        id=str(apartment['_id']),
        state=apartment['state'],
        address=apartment['address'],
        zipcode=int(apartment['zipcode']),
        bedrooms=int(apartment['bedrooms']),
        bathroom=apartment['bathroom'],
        wifi=apartment['wifi'],
        kitchen=apartment['kitchen']
    )


def map_update_apartment(apartment) -> UpdateApartmentModel | None:
    if apartment is None:
        return None
    
    return UpdateApartmentModel(
        state=apartment['state'],
        address=apartment['address'],
        zipcode=int(apartment['zipcode']),
        bedrooms=int(apartment['bedrooms']),
        bathroom=apartment['bathroom'],
        wifi=apartment['wifi'],
        kitchen=apartment['kitchen']
    )


def map_reservation(reservation: Any) -> Reservation | None:
    if reservation is None:
        return None
    
    return Reservation(
        id=str(reservation['_id']),
        client_id=reservation['client_id'],
        apartment_id=reservation['apartment_id'],
        start_date=reservation['start_date'],
        end_date=reservation['end_date'],
        status=reservation['status']
    )


def map_update_reservation(reservation) -> UpdateReservationModel | None:
    if reservation is None:
        return None
    
    return UpdateReservationModel(
        client_id=reservation['client_id'],
        apartment_id=reservation['apartment_id'],
        start_date=reservation['start_date'],
        end_date=reservation['end_date'],
        status=reservation['status']
    )