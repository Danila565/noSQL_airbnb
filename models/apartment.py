from pydantic import BaseModel


class Apartment(BaseModel):
    id: str
    state: str
    address: str
    zipcode: int
    bedrooms: int
    bathroom: str
    wifi: str
    kitchen: str


class UpdateApartmentModel(BaseModel):
    state: str
    address: str
    zipcode: int
    bedrooms: int
    bathroom: str
    wifi: str
    kitchen: str