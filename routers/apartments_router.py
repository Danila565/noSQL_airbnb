import json
from bson import ObjectId
from typing import Any
from fastapi import APIRouter, Depends, status
from starlette.responses import Response

from models.apartment import Apartment, UpdateApartmentModel
from repository.apartments_repository import ApartmentRepository
from utils.mongo_utils import map_update_apartment

apartments_router = APIRouter()


@apartments_router.get("/all")
async def get_all_apartments(repository: ApartmentRepository = Depends(ApartmentRepository.get_apartment_repo_instance)) -> list[Apartment]:
    return await repository.get_all()


@apartments_router.get("/all_id")
async def get_all_apartments_id(repository: ApartmentRepository = Depends(ApartmentRepository.get_apartment_repo_instance)):
    return await repository.get_all_id()


@apartments_router.get("/state/{state}")
async def get_all_apartments_by_state(state: str,
                                      repository: ApartmentRepository = Depends(ApartmentRepository.get_apartment_repo_instance)):
    return await repository.get_all_by_state(state)


@apartments_router.get("/state/{state}/bedrooms/{bedrooms}/wifi/{wifi}")
async def get_all_apartments_by_state(state: str,
                                      bedrooms: str,
                                      wifi: str,
                                      repository: ApartmentRepository = Depends(ApartmentRepository.get_apartment_repo_instance)):
    return await repository.get_all_by_sbw(state, int(bedrooms), wifi)


@apartments_router.get("/state/{state}")
async def get_all_apartments_by_state(state: str,
                                      repository: ApartmentRepository = Depends(ApartmentRepository.get_apartment_repo_instance)):
    return await repository.get_all_by_state(state)


@apartments_router.get("/{apartment_id}", response_model=Apartment)
async def get_apartment_by_id(apartment_id: str, 
                              repository: ApartmentRepository = Depends(ApartmentRepository.get_apartment_repo_instance)) -> Any:
    if not ObjectId.is_valid(apartment_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    
    apartment = await repository.get_by_id(apartment_id)

    if apartment is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    
    return apartment


@apartments_router.post("/srv/post_all")
async def fill_apartments(repository: ApartmentRepository = Depends(ApartmentRepository.get_apartment_repo_instance)):
    with open('./apartments.json', 'r') as src:
        apartments_list = json.load(src)
        for ap in apartments_list:
            apartment = map_update_apartment(ap)
            await repository.create(apartment)


@apartments_router.delete("/srv/delete_all")
async def remove_all(repository: ApartmentRepository = Depends(ApartmentRepository.get_apartment_repo_instance)) -> Response:
    await repository.delete_all()
    return Response()