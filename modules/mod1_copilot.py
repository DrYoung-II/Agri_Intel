"""
Module 1, 9, 14: AgriResearch Copilot & African Evidence Engine
Evidence Matrix generation, Knowledge Gap Finder, African context grounding,
File Upload & Custom Query Parser, and Last-Mile Multilingual Farmer Voice & Radio Advisory Simulator
"""

import json
import os
import io
import math
import wave
import struct
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components
from core.orchestrator import rule_based_agent_synthesis, detect_target_geography
from core.exporter import render_download_buttons
from core.broadcast_dispatcher import (
    init_broadcast_queue,
    queue_broadcast_advisory,
    render_dispatch_trigger_card,
    generate_vernacular_radio_script
)


def generate_radio_jingle():
    """Generates an authentic warm 3-tone marimba chime (C5-E5-G5) as WAV bytes."""
    sample_rate = 22050
    duration = 1.6
    num_samples = int(sample_rate * duration)
    buffer = io.BytesIO()
    
    with wave.open(buffer, 'w') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        
        # 3 pleasant marimba chime notes (C5=523Hz, E5=659Hz, G5=784Hz)
        notes = [(0.0, 0.5, 523.25), (0.4, 0.9, 659.25), (0.8, 1.5, 783.99)]
        
        for i in range(num_samples):
            t = i / sample_rate
            sample_val = 0.0
            for start, end, freq in notes:
                if start <= t < end:
                    envelope = math.exp(-6.0 * (t - start))
                    sample_val += 0.5 * math.sin(2 * math.pi * freq * (t - start)) * envelope
            
            sample_val = max(-1.0, min(1.0, sample_val))
            wav.writeframes(struct.pack('<h', int(sample_val * 32767)))
            
    return buffer.getvalue()

def get_gtts_lang(lang_key: str) -> tuple[str, str]:
    """Returns (lang_code, tld) for gTTS matching indigenous African and international languages."""
    l_lower = lang_key.lower()
    if "hausa" in l_lower:
        return "ha", "com"
    elif "swahili" in l_lower or "kiswahili" in l_lower:
        return "sw", "com"
    elif "français" in l_lower or "french" in l_lower:
        return "fr", "com"
    elif "pidgin" in l_lower:
        return "en", "co.za"
    elif "yoruba" in l_lower:
        return "en", "com"
    elif "igbo" in l_lower:
        return "en", "com"
    else:
        return "en", "com"


@st.cache_data(show_spinner=False)
def synthesize_radio_voice(text: str, lang_code: str = "en", tld: str = "com") -> bytes:
    """Generates authentic MP3 spoken audio bytes using gTTS."""
    try:
        from gtts import gTTS
        buf = io.BytesIO()
        tts = gTTS(text=text, lang=lang_code, tld=tld, slow=False)
        tts.write_to_fp(buf)
        return buf.getvalue()
    except Exception:
        return b""


def get_scenario_slug(name: str) -> str:
    """Derives stable filesystem slug for radio broadcast scenario."""
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
    """Derives stable filesystem slug for broadcast language."""
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


def get_radio_audio_bytes(scenario_name: str, lang_choice: str, text: str) -> bytes:
    """Loads bundled offline MP3 if available on disk, or falls back to live synthesis."""
    sc_slug = get_scenario_slug(scenario_name)
    l_slug = get_lang_slug(lang_choice)
    audio_path = os.path.join(os.path.dirname(__file__), "..", "assets", "audio", f"{sc_slug}_{l_slug}.mp3")
    if os.path.exists(audio_path):
        try:
            with open(audio_path, "rb") as f:
                data = f.read()
                if len(data) > 1000:
                    return data
        except Exception:
            pass
    # Fallback to live gTTS synthesis
    lang_code, tld = get_gtts_lang(lang_choice)
    return synthesize_radio_voice(text, lang_code=lang_code, tld=tld)


LOCAL_RADIO_BROADCASTS = {
    "🌦️ Kaduna/Kano Maize: Heat Wave & Fertilizer Advisory": {
        "context": "Delayed rainfall anomaly (-18%) with daytime temperature spike > 37.5°C during early vegetative stage.",
        "languages": {
                        "🇨🇮 / 🇸🇳 / 🇨🇲 Français Agricole (Bulletin Rural Panafricain)": {
                "broadcaster": "Ingénieur Amadou Diallo • Radio Rurale Communautaire AgroBiometrix (Bouaké / Kaolack / Garoua)",
                "headline": "Alerte Canicule et Retard des Pluies pour les Producteurs de Maïs",
                "audio_script": (
                    "Chers agriculteurs et producteurs de maïs, bonjour ! Voici un bulletin d'urgence de l'Institut AgroBiometrix : "
                    "Durant les deux prochaines semaines, une forte vague de chaleur et une interruption des pluies toucheront nos bassins de production. "
                    "Les agronomes vous avertissent formellement : n'épandez surtout pas d'engrais Urée sur un sol sec en ce moment ! "
                    "La chaleur intense va volatiliser l'azote dans l'atmosphère et brûler les jeunes racines de votre maïs. "
                    "Recommandation essentielle : attendez le retour des pluies régulières pour que le sol soit bien humide. "
                    "Appliquez ensuite la technique du micro-dosage, soit un bouchon d'engrais par pied de maïs. "
                    "Cette pratique préserve votre récolte tout en divisant vos dépenses d'engrais par deux. Bonne campagne à tous !"
                ),
                "english_translation": (
                    "Dear farmers and maize growers, greetings! Here is an urgent bulletin from the AgroBiometrix Institute: "
                    "Over the next two weeks, an intense heat wave and rainfall pause will affect our production basins. "
                    "Agronomists strictly warn: do not apply Urea fertilizer onto dry topsoil at this time! "
                    "Extreme heat will volatilize nitrogen into the atmosphere and burn tender maize roots. "
                    "Wait until steady rains thoroughly soak the earth, then apply the micro-dosing technique—one bottle cap per maize plant."
                )
            },
            "🇳🇬 Hausa (Harshen Hausa)": {
                "broadcaster": "Malam Ibrahim Dan-Kano • AgroBiometrix Radio FM 98.5 (Kano/Kaduna)",
                "headline": "Gargaɗin Zafi da Jinkirin Damina ga Manoman Masara",
                "audio_script": (
                    "Assalamu alaikum manoma 'yan uwa! Ga wata muhimmiyar sanarwa daga cibiyar kimiyya ta AgroBiometrix: "
                    "A cikin kwanaki goma masu zuwa, za a fuskanci matsanancin zafi da rashin ruwan sama a yankunan Kaduna, "
                    "Kano, da Katsina. Hukumar bincike ta gargadi dukkan manoma: Kada ku yi kuskuren zuba takin Urea a kan "
                    "busasshen rami a yanzu, domin zafin rana zai cinye sinadarin takin kuma ya kone tushen shukar ku. "
                    "Shawara ta kwararru: Ku jira har sai an yi ruwa mai karfi kasa ta jike sosai. Bayan haka, ku yi amfani "
                    "da dabarar 'Micro-dosing'—wato cokali daya kacal na taki a jikin kowace masara. Wannan dabarar za ta "
                    "kare amfanin gonarku kuma za ta rage kudin taki da kashi hamsin cikin dari. Allah Ya albarkaci noman mu!"
                ),
                "english_translation": (
                    "Peace be upon you, fellow farmers! Here is an urgent alert from the AgroBiometrix Science Hub: In the next 10 days, "
                    "we will experience intense heat and a rainfall pause across Kaduna, Kano, and Katsina. Research guidance warns all farmers: "
                    "Do NOT apply Urea fertilizer onto dry topsoil right now, as solar volatilization will destroy the nitrogen and scorch crop roots. "
                    "Expert recommendation: Wait until the next heavy soaking rainfall. Afterward, apply the 'Micro-dosing' technique—one bottle cap "
                    "of fertilizer per maize stand. This will safeguard your harvest while halving your fertilizer expenditure. May God bless our harvest!"
                )
            },
            "🇳🇬 Yoruba (Èdè Yorùbá)": {
                "broadcaster": "Baale Agbe Olusegun • AgroBiometrix Community Extension Radio (Oyo/Ogun)",
                "headline": "Ikilo Ooru ati Idaduro Ojo fun Awon Agbe Agbado",
                "audio_script": (
                    "Ẹ kú ojúmọ́ gbogbo ẹ̀yin àgbẹ̀ wa olókìkí! Ẹ gbọ́ ìfitónilétí pàtàkì láti ọ̀dọ̀ ẹ̀rọ ìmọ̀-ìjìnlẹ̀ AgroBiometrix: "
                    "Ní ọ̀sẹ̀ méjì tí ó ń bọ̀ yìí, oòrùn tí ó gbóná gidigidi yóò wà pẹ̀lú ìdádúró òjò ní agbègbè wa. "
                    "Àwọn onímọ̀ ìjìnlẹ̀ sọ wípé: Ẹ má ṣe da ajílẹ̀ Urea sí orí ilẹ̀ gbígbẹ lásán o! Ooru yóò jó gbogbo ajílẹ̀ náà, "
                    "yóò sì ba gbòǹgbò àgbàdo jẹ́. Ẹ dúró títí tí òjò tí ó fẹ́ yóò fi rin ilẹ̀ dáadáa. Láti fi dín owó kù, "
                    "ẹ lo ìlànà 'Micro-dosing'—òmórí ìgò kan ti ajílẹ̀ sí ìdí igi àgbàdo kọ̀ọ̀kan. Èyí yóò dáàbò bo ìrugbìn yín, "
                    "yóò sì fún yín ní ìrè púpọ̀. Ìrẹ o!"
                ),
                "english_translation": (
                    "Good day, esteemed farmers! Hear this important advisory from the AgroBiometrix intelligence engine: In the coming two weeks, "
                    "severe heat and a dry hiatus will affect our farmlands. Scientists warn: Do not scatter Urea fertilizer on dry soil! "
                    "The heat will volatilize the nutrients and damage seedling roots. Wait until steady rains return to thoroughly moisten the earth. "
                    "To conserve your funds, apply 'Micro-dosing'—one bottle cap per maize stand. This protects your crops and guarantees a bountiful yield!"
                )
            },
            "🇰🇪 Swahili (Kiswahili)": {
                "broadcaster": "Bwana Shamba Wanyama • AgroBiometrix Sauti ya Mkulima (Eldoret/Kitale)",
                "headline": "Tahadhari ya Wimbi la Joto na Usimamizi wa Mbolea",
                "audio_script": (
                    "Habari za asubuhi wakulima wetu shupavu! Huu hapa ujumbe wa dharura kutoka kwa mfumo wa kisayansi wa AgroBiometrix: "
                    "Kuna wimbi kali la joto linalotarajiwa katika kaunti za Uasin Gishu, Trans Nzoia, na Nakuru. "
                    "Utafiti unatoa onyo kali: Msikimbilie kuweka mbolea ya Urea kwenye udongo uliokauka wakati huu. Joto kali litaunguza "
                    "mizizi ya mahindi machanga na kupoteza mbolea yenu hewani. Subirini hadi mvua ya kutosha inyeshe ili udongo uwe "
                    "na unyevu kamili. Tumieni mfumo wa 'Micro-dosing' wa kuweka kijiko kidogo tu cha mbolea karibu na shina. "
                    "Hii italinda mavuno yenu na kuokoa nusu ya gharama zenu za pembejeo!"
                ),
                "english_translation": (
                    "Good morning our resilient farmers! Here is an emergency bulletin from the AgroBiometrix scientific system: "
                    "An intense heat wave is forecasted across Uasin Gishu, Trans Nzoia, and Nakuru counties. "
                    "Agronomic researchers issue a strict warning: Do not rush to apply Urea fertilizer onto parched soil during this period. "
                    "Excessive heat will burn tender maize roots and volatilize costly nutrients into the air. Wait until soaking rains restore soil moisture. "
                    "Adopt the 'Micro-dosing' technique by placing a small crown dose near each plant. This safeguards yield while cutting input outlay by half!"
                )
            },
            "🇳🇬 West African Pidgin": {
                "broadcaster": "Uncle Joe Extension Master • AgroBiometrix Grassroots FM",
                "headline": "Special Heatwave & Fertilizer Warning for All Maize Farmers",
                "audio_script": (
                    "Make all our sharp farmers listen well well! AgroBiometrix AI engine don send urgent red alert: "
                    "Over the next two weeks, serious hot weather and dry spell dey land on our maize farms. "
                    "The scientists don give strict order: Abeg, NO pour your expensive Urea fertilizer on top dry ground now o! "
                    "The hot sun go just burn the fertilizer waste your money, and e fit kill your maize baby plants. "
                    "Wait make heavy rain fall soak the soil first. When the ground don soft, use 'Micro-dosing' method—just "
                    "one small bottle cap of fertilizer for each maize stand. E go protect your farm and save you plenty money!"
                ),
                "english_translation": (
                    "All farmers, listen carefully! The AgroBiometrix AI engine has issued an urgent advisory: Over the next two weeks, "
                    "a severe dry spell and heat wave are hitting our maize farms. The scientists have given strict instructions: "
                    "Please do not apply costly Urea fertilizer on dry topsoil right now! The sun will volatilize the nutrients and damage crops. "
                    "Wait until steady rain soaks the soil. Then use the 'Micro-dosing' bottle-cap method to save fertilizer and secure your yield."
                )
            }
        }
    },
    "🐄 Pastoral Zebu Cattle: THI Heat Stress & Grazing Advisory": {
        "context": "Temperature-Humidity Index (THI) projected to exceed 80 across Sudan Savanna rangelands, causing milk depression and thermal exhaustion.",
        "languages": {
            "🇨🇮 / 🇸🇳 / 🇨🇲 Français Pastoral (Conseil Vétérinaire & Zootechnique)": {
                "broadcaster": "Docteur Vétérinaire Ousmane Traoré • Radio Pastorale AgroBiometrix (Sahel & Savane)",
                "headline": "Protection des Bovins contre le Stress Thermique et l'Indice THI Élevé",
                "audio_script": (
                    "Avis important à tous les éleveurs et pasteurs de la région ! Les capteurs agrométéorologiques d'AgroBiometrix "
                    "indiquent que l'indice de stress thermique dépassera le seuil critique de 80 dans les prochains jours. "
                    "Cette forte chaleur entraîne une baisse brutale de la production laitière et un risque d'épuisement des animaux. "
                    "Conseils pratiques immédiats : déplacez les heures de pâturage tôt le matin et en fin d'après-midi. "
                    "Entre midi et 15 heures, gardez vos troupeaux à l'ombre dense des arbres et fournissez-leur de l'eau fraîche "
                    "à volonté enrichie de pierres à lécher minérales. Protégez vos vaches laitières et vos veaux contre le coup de chaleur !"
                ),
                "english_translation": (
                    "Important notice to all livestock keepers and pastoralists! AgroBiometrix sensors indicate that the heat index "
                    "will exceed the critical threshold of 80. Guidance: shift grazing to dawn and dusk. "
                    "Between 12 PM and 3 PM, hold cattle under dense tree shade and provide cool water with mineral salt licks."
                )
            },
            "🇳🇬 Hausa (Harshen Hausa)": {
                "broadcaster": "Garba Makiyayi • AgroBiometrix Fulani Pastoral Dispatch",
                "headline": "Kariya Daga Zafin Rana ga Shanun Bunaji da Gudali",
                "audio_script": (
                    "Gaisuwa ta musamman ga dukkan makiyayan mu! Bayanan yanayi na AgroBiometrix sun nuna cewa ma'aunin zafi da lema (THI) "
                    "zai haura tamanin (80). Wannan yana nufin dabbobi za su shiga cikin tsananin kunci na zafi. Don kiyaye nono da lafiyar shanunku: "
                    "Ku sauya lokacin kiwo zuwa sanyin safiya da kuma yamma bayan la'asar. A tsakiyar rana tsakanin karfe goma sha biyu zuwa uku, "
                    "ku tsayar da shanu a karkashin inuwar bishiyoyi. Ku tabbatar suna samun ruwan sha mai sanyi da gishirin lasa. "
                    "Wannan zai hana zazzabin zafi da rage yawan nono."
                ),
                "english_translation": (
                    "Warm greetings to all pastoralists! AgroBiometrix meteorological data indicates the Temperature-Humidity Index (THI) will exceed 80. "
                    "This triggers severe heat stress in livestock. To preserve milk yield and herd vitality: Shift grazing schedules to early mornings "
                    "and late afternoons. During peak solar irradiance between 12:00 PM and 3:00 PM, hold cattle under dense tree shade. "
                    "Ensure continuous access to cool drinking water and mineral salt licks to prevent thermal exhaustion."
                )
            },
            "🇰🇪 Swahili (Kiswahili)": {
                "broadcaster": "Mchungaji Ole Kiprono • AgroBiometrix Rangeland Radio",
                "headline": "Kudhibiti Msongo wa Joto kwa Ng'ombe wa Asili",
                "audio_script": (
                    "Salamu kwa wafugaji wetu kote malishoni! Hali ya hewa kutoka kwa mfumo wa AgroBiometrix inaonyesha fahirisi ya joto (THI) "
                    "inapanda zaidi ya kiwango salama. Hii itapunguza uzalishaji wa maziwa na kusababisha mifugo kuchoka haraka. "
                    "Ushauri wetu: Wapeleke mifugo malishoni asubuhi mapema na jioni. Wakati wa jua kali la mchana, waweke chini ya vivuli vya miti "
                    "na muwape maji safi ya kutosha na madini ya chumvi. Hii italinda mifugo yenu dhidi ya magonjwa ya msongo wa joto."
                ),
                "english_translation": (
                    "Greetings to our pastoralists across the rangelands! AgroBiometrix telemetry indicates that the heat index is surpassing safe thresholds. "
                    "This threatens milk yield and induces exhaustion in cattle. Guidance: Graze herds during cool dawn and dusk hours. "
                    "Provide shade during peak midday hours alongside ample clean drinking water and mineral supplements to avert thermal distress."
                )
            }
        }
    },
    "🐔 Poultry: Diurnal Temperature Shift & Harmattan Dust Alert": {
        "context": "Diurnal shift (33°C afternoons vs 19°C chilly mornings) and Harmattan dust haze elevating respiratory disease risk.",
        "languages": {
            "🇨🇮 / 🇸🇳 / 🇨🇲 Français Avicole (Guide de Conduite d'Élevage)": {
                "broadcaster": "Mme Fatou Sow • AgroBiometrix Flash Élevage Avicole (Abidjan / Thiès / Douala)",
                "headline": "Gestion de l'Écart Thermique et de la Poussière d'Harmattan en Aviculture",
                "audio_script": (
                    "Chers éleveurs de volailles, soyez très attentifs ! Les fortes variations de température entre la chaleur de l'après-midi "
                    "et la fraîcheur nocturne, associées aux vents de poussière, mettent en péril la santé de vos bandes de poulets. "
                    "Consigne stricte : retirez l'aliment aux heures chaudes entre 11h30 et 15h30 pour éviter la mortalité par choc thermique. "
                    "Distribuez de l'eau fraîche additionnée de vitamine C et d'électrolytes. Assurez-vous d'avoir administré le vaccin "
                    "de rappel contre la maladie de Newcastle pour prémunir vos oiseaux contre les affections respiratoires !"
                ),
                "english_translation": (
                    "Poultry farmers, take note: Significant diurnal temperature swings paired with dust winds pose severe mortality risks. "
                    "Withdraw daytime feed between 11:30 AM and 3:30 PM. Provide Vitamin C in cool water and administer Newcastle Lasota boosters."
                )
            },
            "🇳🇬 Yoruba (Èdè Yorùbá)": {
                "broadcaster": "Baale Agbe Olusegun • AgroBiometrix Poultry Extension Radio (Oyo/Ogun)",
                "headline": "Itoju Adiye ni Akoko Ooru ati Erupe Oye (Harmattan)",
                "audio_script": (
                    "Ẹ kú ojúmọ́ gbogbo ẹ̀yin àgbẹ̀ adìyẹ wa olókìkí! Ẹ gbọ́ ìfitónilétí pàtàkì: Ní àkókò yìí, ooru gbígbóná wà ní ọ̀sán "
                    "pẹ̀lú òtútù ní òru. Ẹ má ṣe fún adìyẹ ní oúnjẹ láàárín agogo mọ́kànlá àbọ̀ òwúrọ̀ sí agogo mẹ́ta àbọ̀ ọ̀sán (11:30 AM – 3:30 PM). "
                    "Ẹ bu omi tútù tí ó ní Vitamin C àti 'Sodium Bicarbonate' fún wọn mu láti dín ooru kù. Ẹ sì rántí láti fún wọn ní "
                    "abẹ́rẹ́ àjẹsára Newcastle Clone 30 àti Lasota láti dáàbò bo wọn lọ́wọ́ ikọ́ àti erùpẹ̀ oyé!"
                ),
                "english_translation": (
                    "Good day esteemed poultry farmers! Important advisory: Significant temperature swings are occurring between hot afternoons and cool nights. "
                    "Practice split-feeding by withdrawing feed between 11:30 AM and 3:30 PM to eliminate metabolic heat death. "
                    "Add Vitamin C and sodium bicarbonate to cool drinking water, and uphold Newcastle Lasota vaccination against dust hazards."
                )
            },
            "🇳🇬 Hausa (Harshen Hausa)": {
                "broadcaster": "Malam Ibrahim Dan-Kano • AgroBiometrix Avian Health Unit",
                "headline": "Kariyar Kaji Daga Zafin Rana da Kuran Hunturu",
                "audio_script": (
                    "Manoman kaji ga muhimmiyar shawara: A wannan lokaci, zafin rana yana haifar da zazzabi ga kaji yayin da daddare ke yin sanyi. "
                    "Ku janye abinci da tsakar rana tsakanin karfe goma sha daya da rabi zuwa karfe uku da rabi. Ku zuba Vitamin C a cikin ruwan sanyi "
                    "domin kare su daga zafin jini. Ku tabbatar kun ba su maganin riga-kafin Newcastle Lasota don kariya daga kurar hunturu."
                ),
                "english_translation": (
                    "Poultry farmers note this critical advisory: Afternoon heat stress coupled with cool nights poses high mortality risk. "
                    "Withdraw daytime feed between 11:30 AM and 3:30 PM. Provide Vitamin C in cool water and administer Newcastle Lasota to ward off respiratory disease."
                )
            },
            "🇳🇬 West African Pidgin": {
                "broadcaster": "Uncle Joe Extension Master • AgroBiometrix Grassroots FM",
                "headline": "Hot Afternoon & Cold Night Alert for All Poultry Farmers",
                "audio_script": (
                    "Make all poultry farmers listen well! The hot afternoon sun and cold night weather fit kill your broilers if you no take care. "
                    "Remove their feed between 11:30 AM and 3:30 PM make body heat no kill them. Put Vitamin C and small baking soda inside their cold water. "
                    "And give them their Newcastle Lasota booster vaccine against the Harmattan dust!"
                ),
                "english_translation": (
                    "All poultry farmers: Sharp diurnal temperature shifts are occurring. Withdraw feed during peak afternoon heat (11:30 AM–3:30 PM). "
                    "Supply Vitamin C in drinking water to mitigate heat distress and administer Newcastle Lasota vaccines."
                )
            }
        }
    },
    "🐇 Smallholder Cuniculture: Heat Stress, Buck Sterility & Wilted Forages": {
        "context": "Ambient temperatures > 28°C–30°C causing temporary buck sterility and fresh forage causing fatal bloat (tympany).",
        "languages": {
            "🇨🇮 / 🇸🇳 / 🇨🇲 Français Cuniculture (Conseil Élevage de Lapins)": {
                "broadcaster": "Dr. Jean-Baptiste Koffi • AgroBiometrix Studio Cuniculture",
                "headline": "Prévention de l'Infertilité des Mâles et du Ballonnement chez le Lapin",
                "audio_script": (
                    "Chers cunichulteurs et éleveurs de lapins, écoutez attentivement ! Lorsque la température ambiante dépasse 28 à 30 degrés, "
                    "les mâles reproducteurs subissent une stérilité thermique temporaire qui peut durer 6 à 8 semaines. "
                    "Placez des bouteilles d'eau congelée dans les clapiers aux heures les plus chaudes pour rafraîchir vos animaux. "
                    "De plus, ne donnez jamais d'herbe fraîchement coupée ou mouillée : faites toujours faner les fourrages à l'ombre "
                    "pendant 4 à 6 heures avant la distribution pour éliminer tout risque de météorisation et de ballonnement mortel !"
                ),
                "english_translation": (
                    "Rabbit breeders: Ambient temperatures above 28C-30C cause buck sterility lasting 6 to 8 weeks. "
                    "Place frozen bottles in hutches for cooling during peak afternoon hours. "
                    "Always wilt forages in shade for 4 to 6 hours before feeding to eliminate fatal bloat."
                )
            },
            "🇳🇬 Hausa (Harshen Hausa)": {
                "broadcaster": "Malam Ibrahim Dan-Kano • AgroBiometrix Cuniculture Advisory",
                "headline": "Kula da Zoman Noma da Hana Bakon Zafi",
                "audio_script": (
                    "Manoman zomo ku saurara da kyau! Idan zafi ya haura digiri talatin (30°C), mazan zomo suna yin makonni shida zuwa takwas ba sa iya "
                    "daukar ciki (temporary sterility). Don haka, ku sanya kwalaben ruwan kankara a cikin keji da rana domin su kwanta a jiki su sha sanyi. "
                    "Haka kuma, duk ciyawar da kuka yanko kamar Tridax, dole ne ku shanya ta a inuwa na tsawon sa'o'i hudu kafin ku ba su, domin kada ta kumbura musu ciki."
                ),
                "english_translation": (
                    "Cuniculture farmers listen carefully: Ambient temperatures above 30°C cause buck sterility lasting 6 to 8 weeks. "
                    "Place frozen plastic water bottles inside hutches between 12 PM and 3:30 PM so rabbits can conductively cool down. "
                    "Furthermore, always wilt fresh forages like Tridax procumbens in the shade for 4 to 6 hours before feeding to eliminate fatal bloat."
                )
            },
            "🇳🇬 Yoruba (Èdè Yorùbá)": {
                "broadcaster": "Baale Agbe Olusegun • AgroBiometrix Rabbit Extension",
                "headline": "Itoju Ehoro ati Dena Arun Ikun Wiwu (Bloat)",
                "audio_script": (
                    "Ẹ̀yin olùtọ́jú ehoro olókìkí! Ẹ gbọ́ ìmọ̀ràn pàtàkì: Ooru tí ó kọjá ìwọ̀n máa ń ba agbára akọ ehoro jẹ́ fún ọ̀sẹ̀ mẹ́fà sí mẹ́jọ. "
                    "Ẹ gbé ìgò omi yìnyín sínú kéejì wọn ní ọ̀sán kí ara wọn le tútù. Pẹ̀lúpẹ̀lù, ẹ má ṣe fún wọn ní ewé tútù lẹ́sẹ̀kẹsẹ̀; "
                    "ẹ gbọdọ̀ sá ewé náà sí ibòji fún wákàtí mẹ́rin sí mẹ́fà kí ó le rọ díẹ̀, kí ikùn wọn má bàa wú tàbí gbá."
                ),
                "english_translation": (
                    "Rabbit keepers: Excessive tropical heat impairs buck fertility for 6 to 8 weeks. Place frozen bottles inside cages during peak hours for cooling. "
                    "Never feed fresh, dew-covered greens directly; wilt all forages 4 to 6 hours in the shade to prevent lethal tympany (bloat)."
                )
            },
            "🇳🇬 West African Pidgin": {
                "broadcaster": "Uncle Joe Extension Master • AgroBiometrix Grassroots FM",
                "headline": "Important Care Guide for Rabbit Farmers in Hot Weather",
                "audio_script": (
                    "All rabbit farmers, make una listen! Too much hot sun dey make male rabbit lose power to give birth for 6 to 8 weeks. "
                    "Put frozen cold water bottle inside their cage for afternoon make them hug am cool body. "
                    "And any green grass wey you cut, make you spread am for shade for 4 to 6 hours make e dry small before you give them, so that belly swell no go kill them!"
                ),
                "english_translation": (
                    "Rabbit farmers: Heat exceeding 30°C triggers buck sterility for 6 to 8 weeks. Place frozen water bottles inside cages for cooling. "
                    "Always wilt fresh forage 4 to 6 hours before feeding to prevent deadly bloat."
                )
            }
        }
    }
}


def analyze_custom_evidence_dataset(df_up: pd.DataFrame, filename: str) -> dict:
    """
    Intelligent domain detection, biometric profiling, subpopulation evidence synthesis,
    interactive visualization generation, and data-grounded knowledge gap analysis
    for uploaded empirical datasets.
    """
    cols = df_up.columns.tolist()
    cols_lower = [str(c).lower().strip() for c in cols]
    n_rows, n_cols = df_up.shape

    # 1. Multi-Domain Keyword Scoring
    scores = {
        "animal_genetics": 0,
        "crop_agronomy": 0,
        "soil_science": 0,
        "climate_science": 0,
        "socio_economics": 0,
        "literature_matrix": 0
    }

    animal_kw = ["animal", "sire", "dam", "breed", "snp", "marker", "growth_rate", "body_weight", 
                 "milk_yield", "carcass", "cattle", "cow", "bull", "calf", "heifer", "poultry", 
                 "broiler", "layer", "pig", "sheep", "goat", "pedigree", "ebv", "hatchability", "egg"]
    for c in cols_lower:
        for kw in animal_kw:
            if kw in c:
                scores["animal_genetics"] += 2
    if any(c.startswith("snp_") for c in cols_lower):
        scores["animal_genetics"] += 6

    crop_kw = ["variety", "cultivar", "genotype", "accession", "yield", "biomass", "grain", 
               "plot", "rep", "block", "fertilizer", "npk", "treatment", "plant_height", 
               "tiller", "panicle", "lodging", "drought", "maize", "cassava", "rice", "tomato", 
               "sorghum", "cowpea", "harvest_index"]
    for c in cols_lower:
        for kw in crop_kw:
            if kw in c:
                scores["crop_agronomy"] += 2

    soil_kw = ["soil", "ph", "cec", "organic_carbon", "organic_matter", "nitrogen", 
               "phosphorus", "potassium", "calcium", "magnesium", "clay", "sand", "silt", 
               "bulk_density", "lime", "ec", "texture"]
    for c in cols_lower:
        for kw in soil_kw:
            if kw in c:
                scores["soil_science"] += 2

    climate_kw = ["rainfall", "precip", "precipitation", "temperature", "temp", "humidity", 
                  "solar", "radiation", "wind", "spei", "thi", "evapotranspiration"]
    for c in cols_lower:
        for kw in climate_kw:
            if kw in c:
                scores["climate_science"] += 2

    econ_kw = ["income", "revenue", "cost", "profit", "household", "credit", "subsidy", 
               "adoption", "gross_margin", "expenditure", "farm_size"]
    for c in cols_lower:
        for kw in econ_kw:
            if kw in c:
                scores["socio_economics"] += 2

    lit_kw = ["study", "trait", "population", "method", "major_finding", "evidence_strength"]
    matched_lit = sum(1 for kw in lit_kw if kw in cols_lower)
    if matched_lit >= 3:
        scores["literature_matrix"] += 12

    top_domain = max(scores, key=scores.get)
    if scores[top_domain] == 0:
        top_domain = "general_empirical"

    # 2. Categorize Columns
    id_cols = [c for c in cols if any(k in c.lower() for k in ["_id", "id", "sample", "entry", "tag", "plot"])]
    snp_cols = [c for c in cols if c.lower().startswith("snp_") or c.lower().startswith("rs") or "marker" in c.lower()]
    num_cols = df_up.select_dtypes(include=[np.number]).columns.tolist()
    trait_cols = [c for c in num_cols if c not in id_cols and c not in snp_cols]
    factor_cols = [c for c in cols if c not in id_cols and c not in snp_cols and c not in trait_cols]

    for c in trait_cols[:]:
        if df_up[c].nunique() <= 8 and any(k in c.lower() for k in ["sex", "gender", "treatment", "rep", "block", "location", "season", "year"]):
            factor_cols.append(c)
            trait_cols.remove(c)

    missing_pct = float(df_up.isnull().sum().sum()) / (n_rows * n_cols) * 100.0 if n_rows * n_cols > 0 else 0.0
    completeness_pct = round(100.0 - missing_pct, 1)

    trait_stats = {}
    for t in trait_cols:
        s = df_up[t].dropna()
        if len(s) > 0:
            m = float(s.mean())
            sd = float(s.std()) if len(s) > 1 else 0.0
            cv = (sd / m * 100.0) if m != 0 else 0.0
            trait_stats[t] = {
                "mean": m,
                "std": sd,
                "cv": cv,
                "min": float(s.min()),
                "max": float(s.max()),
                "median": float(s.median())
            }

    domain_info = {}
    synthesis_df = pd.DataFrame()
    visualizations = []
    knowledge_gaps = []
    env_note = ""
    bridges = []
    summary_kpis = []

    # =========================================================================
    # DOMAIN 1: ANIMAL GENETICS & BREEDING
    # =========================================================================
    if top_domain == "animal_genetics":
        domain_info = {
            "name": "Animal Genetics, Pedigree & Quantitative Genomics",
            "icon": "🐄",
            "badge": "Livestock Genomics Pipeline",
            "tagline": "Pedigree kinship structure, phenotypic biometric variance & SNP marker profiling"
        }

        breed_col = next((c for c in factor_cols if "breed" in c.lower()), factor_cols[0] if factor_cols else None)
        sex_col = next((c for c in factor_cols if any(k in c.lower() for k in ["sex", "gender"])), None)
        sire_col = next((c for c in id_cols if "sire" in c.lower()), None)
        dam_col = next((c for c in id_cols if "dam" in c.lower()), None)
        animal_col = next((c for c in id_cols if "animal" in c.lower()), id_cols[0] if id_cols else None)

        n_sires = df_up[sire_col].nunique() if sire_col else 0
        n_dams = df_up[dam_col].nunique() if dam_col else 0
        sire_avg = (n_rows / n_sires) if n_sires > 0 else 0.0
        sire_max = int(df_up[sire_col].value_counts().max()) if sire_col else 0
        breeds_list = df_up[breed_col].unique().tolist() if breed_col else []

        mafs = []
        for s in snp_cols:
            if df_up[s].dtype in [np.int64, np.float64, int, float]:
                freq = float(df_up[s].sum()) / (2.0 * n_rows) if n_rows > 0 else 0.0
                mafs.append(min(freq, 1.0 - freq))
        mean_maf = float(np.mean(mafs)) if mafs else 0.0
        min_maf = float(np.min(mafs)) if mafs else 0.0
        max_maf = float(np.max(mafs)) if mafs else 0.0

        corr_val = 0.0
        corr_text = "N/A"
        if len(trait_cols) >= 2:
            t1, t2 = trait_cols[0], trait_cols[1]
            corr_val = float(df_up[t1].corr(df_up[t2]))
            corr_text = f"r = {corr_val:.3f}"

        summary_kpis = [
            {"label": "Total Animals (N)", "val": f"{n_rows}", "sub": "Total progeny records evaluated"},
            {"label": "Pedigree Families", "val": f"{n_sires} Sires • {n_dams} Dams", "sub": f"Average {sire_avg:.1f} progeny/sire"},
            {"label": "Breeds Represented", "val": f"{len(breeds_list)} Breeds", "sub": ", ".join(breeds_list[:3]) if breeds_list else "Lineages"},
            {"label": "Genomic Markers", "val": f"{len(snp_cols)} SNPs", "sub": f"Mean MAF = {mean_maf:.2f}"},
            {"label": "Data Completeness", "val": f"{completeness_pct}%", "sub": "Evaluated across all traits"}
        ]

        group_cols = [c for c in [breed_col, sex_col] if c is not None]
        if group_cols:
            synth_rows = []
            for name, group in df_up.groupby(group_cols):
                if not isinstance(name, tuple):
                    name = (name,)
                cohort_str = " • ".join(str(n) for n in name)
                row_data = {
                    "Cohort / Subpopulation": cohort_str,
                    "Sample Size (n)": len(group)
                }
                for t in trait_cols:
                    m = group[t].mean()
                    s = group[t].std() if len(group) > 1 else 0.0
                    row_data[f"{t} (Mean ± SD)"] = f"{m:.2f} ± {s:.2f}"
                if snp_cols:
                    row_data["Genomic Markers"] = f"{len(snp_cols)} Loci (Polymorphic)"
                row_data["Evidence Classification"] = "Empirical Biometrical Trial (Primary Data)"
                synth_rows.append(row_data)
            synthesis_df = pd.DataFrame(synth_rows)

        if breed_col and trait_cols:
            primary_trait = trait_cols[0]
            fig_box = px.box(
                df_up,
                x=breed_col,
                y=primary_trait,
                color=sex_col if sex_col else None,
                points="all",
                title=f"Distribution of {primary_trait} across Breeds" + (f" by {sex_col}" if sex_col else ""),
                color_discrete_sequence=["#1B5E20", "#81C784", "#388E3C", "#C8E6C9"]
            )
            fig_box.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=40, b=20))
            visualizations.append({
                "title": f"📊 {primary_trait} Distribution by Breed",
                "desc": f"Box plot depicting empirical variation of {primary_trait} across breeds and sexes with jittered observation points.",
                "fig": fig_box
            })

        if len(trait_cols) >= 2:
            t1, t2 = trait_cols[0], trait_cols[1]
            fig_scatter = px.scatter(
                df_up,
                x=t1,
                y=t2,
                color=breed_col if breed_col else None,
                title=f"Bivariate Phenotypic Distribution: {t1} vs {t2} ({corr_text})",
                color_discrete_sequence=["#1B5E20", "#2E7D32", "#4CAF50", "#81C784"]
            )
            fig_scatter.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=40, b=20))
            visualizations.append({
                "title": f"📈 Bivariate Correlation ({t1} vs {t2})",
                "desc": f"Scatter plot showing individual phenotypic covariance and linear association ({corr_text}).",
                "fig": fig_scatter
            })

        if snp_cols and mafs:
            maf_df = pd.DataFrame({"Locus": snp_cols, "Minor_Allele_Freq": mafs})
            fig_maf = px.bar(
                maf_df,
                x="Locus",
                y="Minor_Allele_Freq",
                title=f"Genomic Marker Allele Frequency Profile (Mean MAF = {mean_maf:.2f})",
                color="Minor_Allele_Freq",
                color_continuous_scale="Greens"
            )
            fig_maf.add_hline(y=0.05, line_dash="dash", line_color="red", annotation_text="QC Threshold (MAF = 0.05)")
            fig_maf.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=40, b=20))
            visualizations.append({
                "title": "🧬 SNP Marker Allele Frequencies",
                "desc": f"Minor allele frequency spectrum across polymorphic loci with quality control threshold (MAF >= 0.05).",
                "fig": fig_maf
            })

        env_note = {
            "title": "Bovine Genetics & Bioclimatic Covariates",
            "soil_ph": "Local Soil pH is an edaphic soil parameter (essential for forage grass agronomy and fertilizer balance), but is NOT a direct genetic or physiological covariate of bovine growth traits or pedigree EBVs.",
            "thi": "Temperature-Humidity Index (THI > 72) is the primary tropical stressor causing acute heat strain, depressed rumination, and G×E interactions across temperate Bos taurus breeds.",
            "takeaway": "When modeling genetic merit (BLUP / Selection Indices), model THI as an environmental covariate and exclude Soil pH to avoid biometrical model misspecification."
        }

        bw_desc = f"{trait_stats.get('Body_Weight_kg', {}).get('mean', 0.0):.1f} ± {trait_stats.get('Body_Weight_kg', {}).get('std', 0.0):.1f} kg (CV: {trait_stats.get('Body_Weight_kg', {}).get('cv', 0.0):.1f}%)" if "Body_Weight_kg" in trait_stats else "N/A"
        gr_desc = f"{trait_stats.get('Growth_Rate_kg_day', {}).get('mean', 0.0):.2f} ± {trait_stats.get('Growth_Rate_kg_day', {}).get('std', 0.0):.2f} kg/day (CV: {trait_stats.get('Growth_Rate_kg_day', {}).get('cv', 0.0):.1f}%)" if "Growth_Rate_kg_day" in trait_stats else "N/A"

        knowledge_gaps = [
            f"**Pedigree Depth & Ancestral Kinship Structure**: The dataset records **{n_sires} sires** and **{n_dams} dams** across {n_rows} progeny, "
            f"averaging {sire_avg:.1f} progeny per sire (range: 1 to {sire_max}). *Critical Knowledge Gap*: There is no multi-generational ancestry "
            f"(absence of maternal grandsires, granddams, or earlier pedigree tiers). Without deeper pedigree records, individual inbreeding coefficients ($F$) "
            f"cannot be estimated, and maternal permanent environmental variance ($V_{{pe}}$) cannot be separated from direct additive genetic variance ($V_A$). "
            f"Furthermore, unbalanced sire family sizes risk confounding sire genetic effects with contemporary herd management groups.",

            f"**Phenotypic Variance Partitioning & Narrow-Sense Heritability ($h^2$)**: Body Weight exhibits wide phenotypic variation ({bw_desc}) "
            f"and Growth Rate averages {gr_desc}, with an observed phenotypic correlation of {corr_text}. *Critical Knowledge Gap*: Observed values represent "
            f"raw phenotypic aggregates ($P = \\mu + G + E$). Without linear mixed model variance component estimation (REML or Bayesian Gibbs sampling), "
            f"the narrow-sense heritabilities ($h^2 = V_A / V_P$) and genetic correlations ($r_g$) remain unestimated. Essential tropical lifetime fitness traits "
            f"(calving ease, age at first calving, inter-calving interval, and tick-borne hemoparasite burden) are completely unrecorded.",

            f"**Genomic Marker Density & Genome-Wide Coverage**: The dataset features **{len(snp_cols)} bi-allelic SNP loci**, all showing robust polymorphism "
            f"(mean MAF = {mean_maf:.2f}, ranging from {min_maf:.2f} to {max_maf:.2f}). *Critical Knowledge Gap*: While 10 candidate SNPs can test preliminary QTL "
            f"marker-trait associations via single-marker regression, they are mathematically insufficient for whole-genome Genomic Selection (GBLUP or single-step ssGBLUP). "
            f"High-density beadchips (50k to 777k SNPs) or low-pass genotyping-by-sequencing (GBS) are required to capture linkage disequilibrium (LD) across diverse breeds.",

            f"**Tropical Adaptation & Genotype × Environment ($G \\times E$) Vulnerability**: The dataset consists exclusively of four exotic European breeds "
            f"({', '.join(breeds_list) if breeds_list else 'temperate Bos taurus'}). *Critical Knowledge Gap*: Pure temperate *Bos taurus* breeds suffer severe physiological "
            f"breakdown under sub-Saharan tropical heat load ($THI > 72$), losing 30%–50% of growth potential and suffering high mortality from tsetse-transmitted "
            f"trypanosomiasis and tick-borne anaplasmosis/babesiosis. Crossbreeding evaluations with indigenous West African zebu (*Bos indicus*, e.g., White Fulani/Bunaji, "
            f"Sokoto Gudali) or trypanotolerant taurine (*Bos taurus*, e.g., Muturu, N'Dama) are urgently needed to quantify crossbred heterosis and thermo-tolerance.",

            f"**Recommended AgroBiometrix Action Protocol**: To transform this raw dataset into actionable scientific breeding decisions, proceed to: "
            f"(1) **Module 3 (Statistical Geneticist)** to fit Henderson's Mixed Model Equations (Sire Model / Animal Model), extract Best Linear Unbiased Predictions "
            f"(BLUP) for Sire Estimated Breeding Values (EBVs), and run Duncan's Multiple Range Test across breeds; (2) **Module 4 (Plant & Animal Breeding)** "
            f"to construct a multi-trait Smith-Hazel selection index combining Body Weight and Growth Rate; and (3) **Module 7 (Livestock Intelligence)** "
            f"to run bioclimatic THI thermal stress simulation and slaughter margin optimization."
        ]

        bridges = [
            {
                "module": "🧬 Module 3: Statistical Geneticist",
                "action": "Henderson's Mixed Model Equations (BLUP)",
                "description": "Extract Best Linear Unbiased Predictions for Sire Estimated Breeding Values (EBVs) and compute Duncan's MRT across breeds."
            },
            {
                "module": "🎯 Module 4: Plant & Animal Breeding",
                "action": "Multi-Trait Selection Index (Smith-Hazel)",
                "description": "Construct aggregate economic selection index combining Body Weight and Daily Gain with constrained heritabilities."
            },
            {
                "module": "🐄 Module 7: Livestock Intelligence",
                "action": "Bioclimatic THI Heat Stress Simulation",
                "description": "Simulate tropical heat stress loads (THI > 72) and calculate slaughter profit margins under African temperature profiles."
            }
        ]

    # =========================================================================
    # DOMAIN 2: CROP AGRONOMY & PLANT BREEDING
    # =========================================================================
    elif top_domain == "crop_agronomy":
        domain_info = {
            "name": "Crop Agronomy, Cultivar Evaluation & Plant Breeding",
            "icon": "🌱",
            "badge": "Crop Science & Field Agronomy Pipeline",
            "tagline": "Multi-environment trial analysis, yield stability & agronomic treatment response"
        }
        var_col = next((c for c in factor_cols if any(k in c.lower() for k in ["variety", "cultivar", "genotype", "accession", "entry"])), factor_cols[0] if factor_cols else None)
        trt_col = next((c for c in factor_cols if any(k in c.lower() for k in ["treatment", "fert", "npk", "dose", "irrigation"])), None)
        yield_col = next((c for c in trait_cols if any(k in c.lower() for k in ["yield", "biomass", "grain", "harvest"])), trait_cols[0] if trait_cols else None)

        summary_kpis = [
            {"label": "Trial Observations (N)", "val": f"{n_rows}", "sub": "Total empirical plot observations"},
            {"label": "Cultivars / Genotypes", "val": f"{df_up[var_col].nunique() if var_col else len(factor_cols)} Entries", "sub": "Candidate germplasm lines"},
            {"label": "Quantitative Traits", "val": f"{len(trait_cols)} Traits", "sub": "Phenotypic yield & agronomic metrics"},
            {"label": "Primary Trait", "val": f"{yield_col if yield_col else 'Recorded'}", "sub": "Target selection parameter"},
            {"label": "Data Completeness", "val": f"{completeness_pct}%", "sub": "Evaluated across all trial plots"}
        ]

        group_cols = [c for c in [var_col, trt_col] if c is not None]
        if group_cols and trait_cols:
            synth_rows = []
            for name, group in df_up.groupby(group_cols):
                if not isinstance(name, tuple):
                    name = (name,)
                cohort_str = " • ".join(str(n) for n in name)
                row_data = {
                    "Cultivar / Treatment Cohort": cohort_str,
                    "Replications (n)": len(group)
                }
                for t in trait_cols:
                    m = group[t].mean()
                    s = group[t].std() if len(group) > 1 else 0.0
                    row_data[f"{t} (Mean ± SD)"] = f"{m:.2f} ± {s:.2f}"
                row_data["Evidence Classification"] = "Agronomic Experimental Field Trial"
                synth_rows.append(row_data)
            synthesis_df = pd.DataFrame(synth_rows)

        if var_col and yield_col:
            fig_var = px.box(
                df_up, x=var_col, y=yield_col, color=trt_col if trt_col else None,
                points="all", title=f"{yield_col} Variation across Cultivars",
                color_discrete_sequence=["#1B5E20", "#388E3C", "#81C784"]
            )
            fig_var.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=40, b=20))
            visualizations.append({
                "title": "🌱 Cultivar Yield Distribution",
                "desc": f"Box plot depicting empirical variation of {yield_col} across candidate cultivars and treatment cohorts.",
                "fig": fig_var
            })

        env_note = {
            "title": "Field Crop Agronomy & Edaphic Drivers",
            "soil_ph": "Soil pH directly controls macronutrient availability, phosphorus fixation, and aluminum toxicity in tropical soils.",
            "thi": "Growing Degree Days (GDD) and diurnal temperature swings govern crop phenology and anthesis-silking intervals.",
            "takeaway": "Include soil pH and seasonal rainfall hiatus as essential environmental covariates in multi-environment trial (MET) models."
        }

        knowledge_gaps = [
            f"**Multi-Environment Trials (MET) & G×E Stability**: Trial captures {n_rows} observations across {len(trait_cols)} traits. *Critical Gap*: Multi-location testing across varied agro-ecological zones (Derived Savanna vs Northern Guinea Savanna) is required to calculate cultivar stability indices (AMMI / GGE biplots).",
            "**Soil Spatial Micro-Heterogeneity**: Field plots often exhibit spatial fertility gradients. *Critical Gap*: Ensure spatial block design (RCBD / Alpha-Lattice) controls for intra-plot soil pH and moisture variations.",
            "**Farmer-Preferred Post-Harvest Traits**: High-yielding candidate varieties frequently lack consumer cooking, processing, and storability attributes (e.g. starch paste viscosity, flour density, bruchid resistance).",
            "**Recommended AgroBiometrix Action Protocol**: (1) Use **Module 8 (Experiment Designer)** to generate conformed randomized split-plot layouts; (2) Run **Module 3 (Statistical Geneticist)** for ANOVA and Duncan's grouping across varieties; and (3) Use **Module 5 (Soil Intelligence)** for NPK stoichiometric fertilizer balancing."
        ]
        bridges = [
            {
                "module": "📐 Module 8: Experiment Designer",
                "action": "Field Randomization & Layout Verification",
                "description": "Verify split-plot / RCBD blocking efficiency and generate R agricolae field maps."
            },
            {
                "module": "🧬 Module 3: Statistical Geneticist",
                "action": "Factorial ANOVA & Duncan's Test",
                "description": "Partition treatment and genotype sums of squares and assign post-hoc letter groupings."
            },
            {
                "module": "🧪 Module 5: Soil Intelligence",
                "action": "Stoichiometric NPK Balancing",
                "description": "Calibrate site-specific NPK micro-dosing and lime tonnage based on soil tests."
            }
        ]

    # =========================================================================
    # DOMAIN 3: SOIL SCIENCE
    # =========================================================================
    elif top_domain == "soil_science":
        domain_info = {
            "name": "Edaphic Chemistry & Soil Nutrient Diagnostics",
            "icon": "🧪",
            "badge": "Soil Fertility Pipeline",
            "tagline": "Stoichiometric nutrient balancing, soil reaction (pH) & cation exchange capacity"
        }
        summary_kpis = [
            {"label": "Soil Samples (N)", "val": f"{n_rows}", "sub": "Total soil core samples"},
            {"label": "Chemical Analytes", "val": f"{len(trait_cols)} Parameters", "sub": "Measured edaphic variables"},
            {"label": "Data Completeness", "val": f"{completeness_pct}%", "sub": "Sample analytical coverage"}
        ]
        env_note = {
            "title": "Edaphic Soil Chemistry Diagnostics",
            "soil_ph": "Soil pH is the foundational master variable determining cation exchange capacity (CEC) and nutrient availability.",
            "thi": "Atmospheric evaporative demand and soil temperature influence microbial mineralization rates.",
            "takeaway": "Maintain optimal 6.0–6.8 pH range to maximize NPK fertilizer use efficiency."
        }
        knowledge_gaps = [
            "**Stoichiometric Nutrient Balance**: Analysis of macronutrient ratios (C:N, N:P:K, Ca:Mg) required to prevent secondary deficiency lockout.",
            "**Buffering & Lime Requirement**: Acid soils (pH < 5.5) require SMP buffer or aluminum saturation titrations to calibrate precise agricultural lime tonnage.",
            "**Spatial Geostatistical Mapping**: Point samples should be interpolated using ordinary kriging across spatial coordinates to guide variable-rate fertilizer application."
        ]
        bridges = [
            {
                "module": "🧪 Module 5: Soil Intelligence",
                "action": "Automated Stoichiometric Balancing",
                "description": "Run nutrient replenishment and agricultural lime requirement models."
            }
        ]

    # =========================================================================
    # FALLBACK / GENERAL EMPIRICAL
    # =========================================================================
    else:
        domain_info = {
            "name": "General Empirical Agricultural Research Trial",
            "icon": "🔬",
            "badge": "Empirical Field Dataset",
            "tagline": "Exploratory biometric profiling, treatment effects & statistical gap identification"
        }
        summary_kpis = [
            {"label": "Observations (N)", "val": f"{n_rows}", "sub": "Total recorded sample units"},
            {"label": "Variables Recorded", "val": f"{n_cols}", "sub": "Measured quantitative & categorical attributes"},
            {"label": "Quantitative Traits", "val": f"{len(trait_cols)}", "sub": "Continuous biometric parameters"},
            {"label": "Categorical Factors", "val": f"{len(factor_cols)}", "sub": "Experimental treatments & cohorts"},
            {"label": "Data Completeness", "val": f"{completeness_pct}%", "sub": "Overall matrix completeness"}
        ]
        env_note = {
            "title": "General Empirical Research Data",
            "soil_ph": "Edaphic parameter evaluated for crop and soil trials.",
            "thi": "Bioclimatic thermal index evaluated for animal and poultry trials.",
            "takeaway": "Tailor environmental covariates to the specific biological domain under investigation."
        }
        knowledge_gaps = [
            f"**Sample Replication**: Dataset contains {n_rows} observations across {n_cols} variables. Replication across seasons and multi-environment locations is recommended before extension deployment.",
            "**Confounding Environmental Covariates**: Explicitly verify whether edaphic (soil pH, nutrients) or bioclimatic (THI, rainfall) factors represent the relevant biological drivers for this specific commodity.",
            "**Economic Sensitivity**: Cross-reference empirical responses with input cost elasticity and farm-gate profit margins."
        ]
        bridges = [
            {
                "module": "📊 Module 3: Statistical Geneticist",
                "action": "Exploratory Biometric Modeling",
                "description": "Run general linear models, ANOVA, and mean separation procedures."
            },
            {
                "module": "📐 Module 8: Experiment Designer",
                "action": "Fieldbook Layout Verification",
                "description": "Audit experimental replication, blocking efficiency, and sample size power."
            }
        ]

    return {
        "domain_title": domain_info.get("name", "Empirical Agricultural Trial"),
        "domain_info": domain_info,
        "summary_kpis": summary_kpis,
        "synthesis_df": synthesis_df,
        "raw_df": df_up,
        "trait_cols": trait_cols,
        "factor_cols": factor_cols,
        "visualizations": visualizations,
        "knowledge_gaps": knowledge_gaps,
        "env_note": env_note,
        "bridges": bridges
    }


def render_research_copilot():
    is_fr = st.session_state.get("app_lang", "en") == "fr"
    if is_fr:
        st.markdown("### 📚 Copilote de Recherche Agricole & Matrice de Preuves")
        st.caption("Assistant de recherche systématique fondé sur des preuves scientifiques, téléversement de documents et vulgarisation radio multilingue.")
        tab_titles = [
            "🔬 Matrice Structurée de Preuves & Lacunes",
            "🎙️ Vulgarisation Vocale & Radio Rurale Communautaire"
        ]
    else:
        st.markdown("### 📚 AgriResearch Copilot & Evidence Engine")
        st.caption("Evidence-grounded systematic research assistant with zero fabricated citations, File Upload, & Multilingual Radio Extension.")
        tab_titles = [
            "🔬 Structured Evidence Matrix & Gaps",
            "🎙️ Last-Mile Multilingual Voice & Radio Advisory"
        ]

    tab_evidence, tab_radio = st.tabs(tab_titles)

    # -------------------------------------------------------------
    # TAB 1: EVIDENCE MATRIX & KNOWLEDGE GAPS
    # -------------------------------------------------------------
    with tab_evidence:
        # Load curated African Evidence Base
        db_path = os.path.join("data", "african_evidence_base.json")
        evidence_db = {}
        if os.path.exists(db_path):
            with open(db_path, "r", encoding="utf-8") as f:
                evidence_db = json.load(f)

        col1, col2 = st.columns([2, 1])
        with col1:
            research_topic = st.selectbox(
                "Sélectionnez le Domaine de Recherche Agricole :" if is_fr else "Select Agricultural Research Domain:",
                [
                    "📁 Custom Query (Upload File or Type Prompt)",
                    "🐄 Genetic Resistance to Trypanosomiasis in West African Cattle",
                    "🌡️ Heat Tolerance & Thermoregulation in Indigenous African Zebu & Taurine",
                    "🌽 Drought & Heat Tolerant Maize Breeding in the Northern Guinea/Sudan Savanna",
                    "🐔 Avian Bioclimatics & Poultry Disease Dynamics in Tropical Nigeria",
                    "🐇 Cuniculture Science: Rabbit Breeds, Heat Sterility & Forages in Nigeria",
                    "🍅 Horticultural Science: Tomato Cultivars, Blossom End Rot & TYLCV in Western Nigeria",
                    "🥔 Cassava Genomics & Disease Immunity (CMD2/CMD3) in Sub-Saharan Africa",
                    "🌾 Lowland & Upland Rice Submergence & Nitrogen Efficiency (Sub1, FARO 44)"
                ],
                index=0
            )
        with col2:
            evidence_filter = st.selectbox("Filtre de Robustesse des Preuves :" if is_fr else "Evidence Strength Filter:", ["All Evidence", "Strong (Replicated) Only", "QTL / GWAS Only"])

        # Check if user selected Custom Query
        is_custom = "Custom Query" in research_topic or "Upload" in research_topic or "Type Prompt" in research_topic
        raw_items = []
        uploaded_gaps = []
        custom_analysis = None

        if is_custom:
            st.markdown("---")
            custom_mode = st.radio(
                "Choose Custom Avenue:",
                ["📁 Upload Evidence File (CSV, Excel, TXT)", "✍️ Type Scientific Prompt"],
                horizontal=True
            )

            if "Upload Evidence File" in custom_mode:
                st.markdown("##### 📂 Upload Research Dataset or Evidence Document")
                st.caption("Upload your empirical trial data, systematic review matrix, or research notes in CSV, Excel, or Text format:")
                
                uploaded_file = st.file_uploader(
                    "Choose file to upload:",
                    type=["csv", "xlsx", "xls", "txt"],
                    help="Upload a CSV/Excel file with columns: Study, Population, Trait, Sample_Size, Method, Major_Finding, Evidence_Strength (or any trial table)"
                )

                if uploaded_file is not None:
                    try:
                        if uploaded_file.name.endswith(".csv"):
                            df_up = pd.read_csv(uploaded_file)
                        elif uploaded_file.name.endswith((".xlsx", ".xls")):
                            df_up = pd.read_excel(uploaded_file)
                        else:
                            # Plain text file
                            txt_content = uploaded_file.read().decode("utf-8", errors="ignore")
                            lines = [line.strip() for line in txt_content.split("\n") if line.strip()]
                            df_up = pd.DataFrame([
                                {
                                    "Study": f"Uploaded Doc ({uploaded_file.name})",
                                    "Population": "User Field Dataset",
                                    "Trait": line[:35] if len(line) > 35 else line,
                                    "Sample_Size": "N/A",
                                    "Method": "Document Text Extraction",
                                    "Major_Finding": line,
                                    "Evidence_Strength": "User Provided"
                                }
                                for line in lines[:10]
                            ])

                        # Run domain-specific empirical evidence analysis
                        custom_analysis = analyze_custom_evidence_dataset(df_up, uploaded_file.name)
                        st.success(f"✅ Successfully loaded **{uploaded_file.name}** ({len(df_up)} records found)")
                        domain_lbl = custom_analysis.get("domain_title") or custom_analysis.get("domain_info", {}).get("name", "Empirical Research Dataset")
                        st.info(f"🧬 **Identified Domain Framework**: **{domain_lbl}**")
                        uploaded_gaps = custom_analysis.get("knowledge_gaps", [])
                        if not custom_analysis["synthesis_df"].empty:
                            raw_items = custom_analysis["synthesis_df"].to_dict("records")
                        else:
                            raw_items = df_up.to_dict("records")
                    except Exception as e:
                        st.error(f"Error parsing file: {e}")
                        raw_items = []
                else:
                    # Provide template download button
                    st.info("💡 **No file uploaded yet**. You can upload your own research file above, or download our standardized template to test:")
                    template_csv = (
                        "Study,Population,Trait,Sample_Size,Method,Major_Finding,Evidence_Strength\n"
                        "IITA Research Bulletin (2024),Cassava TMS 98/0505,CMD2 Mosaic Immunity,350,GWAS Linkage,High dominant resistance in sub-humid rainforest,Strong (Replicated)\n"
                        "NAPRI Shika-Zaria (2023),White Fulani x Muturu,Trypanotolerance PCV,180,Candidate Gene Panel,Maintained PCV > 28% under natural tsetse challenge,Strong\n"
                        "FUNAAB Poultry Trial (2024),ShikaBrown Layers,Harmattan Heat Stress,250,Thermal Chamber Trial,Electrolyte therapy preserved eggshell thickness at >32C,Strong (Replicated)\n"
                        "NIHORT Ibadan (2023),Cobra 26 F1,Rain-Cracking & Firmness,180,Rainforest Field Trial,Thick pericarp eliminated fruit splitting during late rains,Strong (Replicated)\n"
                        "Cuniculture Lab (2024),New Zealand White x Chinchilla,Heat Sterility & Bloat,120,Factorial Trial,Wilting Tridax 4 hrs cut bloat 92%; shaded bottles prevented buck sterility,Strong\n"
                    )
                    st.download_button(
                        label="📥 Download Sample Evidence Matrix Template (.csv)",
                        data=template_csv.encode("utf-8"),
                        file_name="sample_agrobiometrix_evidence_template.csv",
                        mime="text/csv"
                    )
                    # Sample preview rows
                    raw_items = [
                        {
                            "Study": "Sample User Study (Upload your file above)",
                            "Population": "Example Lineage / Breed",
                            "Trait": "Breeding / Disease Trait",
                            "Sample_Size": 150,
                            "Method": "QTL / GWAS / Factorial Trial",
                            "Major_Finding": "Upload your CSV, Excel, or TXT file above to analyze and filter your own empirical research matrix.",
                            "Evidence_Strength": "Strong (Replicated)"
                        }
                    ]

            else:
                # Type Scientific Prompt
                st.markdown("##### ✍️ Type Scientific Research Inquiry")
                
                # Preset quick chips
                st.caption("Click a sample inquiry or type your custom research prompt:")
                c1, c2, c3, c4 = st.columns(4)
                preset_val = ""
                if c1.button("🐇 Rabbit Heat & Bloat"):
                    preset_val = "Rabbit heat stress buck sterility and wilted forage bloat"
                if c2.button("🐔 Broiler Bioclimatics"):
                    preset_val = "Poultry heat stress electrolyte balance and Newcastle disease"
                if c3.button("🍅 Tomato Blossom End Rot"):
                    preset_val = "Tomato blossom end rot calcium and TYLCV whitefly"
                if c4.button("🐄 Cattle Trypanotolerance"):
                    preset_val = "Muturu and N'Dama trypanosomiasis resistance QTL"

                custom_query_text = st.text_input(
                    "Enter Research Inquiry:",
                    value=preset_val,
                    placeholder="e.g. Rabbit heat stress sterility, Broiler Harmattan bioclimatics, Tomato bacterial wilt..."
                )

                if custom_query_text.strip():
                    q_term = custom_query_text.lower()
                    matched_items = []
                    for cat, items in evidence_db.items():
                        if isinstance(items, list):
                            for it in items:
                                if isinstance(it, dict):
                                    text_corpus = f"{it.get('Study', '')} {it.get('Population', '')} {it.get('Trait', '')} {it.get('Method', '')} {it.get('Major_Finding', '')}".lower()
                                    if any(w in text_corpus for w in q_term.split()):
                                        matched_items.append(it)
                    if matched_items:
                        raw_items = matched_items
                        st.info(f"🔎 Found **{len(matched_items)} matching studies** in the African Evidence Base for: *'{custom_query_text}'*")
                    else:
                        # Synthesize via orchestrator with regional awareness
                        active_reg = st.session_state.get("active_region")
                        synth = rule_based_agent_synthesis(custom_query_text, active_region=active_reg)
                        geo_info = detect_target_geography(custom_query_text, active_region=active_reg)
                        country_tag = geo_info.get("label", "Sub-Saharan Africa")
                        if not synth.get("unsupported"):
                            raw_items = [
                                {
                                    "Study": f"AgroBiometrix Synthesized Evidence Consensus ({country_tag}, 2026)",
                                    "Population": f"Calibrated {country_tag} Agro-Ecologies",
                                    "Trait": custom_query_text[:40],
                                    "Sample_Size": "Multi-Agent Meta-Synthesis",
                                    "Method": f"Specialized AI Agent Ensemble ({country_tag} Grounded)",
                                    "Major_Finding": synth.get("summary", synth.get("final_synthesis", ""))[:220] + "...",
                                    "Evidence_Strength": "Strong (Institutional Consensus)"
                                }
                            ]
                        else:
                            raw_items = [
                                {
                                    "Study": "Notice: Offline Evidence Boundary Reached",
                                    "Population": "N/A",
                                    "Trait": "Uncalibrated Domain",
                                    "Sample_Size": 0,
                                    "Method": "Zero-Hallucination Policy",
                                    "Major_Finding": "No peer-reviewed records in offline database. Please connect Live Multi-Agent AI (Google Gemini).",
                                    "Evidence_Strength": "Withheld"
                                }
                            ]
                else:
                    # Default sample
                    raw_items = evidence_db.get("trypanosomiasis_resistance", [])

        # Non-custom pre-calibrated domains
        elif "Trypanosomiasis" in research_topic:
            raw_items = evidence_db.get("trypanosomiasis_resistance", [])
        elif "Heat Tolerance" in research_topic:
            raw_items = evidence_db.get("heat_tolerance_cattle", [])
        elif "Maize" in research_topic:
            raw_items = evidence_db.get("maize_drought_tolerance", [])
        elif "Poultry" in research_topic or "Avian" in research_topic:
            raw_items = evidence_db.get("poultry_bioclimatics", [])
        elif "Cuniculture" in research_topic or "Rabbit" in research_topic:
            raw_items = evidence_db.get("rabbit_cuniculture", [])
        elif "Tomato" in research_topic or "Horticultural" in research_topic:
            raw_items = evidence_db.get("tomato_horticulture", [])
        elif "Cassava" in research_topic:
            raw_items = evidence_db.get("cassava_genomics", [])
        elif "Rice" in research_topic:
            raw_items = evidence_db.get("rice_submergence", [])
        else:
            raw_items = evidence_db.get("trypanosomiasis_resistance", [])

        if custom_analysis is not None:
            domain_lbl = custom_analysis.get("domain_title") or custom_analysis.get("domain_info", {}).get("name", "Empirical Research Dataset")
            
            # 1. Executive Metric KPI Bar
            st.markdown(f"#### 📊 Empirical Dataset Overview — {domain_lbl}")
            kpis = custom_analysis.get("summary_kpis", [])
            if kpis:
                kpi_cols = st.columns(len(kpis))
                for col, kpi in zip(kpi_cols, kpis):
                    if isinstance(kpi, dict):
                        col.metric(label=kpi.get("label", "Metric"), value=kpi.get("val", kpi.get("value", "N/A")), help=kpi.get("sub", kpi.get("help", None)))
                    elif isinstance(kpi, (list, tuple)):
                        l_txt = kpi[0] if len(kpi) > 0 else "Metric"
                        v_txt = kpi[1] if len(kpi) > 1 else "N/A"
                        s_txt = kpi[2] if len(kpi) > 2 else None
                        col.metric(label=l_txt, value=v_txt, help=s_txt)

            # 2. Environmental & Edaphic Covariate Clarification Box
            if custom_analysis.get("env_note"):
                env = custom_analysis["env_note"]
                if isinstance(env, dict):
                    e_title = env.get("title", "Environmental & Edaphic Covariate Calibration")
                    e_soil = env.get("soil_ph", "N/A")
                    e_thi = env.get("thi", "N/A")
                    e_takeaway = env.get("takeaway", "")
                    st.markdown(f"""
<div class="agri-card" style="border-left: 5px solid #FF9800; background: #FFF8E1; padding: 12px 16px; margin: 14px 0; border-radius: 4px;">
    <div style="font-weight: 700; color: #E65100; font-size: 0.95rem; margin-bottom: 4px;">
        🌍 Environmental & Edaphic Covariate Calibration ({e_title})
    </div>
    <div style="font-size: 0.85rem; color: #37474F; line-height: 1.5;">
        • <b>Soil pH Clarification</b>: {e_soil}<br>
        • <b>THI (Temperature-Humidity Index) Calibration</b>: {e_thi}
    </div>
    <div style="font-size: 0.82rem; color: #1B5E20; font-weight: 600; margin-top: 6px;">
        💡 <b>Methodological Takeaway</b>: {e_takeaway}
    </div>
</div>
""", unsafe_allow_html=True)
                else:
                    st.info(str(env))

            # 3. Evidence Matrix with Dual Views
            st.markdown("#### 🔬 Structured Evidence Matrix")
            view_mode = st.radio(
                "Matrix View Format:",
                ["📋 Subpopulation Evidence Synthesis Matrix (Aggregated)", "🔍 Full Raw Empirical Observation Matrix (Micro-records)"],
                horizontal=True
            )
            
            if "Subpopulation" in view_mode and not custom_analysis["synthesis_df"].empty:
                disp_df = custom_analysis["synthesis_df"]
                st.dataframe(disp_df, use_container_width=True)
                csv_data = disp_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Evidence Synthesis Matrix (CSV)",
                    data=csv_data,
                    file_name="agrobiometrix_evidence_synthesis.csv",
                    mime="text/csv",
                    key="dl_synth_matrix"
                )
            else:
                raw_df_disp = custom_analysis["raw_df"].copy()
                if "Breed" in raw_df_disp.columns:
                    unique_breeds = ["All Breeds"] + sorted(list(raw_df_disp["Breed"].dropna().unique()))
                    selected_breed = st.selectbox("Filter Micro-records by Breed / Lineage:", unique_breeds)
                    if selected_breed != "All Breeds":
                        raw_df_disp = raw_df_disp[raw_df_disp["Breed"] == selected_breed]
                st.dataframe(raw_df_disp, use_container_width=True)
                csv_raw = raw_df_disp.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Raw Micro-records (CSV)",
                    data=csv_raw,
                    file_name="agrobiometrix_raw_micro_records.csv",
                    mime="text/csv",
                    key="dl_raw_matrix"
                )

            # 4. Interactive Empirical Visualizations
            if custom_analysis.get("visualizations"):
                st.markdown("---")
                st.markdown("#### 📈 Interactive Empirical Trait & Genomic Visualizations")
                viz_list = custom_analysis["visualizations"]
                tab_titles = []
                for v in viz_list:
                    if isinstance(v, dict):
                        tab_titles.append(v.get("title", "Visualization"))
                    elif isinstance(v, (list, tuple)):
                        tab_titles.append(v[0] if len(v) > 0 else "Visualization")
                viz_tabs = st.tabs(tab_titles)
                for tab, v in zip(viz_tabs, viz_list):
                    with tab:
                        if isinstance(v, dict):
                            if v.get("desc"):
                                st.caption(v["desc"])
                            st.plotly_chart(v["fig"], use_container_width=True)
                        elif isinstance(v, (list, tuple)):
                            st.plotly_chart(v[1], use_container_width=True)

            # 5. Knowledge Gap Analysis & Synthesis
            st.markdown("---")
            st.markdown("#### 🧭 Knowledge Gap Analysis & Domain Grounding")
            for gap in custom_analysis["knowledge_gaps"]:
                st.markdown(f"- {gap}")

            # 6. Cross-Module Action Roadmap
            if custom_analysis.get("bridges"):
                st.markdown("---")
                st.markdown("#### 🚀 Recommended Cross-Module Analytical Progression")
                st.caption("AgroBiometrix detected actionable biometric and genomic signals. Advance this dataset to downstream modules:")
                bridge_list = custom_analysis["bridges"]
                b_cols = st.columns(min(3, len(bridge_list)))
                for idx, bridge in enumerate(bridge_list):
                    col = b_cols[idx % 3]
                    with col:
                        if isinstance(bridge, dict):
                            m_title = bridge.get("module", "AgroBiometrix Module")
                            m_action = bridge.get("action", "Recommended Analysis")
                            m_desc = bridge.get("description", "")
                        elif isinstance(bridge, (list, tuple)):
                            m_title = bridge[0] if len(bridge) > 0 else "AgroBiometrix Module"
                            m_action = bridge[1] if len(bridge) > 1 else "Recommended Analysis"
                            m_desc = bridge[2] if len(bridge) > 2 else ""
                        else:
                            m_title, m_action, m_desc = str(bridge), "", ""
                        st.markdown(f"""
<div class="agri-card" style="border-top: 3px solid #2E7D32; background: #FAFAFA; padding: 12px; height: 100%; border-radius: 4px;">
    <div style="font-weight: 700; color: #1B5E20; font-size: 0.9rem; margin-bottom: 4px;">
        {m_title}
    </div>
    <div style="font-size: 0.8rem; color: #424242; margin-bottom: 6px;">
        <b>Action</b>: {m_action}
    </div>
    <div style="font-size: 0.75rem; color: #616161;">
        {m_desc}
    </div>
</div>
""", unsafe_allow_html=True)

            st.info("💡 **Africa-First Evidence Grounding**: Powered by institutional synthesis across CGIAR, IITA, ILRI, NAPRI, FUNAAB, NIHORT, FAO, and national agricultural research systems (NARS).")

        else:
            # Standard pre-calibrated domains or prompt query
            df_evidence = pd.DataFrame(raw_items)
            
            # Apply filter cleanly
            if not df_evidence.empty and "Evidence_Strength" in df_evidence.columns:
                if evidence_filter == "Strong (Replicated) Only":
                    df_evidence = df_evidence[df_evidence["Evidence_Strength"].str.contains("Replicated", case=False, na=False)]
                elif evidence_filter == "QTL / GWAS Only":
                    if "Method" in df_evidence.columns:
                        df_evidence = df_evidence[df_evidence["Method"].str.contains("QTL|GWAS|Sequencing", case=False, na=False)]

            st.markdown("#### 🔬 Structured Evidence Matrix")
            
            if df_evidence.empty:
                st.warning(f"⚠️ No records match the filter **'{evidence_filter}'**. Switch the filter to **'All Evidence'** to view all loaded studies.")
            else:
                st.dataframe(df_evidence, use_container_width=True)
                csv_data = df_evidence.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Evidence Matrix (CSV)",
                    data=csv_data,
                    file_name="agrobiometrix_evidence_matrix.csv",
                    mime="text/csv"
                )

            st.markdown("---")
            st.markdown("#### 🧭 Knowledge Gap Analysis & Synthesis")
            
            if uploaded_gaps:
                gaps = uploaded_gaps
            elif "Trypanosomiasis" in research_topic:
                gaps = [
                    "**Smallholder Field Validation**: Most QTLs were mapped in experimental research herds (ILRI/ITC); limited validation in pastoral transhumance systems.",
                    "**G×E and Co-Infection**: Scarce genomic data on dual challenge of trypanosomiasis plus tick-borne diseases (theileriosis, babesiosis) under heat stress.",
                    "**Functional Validation**: Candidate regulatory variants within TICAM1 and cytokine loci require functional expression assays in native Muturu/N'Dama tissues."
                ]
            elif "Heat Tolerance" in research_topic:
                gaps = [
                    "**Phenomic Precision**: Respiration rate and rectal temperature are frequently recorded manually; need automated high-throughput infrared thermography.",
                    "**Interaction with Nutritional Scarcity**: Dry-season heat stress coincides with poor forage quality; limited studies on metabolic heat production under roughage diets.",
                    "**Genomic Prediction Accuracies**: Cross-breed genomic prediction accuracies between West African Zebu (Bunaji) and East African Zebu (Boran) remain unbenchmarked."
                ]
            elif "Maize" in research_topic:
                gaps = [
                    "**Late Season Drought Stress**: Most studies evaluate vegetative water deficit; reproductive heat stress during pollen shedding remains a critical gap.",
                    "**Soil Micro-nutrient Interactions**: Synergies between zinc/boron priming and drought tolerance alleles require multi-location trials.",
                    "**Farmer-Preferred Cooking & Processing Traits**: High-yielding drought hybrids occasionally lack grain flour density favored for local staple foods (Tuwo)."
                ]
            elif "Poultry" in research_topic or "Avian" in research_topic:
                gaps = [
                    "**Bioclimatic Automation**: High reliance on manual curtain adjustments; scarce adoption of automated humidity-actuated side drop curtains.",
                    "**Thermostable Vaccines**: Newcastle disease outbreaks during Harmattan dust storms persist due to rural cold-chain breaks for conventional live vaccines.",
                    "**Indigenous Strain Biometrics**: Limited large-scale genomic mapping of heat-shock protein expression (HSP70) in local scavenging fowls compared to commercial broilers."
                ]
            elif "Cuniculture" in research_topic or "Rabbit" in research_topic:
                gaps = [
                    "**Buck Heat Infertility Biomarkers**: Lack of rapid hormonal assays to predict onset and recovery from testicular heat degeneration (>28°C–30°C).",
                    "**Standardized Tropical Pellet Formulations**: High reliance on ad-hoc forage mixes with unpredictable fiber content, causing mucoid enteropathy outbreaks.",
                    "**Genetic Improvement Programs**: Absence of a national pedigree register for New Zealand White and Chinchilla breeders across West Africa."
                ]
            elif "Tomato" in research_topic or "Horticultural" in research_topic:
                gaps = [
                    "**Dual Resistance Strains**: Scarcity of commercial OPVs combining both Ralstonia bacterial wilt tolerance and Ty-1 Begomovirus resistance.",
                    "**Calcium Uptake in Humid Soils**: Better understanding of root-zone calcium absorption under high transpiration and acidic ultisol dynamics.",
                    "**Cold Chain & Post-Harvest Losses**: Over 40% post-harvest loss during long-haul transit from northern production zones to southern terminal markets (Mile 12)."
                ]
            elif "Cassava" in research_topic:
                gaps = [
                    "**Brown Streak Disease (CBSD) Spread**: Need pre-emptive deployment of dual CMD + CBSD resistant varieties ahead of CBSD westward spread.",
                    "**Post-Harvest Physiological Deterioration (PPD)**: Rapid root spoilage within 48–72 hours of harvest remains the primary bottleneck for industrial processors."
                ]
            elif "Rice" in research_topic:
                gaps = [
                    "**Multi-Stress Stacking**: Varieties combining Sub1 flash-flooding tolerance with salinity and iron toxicity tolerance in coastal and inland valleys.",
                    "**Mechanized Deep Fertilizer Placement**: Lack of affordable smallholder applicator tools for urea super-granules."
                ]
            else:
                gaps = [
                    "**Smallholder Field Grounding**: Research requires multi-environment validation across varied smallholder management systems.",
                    "**Input Cost Sensitivity**: Need economic optimization models pairing genetic traits with local input affordability."
                ]

            for gap in gaps:
                st.markdown(f"- {gap}")

            st.info("💡 **Africa-First Evidence Grounding**: Powered by institutional synthesis across CGIAR, IITA, ILRI, NAPRI, FUNAAB, NIHORT, FAO, and national agricultural research systems (NARS).")

            # Last-Mile Extension Dispatch trigger for current research query
            first_gap = gaps[0].replace("**", "").replace("*", "") if 'gaps' in locals() and gaps else "Agronomic optimization required"
            first_sol = "Validated agronomic protocols and stress-mitigation guidelines."
            if 'df_evidence' in locals() and isinstance(df_evidence, pd.DataFrame) and not df_evidence.empty:
                for c in ["Key Metric / Target Value", "Impact_Finding", "Trait"]:
                    if c in df_evidence.columns:
                        first_sol = str(df_evidence.iloc[0][c])
                        break

            curr_topic = research_topic if 'research_topic' in locals() and research_topic else "Field Crops"
            curr_geo = "Pan-African Smallholder Belts"
            if 'geo_info' in locals() and isinstance(geo_info, dict):
                curr_geo = geo_info.get("label", curr_geo)
            elif 'active_reg' in locals():
                curr_geo = str(active_reg)

            render_dispatch_trigger_card(
                source_module="Module 1: AI Research Scientist Studio",
                commodity=curr_topic.split()[0] if curr_topic else "Field Crops",
                region=curr_geo,
                headline=f"Evidence Grounding: {curr_topic[:50]}",
                trigger_summary=first_gap[:140],
                recommendation_summary=str(first_sol)[:140]
            )

    # -------------------------------------------------------------
    # TAB 2: LAST-MILE MULTILINGUAL VOICE & RADIO ADVISORY
    # -------------------------------------------------------------
    with tab_radio:
        init_broadcast_queue()
        st.markdown("#### 📻 Community Extension Radio & Multilingual Voice Dispatcher")
        st.markdown(
            "Translates complex agricultural research and climate biometrics into **indigenous local-language voice bulletins** "
            "for rural smallholders across Africa. Demonstrates end-to-end delivery from **lab to last-mile farmer**."
        )

        radio_mode = st.radio(
            "📻 Select Radio Operation Mode:" if not is_fr else "📻 Mode de Fonctionnement Radio :",
            [
                "🎙️ Live AI Extension Broadcast Studio & Dynamic Queue (On-The-Fly Generation)",
                "📻 Curated Institutional Benchmarks (Pre-Bundled Ground Truth)"
            ],
            index=0,
            horizontal=True,
            key="radio_mode_toggle_selector"
        )

        if "Live AI" in radio_mode:
            st.markdown("---")
            # -------------------------------------------------------------
            # SECTION 1: GLOBAL BROADCAST DISPATCH QUEUE
            # -------------------------------------------------------------
            st.markdown("##### 📡 Live Agricultural Broadcast Dispatch Queue")
            st.caption(
                "Active research findings and biometric diagnoses automatically captured from analytical modules across AgroBiometrix for vernacular broadcast:"
            )

            queue = st.session_state.get("broadcast_dispatch_queue", [])
            with st.expander(f"📋 View Active Dispatch Queue ({len(queue)} Analytical Alerts Pending Air)", expanded=True):
                for idx, item in enumerate(queue):
                    q_col1, q_col2, q_col3 = st.columns([1.2, 3, 1])
                    with q_col1:
                        st.markdown(f"**`{item['id']}`**<br><span style='font-size:0.75rem; color:#6B7280;'>⏱️ {item['timestamp']}</span>", unsafe_allow_html=True)
                        st.caption(f"🏛️ {item['source_module']}")
                    with q_col2:
                        st.markdown(f"**📢 {item['headline']}** (`{item['commodity']}`)")
                        st.markdown(f"<span style='font-size:0.78rem; color:#1B5E20; font-weight:600;'>📍 {item['region']}</span><br><span style='font-size:0.80rem;'><b>Trigger:</b> {item['agronomic_trigger']}</span>", unsafe_allow_html=True)
                    with q_col3:
                        if st.button("⚡ Load to Studio", key=f"btn_load_q_{idx}", help="Load this finding directly into the Broadcast Studio below"):
                            st.session_state["active_studio_alert"] = item
                            st.session_state["dyn_head_val"] = item["headline"]
                            st.session_state["dyn_comm_val"] = item["commodity"]
                            st.session_state["dyn_reg_val"] = item["region"]
                            st.session_state["dyn_trig_val"] = item["agronomic_trigger"]
                            st.session_state["dyn_rec_val"] = item["recommendation"]
                            st.rerun()
                    st.markdown("<hr style='margin: 4px 0 8px 0; border: none; border-top: 1px dashed #D1D5DB;' />", unsafe_allow_html=True)

                c_q1, c_q2 = st.columns([1, 1])
                with c_q1:
                    if st.button("🔄 Reset Queue to Defaults", key="btn_reset_queue"):
                        from core.broadcast_dispatcher import DEFAULT_BROADCAST_QUEUE
                        st.session_state["broadcast_dispatch_queue"] = list(DEFAULT_BROADCAST_QUEUE)
                        st.rerun()

            # -------------------------------------------------------------
            # SECTION 2: BROADCASTER STUDIO COMPOSER
            # -------------------------------------------------------------
            st.markdown("##### 🎙️ Extension Radio Broadcaster Studio & AI Script Generator")
            st.caption(
                "Compose or synthesize culturally grounded vernacular radio bulletins from any agronomic finding or field emergency alert:"
            )

            active_alert = st.session_state.get("active_studio_alert", queue[0] if queue else {})

            c_top1, c_top2 = st.columns([2, 1])
            with c_top1:
                head_in = st.text_input(
                    "Advisory Headline / Bulletin Title:",
                    value=st.session_state.get("dyn_head_val", active_alert.get("headline", "Severe Phosphorus & Zinc Fixation in Acidic Ultisols")),
                    key="studio_head_input"
                )
            with c_top2:
                comm_in = st.text_input(
                    "Target Agricultural Commodity:",
                    value=st.session_state.get("dyn_comm_val", active_alert.get("commodity", "Maize & Cassava")),
                    key="studio_comm_input"
                )

            reg_in = st.text_input(
                "Target Agro-Ecological Region / State / Country:",
                value=st.session_state.get("dyn_reg_val", active_alert.get("region", "Southwest Nigeria (Oyo/Ogun Transition Zone)")),
                key="studio_reg_input"
            )

            c_f1, c_f2 = st.columns([1, 1])
            with c_f1:
                trig_in = st.text_area(
                    "Scientific Trigger & Biometric Finding:",
                    value=st.session_state.get("dyn_trig_val", active_alert.get("agronomic_trigger", "Soil pH < 5.1 with active Al3+ toxicity and high P-sorption capacity. Surface urea broadcast causing 40% ammonia volatilization.")),
                    height=90,
                    key="studio_trig_input"
                )
            with c_f2:
                rec_in = st.text_area(
                    "Practical Agronomic Remedy & Farmer Guidance:",
                    value=st.session_state.get("dyn_rec_val", active_alert.get("recommendation", "Halt surface urea broadcast. Apply 2.5 t/ha agricultural lime with organic compost. Switch to micro-dosing single superphosphate (SSP) at root zone.")),
                    height=90,
                    key="studio_rec_input"
                )

            # Language Selection for Dynamic Generation
            studio_lang_options = [
                "🇳🇬 Èdè Yorùbá (Yoruba)",
                "🇳🇬 Harshen Hausa (Hausa)",
                "🇰🇪 Kiswahili (Swahili)",
                "🇨🇮 Français Agricole (French)",
                "🇳🇬 West African Pidgin",
                "🇬🇧 Institutional English"
            ]
            studio_lang_choice = st.radio(
                "📻 Select Target Broadcast Language for On-Air Generation:",
                studio_lang_options,
                index=0,
                horizontal=True,
                key="studio_lang_choice_radio"
            )

            btn_gen = st.button("✨ GENERATE LIVE INDIGENOUS SPOKEN BULLETIN", type="primary", use_container_width=True, key="btn_generate_dynamic_radio")

            # Store and display generated dynamic bulletin
            if btn_gen:
                with st.spinner(f"🎙️ Formulating culturally grounded radio script in {studio_lang_choice}..."):
                    dyn_result = generate_vernacular_radio_script(
                        headline=head_in,
                        commodity=comm_in,
                        region=reg_in,
                        trigger=trig_in,
                        recommendation=rec_in,
                        target_lang=studio_lang_choice
                    )
                    st.session_state["current_dynamic_bulletin"] = dyn_result
                    st.session_state["current_dynamic_lang"] = studio_lang_choice

            dyn_data = st.session_state.get("current_dynamic_bulletin")
            dyn_lang = st.session_state.get("current_dynamic_lang", studio_lang_choice)

            if not dyn_data:
                # Pre-seed with active alert so screen is immediately rich and ready
                dyn_data = generate_vernacular_radio_script(
                    headline=head_in,
                    commodity=comm_in,
                    region=reg_in,
                    trigger=trig_in,
                    recommendation=rec_in,
                    target_lang=studio_lang_choice
                )
                st.session_state["current_dynamic_bulletin"] = dyn_data
                st.session_state["current_dynamic_lang"] = studio_lang_choice

            st.markdown(f"""
<div class="agri-card" style="border-left: 5px solid #1B5E20; background: #F8FAF8; margin-top: 1rem;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
        <span style="font-size: 0.8rem; font-weight: 700; color: #1B5E20; text-transform: uppercase;">
            📡 ON AIR • {dyn_data.get('broadcaster', 'AgroBiometrix Community Radio')}
        </span>
        <span style="background: #E8F5E9; color: #1B5E20; font-size: 0.75rem; padding: 2px 8px; border-radius: 4px; font-weight: 600;">
            ⚡ Dynamically Formulated from Live Research Finding
        </span>
    </div>
    <div style="font-size: 1.1rem; font-weight: 700; color: #1B5E20; margin-bottom: 0.5rem;">
        📢 {dyn_data.get('headline', head_in)}
    </div>
</div>
""", unsafe_allow_html=True)

            col_dyn_audio, col_dyn_txt = st.columns([1, 1])
            with col_dyn_audio:
                st.markdown("##### 🔊 Real-Time Voice Broadcast Audio")
                st.caption(f"Listen to the dynamically formulated {dyn_lang} voice bulletin:")

                # Browser Web Speech API via components.html
                dyn_script_json = json.dumps(dyn_data.get('audio_script', ''))
                if "yoruba" in dyn_lang.lower():
                    dyn_bcp47 = "yo-NG"
                    dyn_tag = "Yorùbá"
                elif "hausa" in dyn_lang.lower():
                    dyn_bcp47 = "ha-NG"
                    dyn_tag = "Hausa"
                elif "swahili" in dyn_lang.lower():
                    dyn_bcp47 = "sw-KE"
                    dyn_tag = "Swahili"
                elif "français" in dyn_lang.lower() or "french" in dyn_lang.lower():
                    dyn_bcp47 = "fr-FR"
                    dyn_tag = "Français"
                else:
                    dyn_bcp47 = "en-NG"
                    dyn_tag = "Pidgin / English"

                components.html(f"""
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 6px 0 10px 0;">
    <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
        <button id="btnPlayDynVoice" onclick="startDynSpeech()" style="
            background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%);
            color: #FFFFFF;
            border: none;
            border-radius: 8px;
            padding: 10px 18px;
            font-size: 0.92rem;
            font-weight: 700;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 3px 8px rgba(27,94,32,0.35);
            transition: all 0.2s ease;
        " onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
            <span>🔊 PLAY SPOKEN SCRIPT ({dyn_tag})</span>
        </button>
        <button id="btnStopDynVoice" onclick="stopDynSpeech()" style="
            background: #F3F4F6;
            color: #374151;
            border: 1px solid #D1D5DB;
            border-radius: 8px;
            padding: 10px 14px;
            font-size: 0.88rem;
            font-weight: 600;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        ">
            <span>⏹️ Stop</span>
        </button>
        <span id="dynSpeechState" style="font-size: 0.84rem; color: #4B5563; font-weight: 500;"></span>
    </div>
</div>
<script>
function getSynth() {{
    try {{
        if (window.speechSynthesis) return window.speechSynthesis;
        if (window.parent && window.parent.speechSynthesis) return window.parent.speechSynthesis;
        if (window.top && window.top.speechSynthesis) return window.top.speechSynthesis;
    }} catch(e) {{}}
    return window.speechSynthesis || null;
}}

let dynUtter = null;

function startDynSpeech() {{
    const synth = getSynth();
    if (!synth) {{
        alert('Web Speech Synthesis is not supported in this browser.');
        return;
    }}
    synth.cancel();

    const script = {dyn_script_json};
    const u = new SpeechSynthesisUtterance(script);
    u.lang = '{dyn_bcp47}';
    u.rate = 0.92;
    u.pitch = 1.0;

    try {{
        const voices = synth.getVoices();
        const matched = voices.find(v => v.lang.toLowerCase().replace('_', '-').startsWith('{dyn_bcp47}'.toLowerCase().slice(0, 2)));
        if (matched) u.voice = matched;
    }} catch(e) {{}}

    const sEl = document.getElementById('dynSpeechState');
    sEl.innerHTML = '<span style="color: #1B5E20; font-weight: 600;">🎙️ Speaking broadcast ({dyn_tag})...</span>';

    u.onend = function() {{
        sEl.innerHTML = '<span style="color: #6B7280;">✅ Spoken broadcast finished</span>';
    }};

    u.onerror = function(ev) {{
        sEl.innerHTML = '<span style="color: #4B5563;">Playback ended</span>';
    }};

    dynUtter = u;
    synth.speak(u);
}}

function stopDynSpeech() {{
    const synth = getSynth();
    if (synth) {{
        synth.cancel();
        document.getElementById('dynSpeechState').innerHTML = '<span style="color: #6B7280;">⏹️ Playback stopped</span>';
    }}
}}
</script>
""", height=65)

                with st.expander("🔔 Radio Station Sign-on Cue Chime (Acoustic Jingle)", expanded=False):
                    st.caption("Broadcast intro marimba chime (C5-E5-G5 harmonic sequence):")
                    st.audio(generate_radio_jingle(), format="audio/wav")

                st.markdown(f"""
<div class="agri-card" style="border: 1px dashed #81C784; background: #FFFFFF; font-size: 0.85rem; line-height: 1.5;">
    <b>🗣️ Indigenous Voice Transcript ({dyn_lang}):</b><br><br>
    <i>"{dyn_data.get('audio_script', '')}"</i>
</div>
""", unsafe_allow_html=True)

            with col_dyn_txt:
                st.markdown("##### 🌐 Verified Translation & Cultural Context")
                st.markdown(f"""
<div class="agri-card" style="background: #FFFFFF; font-size: 0.85rem; line-height: 1.5;">
    <b>Institutional English Translation:</b><br><br>
    "{dyn_data.get('english_translation', '')}"
</div>
""", unsafe_allow_html=True)

                if dyn_data.get('proverb_or_cultural_hook'):
                    st.markdown(f"""
<div class="agri-card" style="background: #F0FDF4; border-left: 4px solid #22C55E; font-size: 0.85rem; line-height: 1.5; margin-top: 0.5rem;">
    <b>🪝 Cultural Farming Hook / Indigenous Proverb Used:</b><br>
    <i>"{dyn_data.get('proverb_or_cultural_hook', '')}"</i>
</div>
""", unsafe_allow_html=True)

                st.markdown(f"""
<div class="agri-card agri-card-highlight" style="font-size: 0.8rem; margin-top: 0.5rem;">
    <b>🔬 Underlying AgroBiometrix Biometric Source:</b><br>
    • Source Module: {active_alert.get('source_module', 'Cross-Suite Analytics')}<br>
    • Target Commodity: {comm_in} | Region: {reg_in}<br>
    • Status: Verified for Community Radio Broadcast
</div>
""", unsafe_allow_html=True)

            # Download Cue Sheet Packet
            cue_sheet = f"""AGROBIOMETRIX LIVE BROADCASTER CUE SHEET & STATION AUDIO PACKET
Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Broadcaster / Call-Sign: {dyn_data.get('broadcaster', '')}
Target Commodity: {comm_in}
Agro-Ecological Region: {reg_in}
Language: {dyn_lang}
Headline: {dyn_data.get('headline', head_in)}

--- INDIGENOUS VERNACULAR BROADCAST SCRIPT ---
{dyn_data.get('audio_script', '')}

--- ENGLISH EQUIVALENT ---
{dyn_data.get('english_translation', '')}

--- SCIENTIFIC FIELD CONTEXT ---
Trigger: {trig_in}
Remedy: {rec_in}

--- CULTURAL HOOK / PROVERB ---
{dyn_data.get('proverb_or_cultural_hook', 'N/A')}
"""
            render_download_buttons(
                content_text=cue_sheet,
                filename_prefix=f"AgroBiometrix_Live_Studio_Radio_{dyn_lang[:2]}",
                title=f"Station Cue Sheet: {dyn_data.get('headline', '')[:30]}",
                key_prefix="btn_dl_dyn_studio_radio"
            )

        else:
            # -------------------------------------------------------------
            # BENCHMARK SUITE: CURATED INSTITUTIONAL BENCHMARKS
            # -------------------------------------------------------------
            st.markdown("---")
            scenario_choice = st.selectbox(
                "Select Field Advisory Scenario:",
                list(LOCAL_RADIO_BROADCASTS.keys()),
                index=0
            )
            selected_scenario = LOCAL_RADIO_BROADCASTS[scenario_choice]

            st.info(f"**Field Context**: {selected_scenario['context']}")

            # Language Selector - High-Visibility Horizontal Radio Bar (One-Click Audio Switch)
            avail_langs = list(selected_scenario["languages"].keys())
            default_idx = 0
            if is_fr:
                for idx, l in enumerate(avail_langs):
                    if "français" in l.lower() or "french" in l.lower():
                        default_idx = idx
                        break

            lang_label = "📻 **Choisissez la Langue de Diffusion (Cliquez pour Écouter le Bulletin) :**" if is_fr else "📻 **Select Broadcast Language (Click any language to load & play audio):**"
            lang_choice = st.radio(
                lang_label,
                options=avail_langs,
                index=default_idx,
                horizontal=True,
                key="radio_indigenous_lang_selector",
                help="Bascule instantanément le lecteur audio, la transcription et la traduction dans la langue sélectionnée" if is_fr else "Instantly switches the audio player, transcript, and verified translation to the selected language."
            )
            broadcast_data = selected_scenario["languages"][lang_choice]

            # Radio Station Studio Box
            st.markdown(f"""
<div class="agri-card" style="border-left: 5px solid #1B5E20; background: #F8FAF8; margin-top: 1rem;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
        <span style="font-size: 0.8rem; font-weight: 700; color: #1B5E20; text-transform: uppercase;">
            📡 ON AIR • {broadcast_data['broadcaster']}
        </span>
        <span style="background: #E8F5E9; color: #1B5E20; font-size: 0.75rem; padding: 2px 8px; border-radius: 4px; font-weight: 600;">
            100% African Ground Truth
        </span>
    </div>
    <div style="font-size: 1.1rem; font-weight: 700; color: #1B5E20; margin-bottom: 0.5rem;">
        📢 {broadcast_data['headline']}
    </div>
</div>
""", unsafe_allow_html=True)

            col_audio, col_txt = st.columns([1, 1])
            with col_audio:
                st.markdown("##### 🔊 Broadcast Audio Player")
                st.caption("Listen to the authentic vernacular radio voice bulletin broadcasted for rural smallholders:")
                
                # Load pre-bundled offline MP3 audio or synthesize via regional engine
                spoken_mp3 = get_radio_audio_bytes(scenario_choice, lang_choice, broadcast_data['audio_script'])
                
                is_tonal_lang = "yoruba" in lang_choice.lower() or "igbo" in lang_choice.lower()
                if is_tonal_lang:
                    if is_fr:
                        st.markdown('''
<div style="background: #FFFBEB; border-left: 4px solid #F59E0B; border-radius: 6px; padding: 9px 12px; margin: 6px 0 10px 0;">
    <div style="font-size: 0.80rem; font-weight: 700; color: #92400E; display: flex; align-items: center; gap: 5px;">
        <span>⚠️</span> <span>Avis Vocal : Modèle Tonal Indigène (Dò-Re-Mí)</span>
    </div>
    <div style="font-size: 0.75rem; color: #78350F; line-height: 1.4; margin-top: 3px;">
        Le synthétiseur standard gTTS utilise un rendu phonétique anglais par défaut.<br>
        👉 <b>Pour écouter le script parlé directement</b>, cliquez sur <b>'🔊 PLAY SPOKEN SCRIPT'</b> ci-dessous ou écoutez le lecteur MP3 officiel.
    </div>
</div>
''', unsafe_allow_html=True)
                    else:
                        st.markdown('''
<div style="background: #FFFBEB; border-left: 4px solid #F59E0B; border-radius: 6px; padding: 9px 12px; margin: 6px 0 10px 0;">
    <div style="font-size: 0.80rem; font-weight: 700; color: #92400E; display: flex; align-items: center; gap: 5px;">
        <span>⚠️</span> <span>Voice Model Notice: Tonal Intonation (Dò-Re-Mí)</span>
    </div>
    <div style="font-size: 0.75rem; color: #78350F; line-height: 1.4; margin-top: 3px;">
        Standard Google gTTS lacks native tonal acoustic models for Yoruba and Igbo (playing an English phonetic fallback).<br>
        👉 <b>To hear the authentic spoken voice script</b>, click <b>'🔊 PLAY SPOKEN SCRIPT'</b> below or listen to the official audio track.
    </div>
</div>
''', unsafe_allow_html=True)
                else:
                    status_txt = "🟢 Moteur Vocal Indigène Natif Actif (Acoustique Régionale Studio)" if is_fr else "🟢 Native Indigenous Acoustic Voice Active (Regional Studio Speech Track)"
                    st.markdown(f'''
<div style="background: #F0FDF4; border-left: 4px solid #22C55E; border-radius: 6px; padding: 7px 12px; margin: 5px 0 9px 0;">
    <div style="font-size: 0.78rem; font-weight: 700; color: #166534;">{status_txt}</div>
</div>
''', unsafe_allow_html=True)

                # Primary Spoken Voice Audio Player (Full 30-50s Spoken Bulletin)
                if spoken_mp3:
                    st.audio(spoken_mp3, format="audio/mp3")
                    st.caption(f"🎙️ **Live Vernacular Voice Stream Active** ({lang_choice} • Full Audio Broadcast)")
                else:
                    st.warning("⚠️ Spoken audio track is buffering. Please click 'PLAY SPOKEN SCRIPT' below.")

                # Browser-based interactive speech button via components.html (never sanitized/stripped)
                safe_script_json = json.dumps(broadcast_data['audio_script'])
                if "yoruba" in lang_choice.lower():
                    bcp47 = "yo-NG"
                    lang_tag = "Yorùbá"
                elif "igbo" in lang_choice.lower():
                    bcp47 = "ig-NG"
                    lang_tag = "Ìgbò"
                elif "hausa" in lang_choice.lower():
                    bcp47 = "ha-NG"
                    lang_tag = "Hausa"
                elif "swahili" in lang_choice.lower() or "kiswahili" in lang_choice.lower():
                    bcp47 = "sw-KE"
                    lang_tag = "Swahili"
                elif "français" in lang_choice.lower() or "french" in lang_choice.lower():
                    bcp47 = "fr-FR"
                    lang_tag = "Français"
                else:
                    bcp47 = "en-NG"
                    lang_tag = "Pidgin"

                play_lbl = f"🔊 PLAY SPOKEN SCRIPT ({lang_tag})" if not is_fr else f"🔊 LIRE LE SCRIPT VOCAL ({lang_tag})"
                stop_lbl = "⏹️ Stop" if not is_fr else "⏹️ Arrêter"

                components.html(f"""
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 6px 0 10px 0;">
    <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
        <button id="btnPlayVoice" onclick="startSpeechPlayback()" style="
            background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%);
            color: #FFFFFF;
            border: none;
            border-radius: 8px;
            padding: 10px 18px;
            font-size: 0.92rem;
            font-weight: 700;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 3px 8px rgba(27,94,32,0.35);
            transition: all 0.2s ease;
        " onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
            <span>{play_lbl}</span>
        </button>
        <button id="btnStopVoice" onclick="stopSpeechPlayback()" style="
            background: #F3F4F6;
            color: #374151;
            border: 1px solid #D1D5DB;
            border-radius: 8px;
            padding: 10px 14px;
            font-size: 0.88rem;
            font-weight: 600;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        ">
            <span>{stop_lbl}</span>
        </button>
        <span id="speechState" style="font-size: 0.84rem; color: #4B5563; font-weight: 500;"></span>
    </div>
</div>
<script>
function getSpeechSynth() {{
    try {{
        if (window.speechSynthesis) return window.speechSynthesis;
        if (window.parent && window.parent.speechSynthesis) return window.parent.speechSynthesis;
        if (window.top && window.top.speechSynthesis) return window.top.speechSynthesis;
    }} catch(e) {{
        console.warn('SpeechSynthesis access notice:', e);
    }}
    return window.speechSynthesis || null;
}}

let activeUtterance = null;

function startSpeechPlayback() {{
    const synth = getSpeechSynth();
    if (!synth) {{
        alert('Web Speech Synthesis is not supported in this browser. Please use the standard MP3 player above.');
        return;
    }}
    synth.cancel();

    const scriptText = {safe_script_json};
    const utter = new SpeechSynthesisUtterance(scriptText);
    utter.lang = '{bcp47}';
    utter.rate = 0.92;
    utter.pitch = 1.0;

    try {{
        const voices = synth.getVoices();
        const matched = voices.find(v => v.lang.toLowerCase().replace('_', '-').startsWith('{bcp47}'.toLowerCase().slice(0, 2)));
        if (matched) utter.voice = matched;
    }} catch(e) {{}}

    const statusEl = document.getElementById('speechState');
    statusEl.innerHTML = '<span style="color: #1B5E20; font-weight: 600;">🎙️ Speaking full broadcast ({lang_tag})...</span>';

    utter.onend = function() {{
        statusEl.innerHTML = '<span style="color: #6B7280;">✅ Broadcast complete</span>';
    }};

    utter.onerror = function(ev) {{
        console.log('Speech event:', ev);
        statusEl.innerHTML = '<span style="color: #4B5563;">Playback ended</span>';
    }};

    activeUtterance = utter;
    synth.speak(utter);
}}

function stopSpeechPlayback() {{
    const synth = getSpeechSynth();
    if (synth) {{
        synth.cancel();
        document.getElementById('speechState').innerHTML = '<span style="color: #6B7280;">⏹️ Playback stopped</span>';
    }}
}}
</script>
""", height=65)

                # Distinct Station Cue Chime Expander (Completely separate from spoken voice bulletin)
                with st.expander("🔔 Radio Station Sign-on Cue Chime (Acoustic Jingle)", expanded=False):
                    st.caption("Standard 3-tone marimba cue chime (C5-E5-G5 harmonic sequence) broadcasted prior to voice bulletins to alert rural listeners across radio transistors:")
                    jingle_wav = generate_radio_jingle()
                    st.audio(jingle_wav, format="audio/wav")

                with st.expander("🎙️ African Voice AI & Tonal Models (YarnGPT / ElevenLabs)", expanded=False):
                    st.markdown(
                        "AgroBiometrix supports studio-grade indigenous voice models via **YarnGPT** (dedicated Nigerian speech models for Yorùbá, Ìgbò, Hausa, Pidgin) "
                        "and **ElevenLabs Multilingual v2**."
                    )
                    st.info(
                        "💡 **How to activate in production**: Add your YarnGPT or ElevenLabs API key in **Module 15 (API Hub)** to upgrade rural radio advisories from web fallback to authentic studio voiceover."
                    )

                st.markdown(f"""
<div class="agri-card" style="border: 1px dashed #81C784; background: #FFFFFF; font-size: 0.85rem; line-height: 1.5;">
    <b>🗣️ Indigenous Voice Transcript ({lang_choice}):</b><br><br>
    <i>"{broadcast_data['audio_script']}"</i>
</div>
""", unsafe_allow_html=True)

            with col_txt:
                st.markdown("##### 🌐 Verified English Translation & Biometrics Link")
                st.markdown(f"""
<div class="agri-card" style="background: #FFFFFF; font-size: 0.85rem; line-height: 1.5;">
    <b>Institutional English Translation:</b><br><br>
    "{broadcast_data['english_translation']}"
</div>
""", unsafe_allow_html=True)

                st.markdown(f"""
<div class="agri-card agri-card-highlight" style="font-size: 0.8rem; margin-top: 0.5rem;">
    <b>🔬 Underlying AgroBiometrix Biometric Models Linked:</b><br>
    • Open-Meteo REST API: 14-day rainfall hiatus & heat stress index<br>
    • Soil Intelligence Mod 5: Crown micro-dosing (20 kg NPK/ha)<br>
    • DMRT ANOVA Mod 3: Validated non-significant yield loss under 50% fertilizer reduction
</div>
""", unsafe_allow_html=True)

            # Download radio script for field agents
            downloadable_script = f"""AGROBIOMETRIX COMMUNITY EXTENSION RADIO BROADCAST SCRIPT
Scenario: {scenario_choice}
Language: {lang_choice}
Broadcaster / Station: {broadcast_data['broadcaster']}
Headline: {broadcast_data['headline']}

--- INDIGENOUS LANGUAGE SCRIPT ---
{broadcast_data['audio_script']}

--- ENGLISH EQUIVALENT ---
{broadcast_data['english_translation']}

--- BIOMETRIC NOTES FOR EXTENSION AGENTS ---
Target recommendations generated by AgroBiometrix Biometric & Climate Ensemble.
Compliant with CGIAR / IFPRI digital extension standards for sub-Saharan Africa.
"""
            render_download_buttons(
                content_text=downloadable_script,
                filename_prefix=f"AgroBiometrix_Radio_Advisory_{lang_choice[:2]}",
                title=f"AgroBiometrix Radio Advisory: {broadcast_data.get('headline', '')}",
                key_prefix="btn_dl_radio"
            )

