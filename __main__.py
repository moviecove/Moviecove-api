from fastapi import FastAPI
import uvicorn
import os

app = FastAPI()

@app.get("/")
def root():
    return {"status": "MovieCove API running 🚀"}

# example search route (temporary test)
@app.get("/search/{q}")
def search(q: str):
    return {
        "results": [
            {
                "id": "1",
                "title": f"{q} Movie",
                "poster": "https://via.placeholder.com/300x450",
                "stream": "https://samplelib.com/lib/preview/mp4/sample-5s.mp4"
            }
        ]
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
