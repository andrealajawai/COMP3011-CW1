from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    release_year = Column(Integer, nullable=False)
    genre = Column(String, nullable=False)
    total_tracks = Column(Integer, nullable=True)

    user_score = Column(Integer, nullable=True)
    rating_count = Column(Integer, nullable=True)
    album_link = Column(String, nullable=True)

    artist_id = Column(Integer, ForeignKey("artists.id"), nullable=False)

    artist = relationship("Artist", back_populates="albums")