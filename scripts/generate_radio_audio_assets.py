import os
import sys
import time
from gtts import gTTS

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from modules.mod1_copilot import LOCAL_RADIO_BROADCASTS, get_gtts_lang

OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "audio"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_scenario_slug(name: str) -> str:
    if "Maize" in name:
        return "maize"
    elif "Cattle" in name:
        return "cattle"
    elif "Poultry" in name:
        return "poultry"
    elif "Cuniculture" in name:
        return "cuniculture"
    return "broadcast"

def get_lang_slug(lang: str) -> str:
    l = lang.lower()
    if "français" in l or "french" in l:
        return "fr"
    elif "hausa" in l:
        return "ha"
    elif "yoruba" in l:
        return "yo"
    elif "swahili" in l:
        return "sw"
    elif "pidgin" in l:
        return "pidgin"
    return "en"

def main():
    print(f"Generating radio audio assets into: {OUTPUT_DIR}")
    total = sum(len(sc["languages"]) for sc in LOCAL_RADIO_BROADCASTS.values())
    count = 0

    for sc_name, sc_data in LOCAL_RADIO_BROADCASTS.items():
        sc_slug = get_scenario_slug(sc_name)
        for lang_name, lang_data in sc_data["languages"].items():
            count += 1
            l_slug = get_lang_slug(lang_name)
            filename = f"{sc_slug}_{l_slug}.mp3"
            filepath = os.path.join(OUTPUT_DIR, filename)

            if os.path.exists(filepath) and os.path.getsize(filepath) > 10000:
                print(f"[{count}/{total}] Skipping {filename} (already exists, {os.path.getsize(filepath)} bytes)")
                continue

            script_text = lang_data.get("audio_script", "").strip()
            lang_code, tld = get_gtts_lang(lang_name)
            
            print(f"[{count}/{total}] Generating {filename} ({lang_code}, tld={tld})...", end=" ", flush=True)
            success = False
            for attempt in range(3):
                try:
                    tts = gTTS(text=script_text, lang=lang_code, tld=tld, slow=False)
                    tts.save(filepath)
                    print(f"DONE ({os.path.getsize(filepath)} bytes)")
                    success = True
                    break
                except Exception as e:
                    print(f"Attempt {attempt+1} failed: {e}. Retrying in 2s...", end=" ", flush=True)
                    time.sleep(2)
            
            if not success:
                print(f"FAILED for {filename}!")
            time.sleep(1)

    print("\nGeneration process complete.")

if __name__ == "__main__":
    main()
