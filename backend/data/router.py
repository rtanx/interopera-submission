from typing import List
from fastapi import APIRouter, HTTPException, Depends
from .schemas import SalesRep
from .service import SalesRepService, get_sales_rep_service

router = APIRouter()


@router.get("/", response_model=List[SalesRep])
async def get_all(service: SalesRepService = Depends(get_sales_rep_service)):
    return service.get_all_sales_reps()


@router.get("/{rep_id}", response_model=SalesRep)
async def get_by_id(rep_id: int, service: SalesRepService = Depends(get_sales_rep_service)):
    sales_rep = service.get_sales_rep_by_id(rep_id)
    if not sales_rep:
        raise HTTPException(
            status_code=404, detail="Sales representative not found")
    return sales_rep


@router.get("/region/{region}", response_model=List[SalesRep])
async def get_by_region(region: str, service: SalesRepService = Depends(get_sales_rep_service)):
    sales_reps = service.get_sales_reps_by_region(region)
    if not sales_reps:
        raise HTTPException(
            status_code=404, detail="No sales representatives found in the given region")
    return sales_reps
