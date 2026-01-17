from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# import moviebox internals (NOT cli main)
from moviebox_api.core.search import search_movie
from moviebox_api.core.sources import get_sources

app = FastAPI(title="MovieCove MovieBox API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "MovieCove MovieBox API running 🚀"}

@app.get("/search/{q}")
def search(q: str):
    results = search_movie(q)
    return {"results": results}

@app.get("/sources/{movie_id}")
def sources(movie_id: str):
    streams = get_sources(movie_id)
    return {"streams": streams}
