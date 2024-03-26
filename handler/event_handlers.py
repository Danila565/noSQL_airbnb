import asyncio

from utils.mongo_utils import connect_and_init_mongo, close_mongo_connect

async def startup():
    init_mongo_future = connect_and_init_mongo()
    await asyncio.gather(init_mongo_future)


async def shutdown():
    close_mongo_connect()