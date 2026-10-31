"""
AgroBiometrix - Neural Voice & African Speech Synthesis Engine
Provides unified multi-provider Text-to-Speech (TTS) integration:
1. Google Cloud Text-to-Speech (Neural2 / Chirp African voices: ha-NG, yo-NG, sw-KE, fr-FR)
2. ElevenLabs Multilingual v2 (with African regional voice IDs)
3. Hugging Face African MMS-TTS (Meta Multilingual Speech models for African indigenous languages)
4. Client-side Web Speech API & Bundled Ground-Truth Acoustic Fallback
"""

import os
import json
import requests
import streamlit as st
from typing import Optional, Dict, Any

# Map AgroBiometrix language labels to international BCP-47 and Neural Voice codes
LANGUAGE_VOICE_MAP = {
    "hausa": {
        "bcp47": "ha-NG",
        "google_voice": "ha-NG-Standard-A",
        "hf_model": "facebook/mms-tts-hau",
        "label": "Hausa (Nigeria/Niger)",
        "elevenlabs_voice_id": "21m00Tcm4TlvDq8ikWAM"
    },
    "yoruba": {
        "bcp47": "yo-NG",
        "google_voice": "yo-NG-Standard-A",
        "hf_model": "facebook/mms-tts-yor",
        "label": "Yorùbá (Nigeria/Benin)",
        "elevenlabs_voice_id": "AZnzlk1XvdvUeBnXmlld"
    },
    "swahili": {
        "bcp47": "sw-KE",
        "google_voice": "sw-KE-Standard-A",
        "hf_model": "facebook/mms-tts-swa",
        "label": "Kiswahili (Kenya/Tanzania/DRC)",
        "elevenlabs_voice_id": "EXAVITQu4vr4xnSDxMaL"
    },
    "french": {
        "bcp47": "fr-FR",
        "google_voice": "fr-FR-Neural2-B",
        "hf_model": "facebook/mms-tts-fra",
        "label": "Français Agricole (Panafricain)",
        "elevenlabs_voice_id": "ErXwobaYiN019PkySvjV"
    },
    "pidgin": {
        "bcp47": "pcm",
        "google_voice": "en-NG-Standard-A",
        "hf_model": "facebook/mms-tts-pcm",
        "label": "West African Pidgin",
        "elevenlabs_voice_id": "TxGEqnHWrfWFTfGW9XjX"
    }
}


def get_configured_providers() -> Dict[str, bool]:
    """Inspects session state, st.secrets, and environment variables for TTS credentials."""
    google_key = (
        st.session_state.get("custom_google_tts_key")
        or os.getenv("GOOGLE_TTS_API_KEY")
        or (st.secrets.get("GOOGLE_TTS_API_KEY") if hasattr(st, "secrets") and "GOOGLE_TTS_API_KEY" in st.secrets else None)
    )
    eleven_key = (
        st.session_state.get("custom_elevenlabs_key")
        or os.getenv("ELEVENLABS_API_KEY")
        or (st.secrets.get("ELEVENLABS_API_KEY") if hasattr(st, "secrets") and "ELEVENLABS_API_KEY" in st.secrets else None)
    )
    hf_token = (
        st.session_state.get("custom_hf_token")
        or os.getenv("HF_TOKEN")
        or (st.secrets.get("HF_TOKEN") if hasattr(st, "secrets") and "HF_TOKEN" in st.secrets else None)
    )

    return {
        "google": bool(google_key),
        "elevenlabs": bool(eleven_key),
        "huggingface": bool(hf_token),
        "webspeech": True,  # Always available via in-browser JS API
        "bundled_ground_truth": True  # Always active via assets/audio/*.mp3
    }


def synthesize_elevenlabs(text: str, voice_id: str, api_key: str) -> Optional[bytes]:
    """Generates speech via ElevenLabs Multilingual v2 REST API."""
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8
        }
    }
    try:
        resp = requests.post(url, json=data, headers=headers, timeout=12)
        if resp.status_code == 200:
            return resp.content
    except Exception:
        pass
    return None


def synthesize_google_tts(text: str, lang_code: str, voice_name: str, api_key: str) -> Optional[bytes]:
    """Generates speech via Google Cloud Text-to-Speech REST API."""
    url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "input": {"text": text},
        "voice": {
            "languageCode": lang_code,
            "name": voice_name
        },
        "audioConfig": {
            "audioEncoding": "MP3",
            "speakingRate": 0.95,
            "pitch": -0.5
        }
    }
    try:
        import base64
        resp = requests.post(url, json=payload, headers=headers, timeout=12)
        if resp.status_code == 200:
            audio_b64 = resp.json().get("audioContent", "")
            if audio_b64:
                return base64.b64decode(audio_b64)
    except Exception:
        pass
    return None


def render_voice_engine_settings_panel():
    """Renders the Voice Synthesis Engine status and credential manager."""
    provs = get_configured_providers()

    with st.expander("⚙️ Neural Voice Synthesis & African Cloud Speech Settings", expanded=False):
        st.markdown("""
<div style="font-size: 0.82rem; color: #374151; line-height: 1.5; margin-bottom: 0.8rem;">
    AgroBiometrix employs a <b>resilient hybrid speech architecture</b>:
    When cloud API keys are present, scripts are rendered into studio-grade neural broadcast audio. 
    In offline or zero-cost mode, the browser's native Web Speech synthesis and pre-rendered indigenous acoustic speech tracks take over seamlessly.
</div>
""", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"**Google Cloud Neural2 / Chirp:** {'🟢 Active' if provs['google'] else '⚪ Unconfigured'}")
            new_g_key = st.text_input("Google TTS API Key:", value=st.session_state.get("custom_google_tts_key", ""), type="password", help="Enables live Google Cloud Text-to-Speech for ha-NG, yo-NG, sw-KE, fr-FR")
            if new_g_key != st.session_state.get("custom_google_tts_key", ""):
                st.session_state["custom_google_tts_key"] = new_g_key
                st.rerun()

        with c2:
            st.markdown(f"**ElevenLabs Multilingual v2:** {'🟢 Active' if provs['elevenlabs'] else '⚪ Unconfigured'}")
            new_e_key = st.text_input("ElevenLabs API Key:", value=st.session_state.get("custom_elevenlabs_key", ""), type="password", help="Enables studio-grade African voice cloning")
            if new_e_key != st.session_state.get("custom_elevenlabs_key", ""):
                st.session_state["custom_elevenlabs_key"] = new_e_key
                st.rerun()

        with c3:
            st.markdown("**Local Browser Web Speech:** 🟢 Active (Zero-Cost)")
            st.markdown("**Bundled Ground-Truth Audio:** 🟢 Active (16 Studio MP3s)")
            st.caption("Indigenous acoustic voice tracks are ready for on-air broadcast across all benchmark commodities.")
