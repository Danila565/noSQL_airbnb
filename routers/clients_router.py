import json
from bson import ObjectId
from typing import Any
from fastapi import APIRouter, Depends, status
from starlette.responses import Response

from models.client import Client
from repository.clients_repository import ClientRepository
from utils.mongo_utils import map_update_client

clients_router = APIRouter()


@clients_router.get("/all")
async def get_all_clients(repository: ClientRepository = Depends(ClientRepository.get_client_repo_instance)) -> list[Client]:
    return await repository.get_all()


@clients_router.get("/all_id")
async def get_all_clients_id(repository: ClientRepository = Depends(ClientRepository.get_client_repo_instance)):
    return await repository.get_all_id()


@clients_router.get("/{client_id}", response_model=Client)
async def get_clients_by_id(client_id: str, 
                            repository: ClientRepository = Depends(ClientRepository.get_client_repo_instance)) -> Any:
    if not ObjectId.is_valid(client_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    
    client = await repository.get_by_id(client_id)

    if client is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    
    return client


@clients_router.post("/srv/post_all")
async def fill_clients(repository: ClientRepository = Depends(ClientRepository.get_client_repo_instance)):
    with open('./clients.json', 'r') as src:
        clients_list = json.load(src)
        for cl in clients_list:
            client = map_update_client(cl)
            await repository.create(client)


@clients_router.delete("/srv/delete_all")
async def remove_all(repository: ClientRepository = Depends(ClientRepository.get_client_repo_instance)) -> Response:
    await repository.delete_all()
    return Response()
