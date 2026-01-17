from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import uvicorn
import os

app = FastAPI(title="MovieCove API")

# ===================== CORS =====================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===================== ROOT =====================
@app.get("/")
def root():
    return {"status": "MovieCove API running 🚀"}

# ===================== SEARCH =====================
@app.get("/search/{q}")
def search(q: str):
    # SAMPLE DATA (replace later with scraper logic)
    return {
        "results": [
            {
                "id": "1",
                "title": f"{q} (2024)",
                "poster": "https://via.placeholder.com/300x450?text=Movie",
                "rating": 8.4,
                "type": "movie"
            },
            {
                "id": "2",
                "title": f"{q} Episode Series",
                "poster": "https://via.placeholder.com/300x450?text=Series",
                "rating": 7.9,
                "type": "series"
            }
        ]
    }

# ===================== MOVIE INFO =====================
@app.get("/info/{movie_id}")
def movie_info(movie_id: str):
    return {
        "id": movie_id,
        "title": "Avengers: Infinity War",
        "rating": 8.4,
        "description": "The Avengers must stop Thanos.",
        "episodes": [
            {"ep": 1, "title": "Episode 1", "stream": "https://samplelib.com/lib/preview/mp4/sample-5s.mp4"},
            {"ep": 2, "title": "Episode 2", "stream": "https://samplelib.com/lib/preview/mp4/sample-10s.mp4"}
        ]
    }

# ===================== SOURCES =====================
@app.get("/sources/{movie_id}")
def sources(movie_id: str):
    return {
        "streams": [
            {
                "quality": "HD",
                "url": f"/stream?url=https://samplelib.com/lib/preview/mp4/sample-5s.mp4"
            }
        ],
        "downloads": [
            {
                "quality": "HD",
                "url": f"/download?url=https://samplelib.com/lib/preview/mp4/sample-5s.mp4"
            }
        ]
    }

# ===================== STREAM PROXY =====================
@app.get("/stream")
def stream(url: str, request: Request):
    headers = {}
    if "range" in request.headers:
        headers["Range"] = request.headers["range"]

    r = requests.get(url, stream=True, headers=headers)

    return StreamingResponse(
        r.iter_content(chunk_size=1024 * 64),
        status_code=206 if "range" in headers else 200,
        headers={
            "Content-Type": "video/mp4",
            "Accept-Ranges": "bytes",
        },
    )

# ===================== DOWNLOAD =====================
@app.get("/download")
def download(url: str):
    r = requests.get(url, stream=True)
    return StreamingResponse(
        r.iter_content(chunk_size=1024 * 64),
        headers={
            "Content-Disposition": "attachment; filename=movie.mp4",
            "Content-Type": "video/mp4",
        },
    )

# ===================== RUN =====================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
