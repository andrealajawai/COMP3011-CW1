from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Music API is running"}


def test_create_artist():
    response = client.post("/artists/", json={
        "name": "Test Artist",
        "country": "Test Country",
        "debut_year": 2000
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Artist"
    assert "id" in data


def test_get_artists():
    response = client.get("/artists/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_album():
    # First create artist
    artist_res = client.post("/artists/", json={
        "name": "Album Artist",
        "country": "UK",
        "debut_year": 1990
    })
    artist_id = artist_res.json()["id"]

    # Then create album
    response = client.post("/albums/", json={
        "title": "Test Album",
        "release_year": 2020,
        "genre": "Rock",
        "total_tracks": 10,
        "artist_id": artist_id
    })

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Album"
    assert data["artist_id"] == artist_id


def test_album_filtering():
    response = client.get("/albums/?genre=rock")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_top_rated_analytics():
    response = client.get("/analytics/top-rated-albums")
    assert response.status_code == 200
    assert isinstance(response.json(), list)