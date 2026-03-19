from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.artist import Artist
from app.schemas.artist import ArtistCreate, ArtistResponse

router = APIRouter(prefix="/artists", tags=["Artists"])


@router.post("/", response_model=ArtistResponse, status_code=201)
def create_artist(artist: ArtistCreate, db: Session = Depends(get_db)):
    db_artist = Artist(
        name=artist.name,
        country=artist.country,
        debut_year=artist.debut_year
    )
    db.add(db_artist)
    db.commit()
    db.refresh(db_artist)
    return db_artist


@router.get("/", response_model=list[ArtistResponse])
def get_artists(db: Session = Depends(get_db)):
    return db.query(Artist).all()


@router.get("/{artist_id}", response_model=ArtistResponse)
def get_artist(artist_id: int, db: Session = Depends(get_db)):
    artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    return artist


@router.put("/{artist_id}", response_model=ArtistResponse)
def update_artist(artist_id: int, updated_artist: ArtistCreate, db: Session = Depends(get_db)):
    artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")

    artist.name = updated_artist.name
    artist.country = updated_artist.country
    artist.debut_year = updated_artist.debut_year

    db.commit()
    db.refresh(artist)
    return artist


@router.delete("/{artist_id}")
def delete_artist(artist_id: int, db: Session = Depends(get_db)):
    artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")

    db.delete(artist)
    db.commit()
    return {"message": "Artist deleted successfully"}