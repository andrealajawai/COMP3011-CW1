import csv
import re
from datetime import datetime
from sqlalchemy.orm import Session

from app.database import SessionLocal, Base, engine
from app.models.artist import Artist
from app.models.album import Album

Base.metadata.create_all(bind=engine)


def extract_year(release_date: str) -> int:
    """
    Extracts year from strings like 'March 15, 2015'
    """
    if not release_date:
        return 1900

    try:
        return datetime.strptime(release_date, "%B %d, %Y").year
    except ValueError:
        match = re.search(r"\b(19|20)\d{2}\b", release_date)
        if match:
            return int(match.group())
        return 1900


def parse_rating_count(rating_count: str) -> int:
    """
    Converts strings like '28,594 ratings' into 28594
    """
    if not rating_count:
        return 0

    cleaned = rating_count.replace("ratings", "").replace("rating", "").replace(",", "").strip()
    try:
        return int(cleaned)
    except ValueError:
        return 0


def import_aoty_data():
    db: Session = SessionLocal()

    with open("data/aoty.csv", mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        imported_count = 0

        for row in reader:
            title = row.get("title", "").strip()
            artist_name = row.get("artist", "").strip()
            release_date = row.get("release_date", "").strip()
            genres = row.get("genres", "").strip()
            user_score = row.get("user_score", "").strip()
            rating_count = row.get("rating_count", "").strip()
            album_link = row.get("album_link", "").strip()

            if not title or not artist_name:
                continue

            release_year = extract_year(release_date)

            try:
                user_score = int(user_score)
            except ValueError:
                user_score = None

            parsed_rating_count = parse_rating_count(rating_count)

            artist = db.query(Artist).filter(Artist.name == artist_name).first()
            if not artist:
                artist = Artist(
                    name=artist_name,
                    country=None,
                    debut_year=None
                )
                db.add(artist)
                db.commit()
                db.refresh(artist)

            existing_album = db.query(Album).filter(
                Album.title == title,
                Album.artist_id == artist.id
            ).first()

            if existing_album:
                continue

            album = Album(
                title=title,
                release_year=release_year,
                genre=genres if genres else "Unknown",
                total_tracks=None,
                user_score=user_score,
                rating_count=parsed_rating_count,
                album_link=album_link if album_link else None,
                artist_id=artist.id
            )

            db.add(album)
            imported_count += 1

        db.commit()
        db.close()

        print(f"Import complete. {imported_count} albums added.")


if __name__ == "__main__":
    import_aoty_data()