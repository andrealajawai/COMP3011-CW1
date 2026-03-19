from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.album import Album
from app.models.artist import Artist

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/top-rated-albums")
def top_rated_albums(
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    albums = (
        db.query(
            Album.id,
            Album.title,
            Album.user_score,
            Album.rating_count,
            Artist.name.label("artist_name")
        )
        .join(Artist, Album.artist_id == Artist.id)
        .filter(Album.user_score.isnot(None))
        .order_by(Album.user_score.desc(), Album.rating_count.desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "id": album.id,
            "title": album.title,
            "artist": album.artist_name,
            "user_score": album.user_score,
            "rating_count": album.rating_count
        }
        for album in albums
    ]


@router.get("/most-rated-albums")
def most_rated_albums(
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    albums = (
        db.query(
            Album.id,
            Album.title,
            Album.user_score,
            Album.rating_count,
            Artist.name.label("artist_name")
        )
        .join(Artist, Album.artist_id == Artist.id)
        .filter(Album.rating_count.isnot(None))
        .order_by(Album.rating_count.desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "id": album.id,
            "title": album.title,
            "artist": album.artist_name,
            "user_score": album.user_score,
            "rating_count": album.rating_count
        }
        for album in albums
    ]


@router.get("/genre-distribution")
def genre_distribution(db: Session = Depends(get_db)):
    results = (
        db.query(
            Album.genre,
            func.count(Album.id).label("album_count")
        )
        .group_by(Album.genre)
        .order_by(func.count(Album.id).desc())
        .all()
    )

    return [
        {
            "genre": row.genre,
            "album_count": row.album_count
        }
        for row in results
    ]


@router.get("/artist-summary/{artist_id}")
def artist_summary(artist_id: int, db: Session = Depends(get_db)):
    artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")

    album_count = db.query(func.count(Album.id)).filter(Album.artist_id == artist_id).scalar()

    avg_score = (
        db.query(func.avg(Album.user_score))
        .filter(Album.artist_id == artist_id, Album.user_score.isnot(None))
        .scalar()
    )

    top_album = (
        db.query(Album)
        .filter(Album.artist_id == artist_id, Album.user_score.isnot(None))
        .order_by(Album.user_score.desc(), Album.rating_count.desc())
        .first()
    )

    return {
        "artist_id": artist.id,
        "artist_name": artist.name,
        "album_count": album_count,
        "average_user_score": round(float(avg_score), 2) if avg_score is not None else None,
        "top_album": {
            "id": top_album.id,
            "title": top_album.title,
            "user_score": top_album.user_score,
            "rating_count": top_album.rating_count
        } if top_album else None
    }


@router.get("/release-year-trends")
def release_year_trends(
    start_year: int | None = Query(default=None),
    end_year: int | None = Query(default=None),
    db: Session = Depends(get_db)
):
    query = db.query(
        Album.release_year,
        func.count(Album.id).label("album_count")
    )

    if start_year is not None:
        query = query.filter(Album.release_year >= start_year)

    if end_year is not None:
        query = query.filter(Album.release_year <= end_year)

    results = (
        query.group_by(Album.release_year)
        .order_by(Album.release_year.asc())
        .all()
    )

    return [
        {
            "release_year": row.release_year,
            "album_count": row.album_count
        }
        for row in results
    ]