import os
import shutil
import uuid
from typing import Optional, List
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel, Field

from app.services.vieneu_service import VieneuService
from app.services.edge_service import EdgeTTSService
from app.services.google_service import GoogleTTSService

router = APIRouter()

# In-memory history tracking
AUDIO_HISTORY = []

class GenerateTTSRequest(BaseModel):
    text: str = Field(..., description="Text to synthesize")
    engine: str = Field("vieneu", description="TTS Engine: vieneu | edge | google")
    voice_id: str = Field("pham_tuyen", description="Voice ID or name")
    speed: float = Field(1.0, ge=0.5, le=2.0, description="Speech rate/speed")
    pitch: float = Field(0.0, ge=-50.0, le=50.0, description="Pitch adjustment")
    volume: float = Field(0.0, ge=-50.0, le=50.0, description="Volume adjustment")
    ref_audio_path: Optional[str] = Field(None, description="Path to reference audio for voice cloning (Vieneu)")
    temperature: float = Field(0.8, ge=0.1, le=1.5, description="Vieneu sampling temperature")

@router.get("/voices")
def get_all_voices():
    """
    Get all available voices grouped by engine.
    """
    vieneu_svc = VieneuService.get_instance()
    edge_svc = EdgeTTSService.get_instance()
    google_svc = GoogleTTSService.get_instance()

    return {
        "vieneu": vieneu_svc.list_preset_voices(),
        "edge": edge_svc.list_voices(),
        "google": google_svc.list_voices()
    }

@router.post("/tts/generate")
async def generate_tts(req: GenerateTTSRequest):
    """
    Generate audio speech from text.
    """
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text parameter cannot be empty.")

    try:
        engine = req.engine.lower()
        result = None

        if engine == "vieneu":
            vieneu_svc = VieneuService.get_instance()
            result = vieneu_svc.generate_speech(
                text=req.text,
                voice_id=req.voice_id,
                ref_audio_path=req.ref_audio_path,
                speed=req.speed,
                temperature=req.temperature
            )
        elif engine == "edge":
            edge_svc = EdgeTTSService.get_instance()
            result = await edge_svc.generate_speech(
                text=req.text,
                voice_id=req.voice_id,
                speed=req.speed,
                pitch=req.pitch,
                volume=req.volume
            )
        elif engine == "google":
            google_svc = GoogleTTSService.get_instance()
            result = google_svc.generate_speech(
                text=req.text,
                lang=req.voice_id
            )
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported engine '{engine}'.")

        # Save to history
        AUDIO_HISTORY.insert(0, result)
        # Keep last 50 history entries
        if len(AUDIO_HISTORY) > 50:
            AUDIO_HISTORY.pop()

        return result

    except Exception as e:
        print(f"Error generating TTS audio: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/audio/upload-ref")
async def upload_reference_audio(file: UploadFile = File(...)):
    """
    Upload a reference audio file (.wav, .mp3, .flac) for voice cloning.
    """
    allowed_extensions = {".wav", ".mp3", ".flac", ".m4a", ".ogg"}
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"Unsupported file format '{ext}'. Allowed formats: WAV, MP3, FLAC, M4A, OGG.")

    ref_dir = "backend/static/audio/references"
    os.makedirs(ref_dir, exist_ok=True)
    
    file_id = f"ref_{uuid.uuid4().hex[:8]}"
    saved_filename = f"{file_id}{ext}"
    saved_path = os.path.join(ref_dir, saved_filename)

    with open(saved_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "id": file_id,
        "filename": file.filename,
        "filepath": saved_path,
        "url": f"/static/audio/references/{saved_filename}"
    }

@router.get("/tts/history")
def get_history():
    """
    Get list of generated audio history clips.
    """
    return AUDIO_HISTORY

@router.delete("/tts/history/{file_id}")
def delete_history_item(file_id: str):
    """
    Delete a history audio clip.
    """
    global AUDIO_HISTORY
    item = next((x for x in AUDIO_HISTORY if x["id"] == file_id), None)
    if item:
        if os.path.exists(item["filepath"]):
            try:
                os.remove(item["filepath"])
            except Exception:
                pass
        AUDIO_HISTORY = [x for x in AUDIO_HISTORY if x["id"] != file_id]
        return {"status": "success", "message": f"Deleted {file_id}"}
    raise HTTPException(status_code=404, detail="Audio item not found")
