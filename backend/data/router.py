from typing import List
from fastapi import APIRouter, HTTPException, Depends
from .schemas import SalesRep
from .service import SalesRepService, get_sales_rep_service

router = APIRouter()


@router.get("/", response_model=List[SalesRep])
async def get_data(service: SalesRepService = Depends(get_sales_rep_service)):
    return service.get_all_sales_reps()
