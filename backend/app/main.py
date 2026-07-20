import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.routes import router as api_router

app = FastAPI(
    title="TellMe TTS API",
    description="FastAPI Backend for TellMe Text-to-Speech & Voice Cloning Web Application",
    version="1.0.0"
)

# Enable CORS for frontend development & production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure static audio folders exist
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
os.makedirs(os.path.join(static_dir, "audio"), exist_ok=True)
os.makedirs(os.path.join(static_dir, "audio", "references"), exist_ok=True)

# Mount static audio files
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Include API routes
app.include_router(api_router, prefix="/api")

@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "service": "TellMe TTS Backend",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
