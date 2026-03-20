# Music Discovery and Album Analytics API

## Overview
This project is a RESTful API that provides functionality for managing music data derived from a popular music review website among music enthusiasts, Album of the Year (https://aoty.org). It includes data such as artists and albums, and supports analytical queries on album ratings by users.

The API integrates a public dataset from Kaggle (https://www.kaggle.com/datasets/tabibyte/aoty-5000-highest-user-rated-albums) and allows retrieving, filtering, and analysing album data.

---

## Features

### Core Functionality
- CRUD operations for Artists
- CRUD operations for Albums
- Relational database design (Artist → Album)

### Dataset
- Public dataset (AOTY CSV from Kaggle) imported into the database
- Automatic data ingestion via Python script

### Querying & Filtering
- Search albums by title
- Filter by genre, release year, artist
- Sort by rating, popularity, or year
- Pagination support (limit & offset)

### Analytics Endpoints
- Top-rated albums
- Most-rated albums
- Genre distribution
- Artist summary
- Release year trends

### Testing & Validation
- Input validation using Pydantic
- Basic test suite using pytest
- Proper HTTP status codes and error handling

---

## Tech used
- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Pytest

---

## Project Structure

```text
app/
├── models/
│   ├── __init__.py
│   ├── album.py
│   ├── artist.py
├── routers/
│   ├── __init__.py
│   ├── albums.py
│   ├── analytics.py
│   ├── artists.py
├── schemas/
│   ├── __init__.py
│   ├── album.py
│   ├── artist.py
├── __init__.py
├── database.py
├── import_aoty.py
├── main.py

data/
├── aoty.csv

tests/
├── test_api.py

pytest.ini
README.md
requirements.txt
````

---

## Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/andrealajawai/COMP3011-CW1.git
cd COMP3011-CW1
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the API

### Import Dataset

```bash
python -m app.import_aoty
```

### Start Server

```bash
uvicorn app.main:app --reload
```

### Open in Browser

```text
http://127.0.0.1:8000/docs
```

---

## Running Tests

### Run

```bash
pytest
```

---

## Example Endpoints

### Artists

* GET /artists/
* POST /artists/

### Albums

* GET /albums/
* POST /albums/

### Analytics

* GET /analytics/top-rated-albums
* GET /analytics/genre-distribution
* GET /analytics/release-year-trends

---

## API Documentation

Interactive API documentation is available via Swagger UI through:

* [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

A PDF version of the documentation is included in docs/api_docs.pdf

---

## Notes

* All genres are stored as strings, which may be seemed as a limitation due to the structure of the dataset used.
* No authentication/user system is implemented.
