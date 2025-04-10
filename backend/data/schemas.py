from typing import List
from pydantic import BaseModel


class Deal(BaseModel):
    client: str
    value: int
    status: str


class Client(BaseModel):
    name: str
    industry: str
    contact: str


class SalesRep(BaseModel):
    id: int
    name: str
    role: str
    region: str
    skills: List[str]
    deals: List[Deal]
    clients: List[Client]


class SalesData(BaseModel):
    salesReps: List[SalesRep]
