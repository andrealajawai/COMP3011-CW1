from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    country = Column(String, nullable=True)
    debut_year = Column(Integer, nullable=True)

    albums = relationship("Album", back_populates="artist", cascade="all, delete")