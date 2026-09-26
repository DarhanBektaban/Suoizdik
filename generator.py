import os
import time
from gtts import gTTS

# Дархан Бектабан әліпбиін қазақша кириллге айналдыру (дыбыстауға арналған)
def bektaban_to_kazakh(text):
    text = text.lower()
    replacements = [
        ("uoil", "өл"), ("uoi", "ө"),
        ("kui", "кү"), ("ui", "ү"),
        ("ai", "ә"), ("gn", "ң"),
        ("gh", "ғ"), ("sh", "ш"),
        ("zh", "ж"), ("uu", "у"),
        ("q", "қ"), ("j", "й")
    ]
    for lat, cyr in replacements:
        text = text.replace(lat, cyr)
    return text

# Сіздің сөздеріңіздің тізімі
words = [
    "adam", "bala", "uoimir", "til", "kitap", "quuanysh", "zhaqsy", "suoiz", 
    "otbasy", "dostyq", "mektep", "elim", "birlik", "egnbek", "suoizdik",
    "aba", "abaj", "abajla", "adal", "adym", "agha", "aghash", "aj", "ajaq",
    "altyn", "ana", "aqyl", "arman", "aspan", "ata", "auua", "auuyl", "azamat",
    "baqyt", "bar", "bas", "batyr", "bilim", "bir", "bostandyq", "dala", "dem",
    "dos", "durys", "eki", "el", "ertegn", "esen", "esep", "esik", "ghylym",
    "guil", "habar", "halyq", "is", "ish", "izdeuu", "kel", "kerek", "keshirim",
    "kuin", "kuish", "kuoik", "kuoiz", "maqsat", "mal", "mejirimdi", "men",
    "mereke", "mura", "namys", "nazar", "oj", "on", "oquu", "oqytuu", "orman",
    "otan", "pajda", "qalam", "qala", "qazaq", "qazhet", "qazir", "qol",
    "qurmet", "raqmet", "sabaq", "sabyr", "saghat", "sailem", "san", "saqtauu",
    "senim", "suu", "suuret", "tabjghat", "tabys", "taghdyr", "tagn", "talap",
    "tamaq", "taza", "temir", "teregn", "tilek", "toq", "tura", "tuz", "tynysh",
    "uij", "uilken", "uimit", "uin", "uish", "uoilim", "uoiner", "uoizen",
    "uuaqyt", "uzyn", "ystyq", "zaman", "zat", "zhaghdaj", "zhagna", "zhaj",
    "zhalghyz", "zhaman", "zhan", "zharqyn", "zhas", "zhaz", "zhazuu", "zher",
    "zhete", "zheti", "zhigit", "zhol", "zholdas", "zhoq", "zhuldyz", "zhuma",
    "zhumys", "zhurek", "zhurt", "zhyl", "zhyldam"
]

# Аудиолар сақталатын қалта
OUTPUT_DIR = "audio"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"Барлығы {len(words)} сөзді дыбыстау басталды...\n")

for word in words:
    file_path = os.path.join(OUTPUT_DIR, f"{word}.mp3")
    
    # Егер файл бұрыннан бар болса, қайта жасамай өткізіп жібереді
    if os.path.exists(file_path):
        continue
    
    kazakh_text = bektaban_to_kazakh(word)
    
    try:
        # Қазақ тіліндегі дыбыс жиілігімен MP3 жасау
        tts = gTTS(text=kazakh_text, lang='kk', slow=False)
        tts.save(file_path)
        print(f"Жазылды: {word}.mp3 ({kazakh_text})")
        time.sleep(0.3)  # Серверге салмақ түсірмеу үшін сәл үзіліс
    except Exception as e:
        print(f"Қате ({word}): {e}")

print("\nБарлық сөздер сәтті сақталды! 'audio/' қалтасын ашып көре аласыз.")
