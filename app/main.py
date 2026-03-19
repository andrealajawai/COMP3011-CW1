from fastapi import FastAPI
from app.database import Base, engine
from app.models import Artist, Album
from app.routers import artists, albums, analytics

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Music Discovery and Album Analytics API",
    description="A REST API for managing artists and albums.",
    version="1.0.0"
)

app.include_router(artists.router)
app.include_router(albums.router)
app.include_router(analytics.router)

@app.get("/")
def root():
    return {"message": "Music API is running"}