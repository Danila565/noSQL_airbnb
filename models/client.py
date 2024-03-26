from pydantic import BaseModel


class Client(BaseModel):
    id: str
    name: str
    surname: str
    age: int
    phone: str
    email: str


class UpdateClientModel(BaseModel):
    name: str
    surname: str
    age: int
    phone: str
    email: str