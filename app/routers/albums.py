from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.album import Album
from app.models.artist import Artist
from app.schemas.album import AlbumCreate, AlbumResponse

router = APIRouter(prefix="/albums", tags=["Albums"])


@router.post("/", response_model=AlbumResponse, status_code=201)
def create_album(album: AlbumCreate, db: Session = Depends(get_db)):
    artist = db.query(Artist).filter(Artist.id == album.artist_id).first()
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")

    db_album = Album(
        title=album.title,
        release_year=album.release_year,
        genre=album.genre,
        total_tracks=album.total_tracks,
        user_score=album.user_score,
        rating_count=album.rating_count,
        album_link=album.album_link,
        artist_id=album.artist_id
    )
    db.add(db_album)
    db.commit()
    db.refresh(db_album)
    return db_album


@router.get("/", response_model=list[AlbumResponse])
def get_albums(
    search: str | None = Query(default=None, description="Search by album title"),
    genre: str | None = Query(default=None),
    release_year: int | None = Query(default=None),
    artist_id: int | None = Query(default=None),
    min_score: int | None = Query(default=None, ge=0, le=100),
    sort_by: str | None = Query(default="title"),
    order: str | None = Query(default="asc"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(Album)

    if search is not None:
        query = query.filter(Album.title.ilike(f"%{search}%"))

    if genre is not None:
        query = query.filter(Album.genre.ilike(f"%{genre}%"))

    if release_year is not None:
        query = query.filter(Album.release_year == release_year)

    if artist_id is not None:
        query = query.filter(Album.artist_id == artist_id)

    if min_score is not None:
        query = query.filter(Album.user_score >= min_score)

    sortable_fields = {
        "title": Album.title,
        "release_year": Album.release_year,
        "user_score": Album.user_score,
        "rating_count": Album.rating_count
    }

    sort_column = sortable_fields.get(sort_by, Album.title)

    if order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    return query.offset(offset).limit(limit).all()


@router.get("/{album_id}", response_model=AlbumResponse)
def get_album(album_id: int, db: Session = Depends(get_db)):
    album = db.query(Album).filter(Album.id == album_id).first()
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    return album


@router.put("/{album_id}", response_model=AlbumResponse)
def update_album(album_id: int, updated_album: AlbumCreate, db: Session = Depends(get_db)):
    album = db.query(Album).filter(Album.id == album_id).first()
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")

    artist = db.query(Artist).filter(Artist.id == updated_album.artist_id).first()
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")

    album.title = updated_album.title
    album.release_year = updated_album.release_year
    album.genre = updated_album.genre
    album.total_tracks = updated_album.total_tracks
    album.user_score = updated_album.user_score
    album.rating_count = updated_album.rating_count
    album.album_link = updated_album.album_link
    album.artist_id = updated_album.artist_id

    db.commit()
    db.refresh(album)
    return album


@router.delete("/{album_id}")
def delete_album(album_id: int, db: Session = Depends(get_db)):
    album = db.query(Album).filter(Album.id == album_id).first()
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")

    db.delete(album)
    db.commit()
    return {"message": "Album deleted successfully"}