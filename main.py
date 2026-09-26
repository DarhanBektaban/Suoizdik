from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(
    title="suoizdik API",
    description="Darhan Bektaban ailippesine arnalghan ashyq suoizdik zhaine audio API",
    version="1.0.0"
)

# Кез келген веб-сайттан сұраныс қабылдауға рұқсат (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

AUDIO_DIR = "audio"

def to_cyrillic(text: str) -> str:
    return (text.lower()
        .replace("uoil", "өл").replace("uoi", "ө")
        .replace("kui", "кү").replace("ui", "ү")
        .replace("ai", "ә")
        .replace("gn", "ң")
        .replace("gh", "ғ")
        .replace("sh", "ш")
        .replace("zh", "ж")
        .replace("uu", "у")
        .replace("q", "қ")
        .replace("j", "й"))

# 1-қызмет: Сөз туралы мәлімет беру (JSON)
@app.get("/api/v1/word")
def get_word_info(word: str = Query(..., description="Tekseriletin suoiz")):
    word_clean = word.lower().strip()
    audio_exists = os.path.exists(os.path.join(AUDIO_DIR, f"{word_clean}.mp3"))
    
    return JSONResponse({
        "status": "success",
        "bektaban": word_clean,
        "cyrillic": to_cyrillic(word_clean),
        "has_audio": audio_exists,
        "audio_url": f"/api/v1/audio?word={word_clean}" if audio_exists else None
    })

# 2-қызмет: Сөздің таза MP3 дыбысын беру
@app.get("/api/v1/audio")
def get_audio_stream(word: str = Query(..., description="Dybystalatyn suoiz")):
    word_clean = word.lower().strip()
    file_path = os.path.join(AUDIO_DIR, f"{word_clean}.mp3")

    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/mpeg", filename=f"{word_clean}.mp3")
    else:
        raise HTTPException(status_code=404, detail="Bunday suoizdin audio fajly tabylmady")
