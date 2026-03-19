from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class ArtistBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    country: Optional[str] = Field(default=None, max_length=100)
    debut_year: Optional[int] = Field(default=None, ge=1900, le=2100)


class ArtistCreate(ArtistBase):
    pass


class ArtistResponse(ArtistBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ArtistSimple(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)