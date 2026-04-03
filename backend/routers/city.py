from fastapi import APIRouter, HTTPException, Query
from backend.models.city import CityService
from backend.schema.city_schema import CityData

router = APIRouter(prefix="/cities", tags=["City"])
service = CityService()


@router.get("", response_model=list[CityData])
def get_city(q: str = Query(..., min_length=3)):
    try:
        data = service.search_city(q)
        return data
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
