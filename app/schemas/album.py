from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from app.schemas.artist import ArtistSimple


class AlbumBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    release_year: int = Field(..., ge=1900, le=2100)
    genre: str = Field(..., min_length=1, max_length=200)
    total_tracks: Optional[int] = Field(default=None, ge=1, le=200)
    artist_id: int
    user_score: Optional[int] = Field(default=None, ge=0, le=100)
    rating_count: Optional[int] = Field(default=None, ge=0)
    album_link: Optional[str] = None


class AlbumCreate(AlbumBase):
    pass


class AlbumResponse(AlbumBase):
    id: int
    artist: ArtistSimple
    model_config = ConfigDict(from_attributes=True)