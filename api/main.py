from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
from api.generator import generate_room_with_llm
from api.themes import themes

app = FastAPI()

# CORS settings (veilig voor dev; beperk voor productie!)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    theme: str
    count: int = 4

@app.get("/api/themes")
def get_themes():
    return list(themes.keys())

@app.post("/api/generate")
def generate_dungeon(request: GenerateRequest):
    if request.theme not in themes:
        raise HTTPException(status_code=400, detail="Invalid theme")

    results = []
    total_tokens = 0
    for _ in range(request.count):
        room, tokens = generate_room_with_llm(theme=request.theme)
        results.append(room)
        total_tokens += tokens

    return {
        "theme": request.theme,
        "total_tokens": total_tokens,
        "rooms": results
    }

# Serve Vite static frontend
app.mount("/assets", StaticFiles(directory="frontend/assets"), name="assets")

@app.get("/")
def serve_index():
    return FileResponse("frontend/index.html")
