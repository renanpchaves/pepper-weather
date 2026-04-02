from pydantic import BaseModel, Field
from typing import Optional


class CityData(BaseModel):
    """
    Pydantic model representing city data from Geocoding API.
    """

    name: str = Field(..., description="Name of the city")
    lat: float = Field(..., description="Latitude of the city")
    lon: float = Field(..., description="Longitude of the city")
    country: str = Field(..., description="Country code")
    state: Optional[str] = Field(None, description="State or region name")
