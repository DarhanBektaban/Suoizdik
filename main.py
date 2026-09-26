from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="suoizdik API")

# Кез келген сайттан, қосымшадан қолжетімді болуы үшін
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

# 1-қызмет: Сөз туралы мәлімет
@app.get("/api/v1/word")
def get_word(word: str = Query(...)):
    word_clean = word.lower().strip()
    file_path = os.path.join(AUDIO_DIR, f"{word_clean}.mp3")
    has_audio = os.path.exists(file_path)
    
    return JSONResponse({
        "status": "success",
        "bektaban": word_clean,
        "cyrillic": to_cyrillic(word_clean),
        "has_audio": has_audio,
        "audio_url": f"/api/v1/audio?word={word_clean}" if has_audio else None
    })

# 2-қызмет: Сөздің таза дыбысын әуен ретінде тікелей қайтару
@app.get("/api/v1/audio")
def get_audio(word: str = Query(...)):
    word_clean = word.lower().strip()
    file_path = os.path.join(AUDIO_DIR, f"{word_clean}.mp3")

    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/mpeg")
    else:
        raise HTTPException(status_code=404, detail="Audio tabylmady")
