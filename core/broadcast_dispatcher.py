"""
AgroBiometrix - Central Agricultural Broadcast Dispatcher & Event Bus
Bridges complex biometric and laboratory analytics (Soils, Breeding, Livestock THI, Climate, Pests)
directly into real-time indigenous vernacular radio broadcasts across Sub-Saharan Africa.
"""

import os
import json
import datetime
import streamlit as st

# Default benchmark seed alerts across the major intelligence suites
DEFAULT_BROADCAST_QUEUE = [
    {
        "id": "DISPATCH-2026-001",
        "timestamp": "2026-10-31 09:15",
        "source_module": "Module 4: Soil Fertility & Stoichiometric Optimizer",
        "commodity": "Maize & Cassava",
        "region": "Southwest Nigeria (Oyo/Ogun Transition Zone)",
        "headline": "Severe Phosphorus & Zinc Fixation in Acidic Ultisols",
        "agronomic_trigger": "Soil pH < 5.1 with active Al3+ toxicity and high P-sorption capacity. Surface urea broadcast causing 40% ammonia volatilization.",
        "recommendation": "Halt surface urea broadcast. Apply 2.5 t/ha agricultural lime with organic compost. Switch to micro-dosing single superphosphate (SSP) at root zone.",
        "status": "Ready for Air"
    },
    {
        "id": "DISPATCH-2026-002",
        "timestamp": "2026-10-31 11:30",
        "source_module": "Module 5: Livestock Biometrics & THI Heat Stress",
        "commodity": "Pastoral Zebu Cattle & Dairy",
        "region": "Sudano-Sahelian Belt (Kano, Jigawa, Katsina)",
        "headline": "THI > 82 Extreme Heat Stress & Ruminal Alkalosis Warning",
        "agronomic_trigger": "Temperature-Humidity Index exceeding 82 during mid-day pasture transit. Milk yield drops by 28%, respiratory rate > 80 bpm.",
        "recommendation": "Shift grazing to crepuscular hours (5:30-8:30 AM and 5:00-7:30 PM). Add sodium bicarbonate and salt licks to shaded watering troughs.",
        "status": "Ready for Air"
    },
    {
        "id": "DISPATCH-2026-003",
        "timestamp": "2026-10-31 13:45",
        "source_module": "Module 8: Agro-Ecosystems & Climate Risk",
        "commodity": "Cowpea & Sorghum",
        "region": "Northern Savanna (Kaduna/Kano)",
        "headline": "14-Day Mid-Season Dry Spell Anomaly Following Flash Rain",
        "agronomic_trigger": "Soil moisture reservoir depleted to 22% during vegetative stage. Harmattan dust haze reducing photosynthetically active radiation (PAR).",
        "recommendation": "Apply organic mulch immediately to conserve residual root moisture. Postpone top-dressing until steady convective rainfall resumes.",
        "status": "Ready for Air"
    },
    {
        "id": "DISPATCH-2026-004",
        "timestamp": "2026-10-31 14:20",
        "source_module": "Module 5: Smallholder Cuniculture & Poultry",
        "commodity": "Rabbits (Cuniculture)",
        "region": "Sub-Humid Forest (Ondo/Ekiti/Edo)",
        "headline": "Cyanogenic Glucoside Toxicity in Wilted Cassava Peelings",
        "agronomic_trigger": "Farmers feeding fresh or half-dried wilted cassava peels to breeding does during morning feeding, causing acute bloat and doe mortality.",
        "recommendation": "Never feed fresh or damp wilted cassava peels. Peels must be sun-dried for 48 hours to dissipate hydrogen cyanide (HCN) before offering.",
        "status": "Ready for Air"
    }
]


def init_broadcast_queue():
    """Initializes the global broadcast dispatch queue in session state."""
    if "broadcast_dispatch_queue" not in st.session_state:
        st.session_state["broadcast_dispatch_queue"] = list(DEFAULT_BROADCAST_QUEUE)


def queue_broadcast_advisory(source_module: str, commodity: str, region: str, headline: str, agronomic_trigger: str, recommendation: str):
    """Allows any analytical module in AgroBiometrix to push a new finding to the radio queue."""
    init_broadcast_queue()
    new_id = f"DISPATCH-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}"
    item = {
        "id": new_id,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "source_module": source_module,
        "commodity": commodity,
        "region": region,
        "headline": headline,
        "agronomic_trigger": agronomic_trigger,
        "recommendation": recommendation,
        "status": "Ready for Air"
    }
    # Prepend newest
    st.session_state["broadcast_dispatch_queue"].insert(0, item)
    return item


def render_dispatch_trigger_card(source_module: str, commodity: str, region: str, headline: str, trigger_summary: str, recommendation_summary: str):
    """Renders a standard 'Send to Extension Radio' button at the bottom of any analytical module."""
    init_broadcast_queue()
    st.markdown("---")
    c_info, c_btn = st.columns([3, 1])
    with c_info:
        st.markdown(f"""
<div style="font-size: 0.84rem; color: #1B5E20; font-weight: 600; display: flex; align-items: center; gap: 6px;">
    <span>📡</span> <span>Last-Mile Extension Link: Ready to broadcast this finding to smallholder radio stations?</span>
</div>
<div style="font-size: 0.76rem; color: #4B5563; margin-top: 2px;">
    Converts this scientific calculation into spoken <b>Yorùbá, Hausa, Swahili, French, or Pidgin</b> radio bulletins.
</div>
""", unsafe_allow_html=True)
    with c_btn:
        btn_key = f"btn_dispatch_{source_module.replace(' ', '_')}_{headline[:10]}"
        if st.button("📢 Send to Radio Queue", key=btn_key, help="Dispatches this analytical finding to the Community Extension Radio Studio"):
            queue_broadcast_advisory(
                source_module=source_module,
                commodity=commodity,
                region=region,
                headline=headline,
                agronomic_trigger=trigger_summary,
                recommendation=recommendation_summary
            )
            st.success("✅ Finding queued! Switch to 'AI Research Scientist Studio > Last-Mile Radio Advisory' to generate spoken broadcast.")


def generate_vernacular_radio_script(headline: str, commodity: str, region: str, trigger: str, recommendation: str, target_lang: str) -> dict:
    """
    Dynamically formulates an authentic indigenous radio broadcast script
    using Gemini AI if available, or Africa-grounded expert linguistic heuristics.
    """
    lang_clean = target_lang.lower()
    
    # Check if live Gemini model is configured
    gemini_model = st.session_state.get("gemini_model")
    if gemini_model:
        prompt = f"""
You are a master Pan-African community radio broadcaster and agricultural extension communicator.
Translate the following scientific agricultural research diagnosis into a compelling, 45-second spoken radio bulletin.

Context:
- Target Commodity: {commodity}
- Target Agro-Ecological Region: {region}
- Scientific Finding / Trigger: {trigger}
- Agronomic Recommendation: {recommendation}
- Broadcast Language: {target_lang}

Rules:
1. Tone: Respectful, energetic, authoritative like a trusted community elder or extension officer on rural transistor radio.
2. Structure: 
   - Welcoming greeting suited to the culture
   - Direct alert stating the crop/animal risk without jargon
   - Practical, actionable field remedy (using local kitchen/farm metaphors like bottle caps, handfuls, shaded trees)
   - Encouraging sign-off
3. Language: Provide authentic, natural phrasing in {target_lang}. If Yoruba, use appropriate tone markers. If Hausa, use natural Northern Nigerian broadcasting style. If French, use clear Pan-African rural French.
4. Provide the output as a valid JSON object with exactly these keys:
   - "broadcaster": Name and station call-sign suited to the region (e.g. "Malam Dan-Kano • AgroBiometrix Radio FM")
   - "headline": Catchy headline in {target_lang}
   - "audio_script": The exact spoken script in {target_lang} (approx. 400-600 characters)
   - "english_translation": Complete faithful English translation
   - "proverb_or_cultural_hook": A relevant indigenous proverb or cultural farming metaphor used.

Output JSON ONLY:
"""
        try:
            resp = gemini_model.generate_content(prompt)
            txt = resp.text.strip()
            if txt.startswith("```json"):
                txt = txt[7:-3].strip()
            elif txt.startswith("```"):
                txt = txt[3:-3].strip()
            data = json.loads(txt)
            if "audio_script" in data:
                return data
        except Exception:
            pass  # Fall back to linguistic heuristics below

    # Intelligent Offline / Heuristic Synthesis
    if "yoruba" in lang_clean:
        return {
            "broadcaster": f"Baálẹ̀ Àgbẹ̀ Olúṣẹ́gun • AgroBiometrix Radio FM ({region})",
            "headline": f"Ìkìlọ̀ Pàjáwìrì fún Àwọn Àgbẹ̀ {commodity} ní Agbègbè {region}",
            "audio_script": (
                f"Ẹ̀kú ojúmọ́ gbogbo ẹ̀yin àgbẹ̀ {commodity} wa ọ̀wọ́n! "
                f"Ìkìlọ̀ pàjáwìrì dé láti àwọn onímọ̀ sáyẹ́ǹsì AgroBiometrix: {trigger}. "
                f"Àmọ̀ràn pàtàkì fún gbogbo yín: {recommendation}. "
                "Ẹ rántí pé: 'Àbọ̀ ọ̀rọ̀ là ń sọ fún ọmọlúwàbí, tó bá dé inú ẹ̀ a di odidi.' "
                "Ẹ tẹ̀lé àmọ̀ràn yìí láti dáàbò bo èso oko yín àti owó tí ẹ ná sí i. Ẹ ṣe púpọ̀, oko á gbè wá o!"
            ),
            "english_translation": (
                f"Greetings to all our esteemed {commodity} farmers! "
                f"An urgent advisory has arrived from AgroBiometrix scientists regarding {region}: {trigger}. "
                f"Crucial recommendation: {recommendation}. "
                "Remember the wisdom: 'A word is enough for the wise.' Protect your harvests and investments."
            ),
            "proverb_or_cultural_hook": "Àbọ̀ ọ̀rọ̀ là ń sọ fún ọmọlúwàbí (A word is enough for the wise)"
        }
    elif "hausa" in lang_clean:
        return {
            "broadcaster": f"Malam Ibrahim Dan-Arewa • AgroBiometrix Radio FM ({region})",
            "headline": f"Muhimmiyar Sanarwa ga Manoman {commodity} a Yankin {region}",
            "audio_script": (
                f"Assalamu alaikum 'yan uwa manoma masu albarka! "
                f"Wata gaggawar shawara ce ta fito daga cibiyar kimiyya ta AgroBiometrix game da {commodity}: {trigger}. "
                f"Kwararrun masana sun ba da shawarar cewa: {recommendation}. "
                "Kamar yadda aka sani: 'Kowa ya tuna bara, bai ji dadin bana ba.' "
                "Ku kiyaye gonakinku da dabbobinku don samun babban rabo da albarka. Allah Ya ba da sa'a!"
            ),
            "english_translation": (
                f"Peace be upon you, blessed farmers! "
                f"An urgent bulletin has been released by the AgroBiometrix Science Hub regarding {commodity} in {region}: {trigger}. "
                f"Specialist guidance: {recommendation}. Protect your farm to reap bountiful blessings."
            ),
            "proverb_or_cultural_hook": "Kowa ya tuna bara, bai ji dadin bana ba (He who remembers past hardships strives harder today)"
        }
    elif "swahili" in lang_clean:
        return {
            "broadcaster": f"Bwana Juma Mkulima • AgroBiometrix Radio Sauti ya Shamba ({region})",
            "headline": f"Tahadhari Muhimu kwa Wakulima na Wafugaji wa {commodity} ({region})",
            "audio_script": (
                f"Habari za asubuhi wakulima hodari wa {commodity}! "
                f"Hapa kuna ripoti maalum kutoka Taasisi ya AgroBiometrix: {trigger}. "
                f"Ushauri wa dharura kutoka kwa wataalamu wetu wa kilimo na mifugo: {recommendation}. "
                "Wazee walisema: 'Haba na haba, hujaza kibaba.' "
                "Fuata maagizo haya sasa ili kulinda mazao na mifugo yako dhidi ya hasara. Kilimo ni uti wa mgongo!"
            ),
            "english_translation": (
                f"Good morning diligent {commodity} farmers! "
                f"Here is a special alert from the AgroBiometrix Institute: {trigger}. "
                f"Urgent guidance from agronomists: {recommendation}. "
                "As the elders say: 'Little by little fills the measure.' Protect your investments now."
            ),
            "proverb_or_cultural_hook": "Haba na haba, hujaza kibaba (Little by little fills the measure)"
        }
    elif "français" in lang_clean or "french" in lang_clean:
        return {
            "broadcaster": f"Ingénieur Amadou Diallo • Radio Rurale AgroBiometrix ({region})",
            "headline": f"Bulletin d'Alerte Agricole Urgent : Filière {commodity} ({region})",
            "audio_script": (
                f"Chers producteurs et éleveurs de {commodity}, bonjour ! "
                f"Voici un communiqué urgent de l'Institut AgroBiometrix concernant le bassin de {region} : {trigger}. "
                f"Les agronomes recommandent formellement : {recommendation}. "
                "Comme le dit le proverbe africain : 'Mieux vaut prévenir que guérir au champ.' "
                "Appliquez ces consignes sans attendre pour préserver votre récolte et vos marges. Bonne campagne à tous !"
            ),
            "english_translation": (
                f"Dear {commodity} producers, greetings! "
                f"Here is an urgent advisory from AgroBiometrix for {region}: {trigger}. "
                f"Agronomists strictly recommend: {recommendation}. "
                "Prevention is better than cure in the field. Protect your harvests."
            ),
            "proverb_or_cultural_hook": "Mieux vaut prévenir que guérir au champ (Prevention is better than cure)"
        }
    else:
        # Default West African Pidgin / English
        return {
            "broadcaster": f"Oga Landlord Agro • AgroBiometrix Farmers Voice FM ({region})",
            "headline": f"Urgent Beta Farm Warning for All {commodity} Farmers for {region}",
            "audio_script": (
                f"Good morning my correct farmer people! "
                f"AgroBiometrix research scientists don bring urgent message for our {commodity} farmers: {trigger}. "
                f"Wetin you suppose do sharp-sharp: {recommendation}. "
                "No forget say 'Better soup, na na money make am!' "
                "Protect your farm and your pocket so that your harvest go make sense. Make agriculture sweet everybody!"
            ),
            "english_translation": (
                f"Good morning great farmers! AgroBiometrix scientists bring an urgent message for {commodity}: {trigger}. "
                f"Immediate action required: {recommendation}. Protect your farm and your investment."
            ),
            "proverb_or_cultural_hook": "Better soup, na money make am (Quality results require sound practices)"
        }
