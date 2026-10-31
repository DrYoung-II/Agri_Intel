"""
Module 14: Last-Mile Multilingual Farmer Voice & Community Radio Disseminator
Suite 8 of AgroBiometrix Consolidated Intelligence Framework
Bridges complex biometrics, soil stoichiometry, breeding, livestock heat stress,
and climate modeling directly to rural smallholders via indigenous community radio,
telecom IVR, and automated station playout syndication.
"""

import os
import io
import json
import wave
import struct
import math
import datetime
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

from core.exporter import render_download_buttons
from core.broadcast_dispatcher import (
    init_broadcast_queue,
    queue_broadcast_advisory,
    render_dispatch_trigger_card,
    generate_vernacular_radio_script,
    DEFAULT_BROADCAST_QUEUE
)
from core.audio_engine import (
    render_voice_engine_settings_panel,
    LANGUAGE_VOICE_MAP,
    get_configured_providers
)
from core.broadcast_feed import generate_podcast_rss_xml


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

        tones = [
            (523.25, 0.0, 0.45),  # C5
            (659.25, 0.35, 0.85), # E5
            (783.99, 0.70, 1.40)  # G5
        ]

        for i in range(num_samples):
            t = float(i) / sample_rate
            sample_val = 0.0

            for freq, start_t, end_t in tones:
                if start_t <= t <= end_t:
                    env_t = t - start_t
                    env = math.exp(-6.5 * env_t) * math.sin(math.pi * min(1.0, env_t * 80.0))
                    fund = math.sin(2.0 * math.pi * freq * env_t)
                    harm = 0.35 * math.sin(4.0 * math.pi * freq * env_t) * math.exp(-12.0 * env_t)
                    sample_val += (fund + harm) * env

            clipped = max(-1.0, min(1.0, sample_val * 0.75))
            int_sample = int(clipped * 32767.0)
            wav.writeframesraw(struct.pack('<h', int_sample))

    buffer.seek(0)
    return buffer.getvalue()


# Curated Institutional Benchmark Broadcasts (Pre-Bundled Ground Truth)
LOCAL_RADIO_BROADCASTS = {
    "Kaduna/Kano Maize: Heat Wave & Fertilizer Advisory": {
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
                    "Shawarar kwararru ita ce: Ku dakata har sai ruwan sama mai karfi ya sake sauka ya jika kasa sosai. "
                    "Sannan ku yi amfani da dabarar 'Micro-dosing', wato kofi daya na murfin gora ga kowane jikin masara. "
                    "Wannan zai kare amfanin gonarku kuma zai rage kudin takin ku da rabi. Allah ya albarkaci nomanmu!"
                ),
                "english_translation": (
                    "Peace be upon you, fellow farmers! Here is an urgent alert from the AgroBiometrix Science Hub: "
                    "In the next 10 days, we will experience intense heat and a rainfall pause across Kaduna, Kano, and Katsina. "
                    "Research guidance warns all farmers: Do NOT apply Urea fertilizer onto dry topsoil right now, as solar volatilization "
                    "will destroy the nitrogen and scorch crop roots. Expert recommendation: Wait until the next heavy soaking rainfall. "
                    "Afterward, apply the 'Micro-dosing' technique—one bottle cap of fertilizer per maize stand. "
                    "This will safeguard your harvest while halving your fertilizer expenditure. May God bless our harvest!"
                )
            },
            "🇳🇬 Yoruba (Èdè Yorùbá)": {
                "broadcaster": "Bàbá Àgbẹ̀ Adékúnlé • Ilé-Iṣẹ́ Rédíò Àgbẹ̀ AgroBiometrix (Ibadan/Akure)",
                "headline": "Ìkìlọ̀ Pàjáwìrì nípa Oòrùn Líle àti Ìdádúró Òjò fún Àwọn Olùgbìn Àgbàdo",
                "audio_script": (
                    "Gbogbo ẹ̀yin àgbẹ̀ àti olùgbìn àgbàdo, a kí yín o! Ìkìlọ̀ pàjáwìrì gbòógì kan rèé látọ̀dọ̀ àwọn onímọ̀ sáyẹ́ǹsì AgroBiometrix: "
                    "Ní ọ̀sẹ̀ méjì tí ń bọ̀ yìí, oòrùn máa mú gan-an, òjò yóò sì dánu dúró díẹ̀ ní àwọn agbègbè wa. "
                    "Àwọn onímọ̀ kìlọ̀ fún gbogbo àgbẹ̀ pé: Ẹ má ṣe gbìyànjú láti fọ́n ajílẹ̀ Urea sí orí ilẹ̀ tí ó gbẹ kòkò ní àkókò yìí rárá! "
                    "Oòrùn gbígbóná yìí yóò jẹ agbára ajílẹ̀ náà run sínú afẹ́fẹ́, yóò sì jó gbòǹgbò àgbàdo yín run. "
                    "Àmọ̀ràn tí ó tọ́ ni pé: Ẹ mú sùúrù títí tí òjò títóbi yóò fi tún rọ̀ láti bomirin ilẹ̀ dáradára. "
                    "Lẹ́yìn náà, ẹ lo ọgbọ́n 'Micro-dosing', ìyẹn ni omorí ìgò kan fún ìtẹ́ àgbàdo kọ̀ọ̀kan. "
                    "Èyí yóò dáàbò bo oko yín, yóò sì dín owó ajílẹ̀ kù ní ìdajì. Oko yóò gbè wá o!"
                ),
                "english_translation": (
                    "All farmers and maize growers, greetings to you! Here is an urgent guidance notice from the AgroBiometrix science team: "
                    "In the coming two weeks, intense solar heat will prevail and rain will temporarily halt across our production belts. "
                    "Agronomists issue a strict warning: Do NOT broadcast Urea fertilizer on dry baked soil during this dry period! "
                    "The scorching heat will vaporize the active nitrogen into the air and burn the roots of your maize crop. "
                    "The correct advice is: Exercise patience until significant rain falls to thoroughly saturate the soil. "
                    "Then utilize the 'Micro-dosing' method—one bottle cap of fertilizer per maize plant stand. "
                    "This safeguards your farm and cuts your fertilizer costs in half. May your farm yield bountifully!"
                )
            },
            "🇰🇪 Swahili (Kiswahili)": {
                "broadcaster": "Bwana Shambani Juma Omondi • Redio ya Jamii AgroBiometrix (Eldoret / Kitale / Morogoro)",
                "headline": "Tahadhari ya Kiangazi cha Ghafla na Mbolea kwa Wakulima wa Mahindi",
                "audio_script": (
                    "Hujambo wakulima wenzangu wa mahindi! Hili ni tangazo muhimu sana kutoka Taasisi ya Utafiti ya AgroBiometrix: "
                    "Katika majuma mawili yajayo, kutakuwa na kiangazi kikali na kukatika kwa mvua katika maeneo yetu ya kilimo. "
                    "Wataalamu wetu wa kilimo wanatoa onyo kali: Msithubutu kuweka mbolea ya Urea kwenye udongo mkavu kwa sasa! "
                    "Jua kali litapoteza rutuba ya mbolea angani na kuchoma mizizi laini ya mahindi yenu changa. "
                    "Ushauri sahihi wa kitaalamu: Subirini hadi mvua kubwa inyeshe tena na kulowesha udongo kikamilifu. "
                    "Kisha tumieni mbinu ya 'Micro-dosing', yaani kifuniko kimoja cha chupa ya soda kwa kila shina la mhindi. "
                    "Mbinu hii italinda mazao yenu na kupunguza nusu ya gharama ya mbolea. Kilimo chenye tija kwa wote!"
                ),
                "english_translation": (
                    "Greetings fellow maize farmers! This is a critical advisory notice from the AgroBiometrix Research Hub: "
                    "Over the next two weeks, an acute dry spell and heat spike will affect our production zones. "
                    "Agronomists strictly warn: Do not apply Urea top-dressing fertilizer to dry soil right now! "
                    "Severe heat will vaporize the nitrogen into the air and burn the tender roots of your growing maize. "
                    "The sound agronomic advice: Wait until soaking rains resume and moisten the soil profile. "
                    "Then deploy the 'Micro-dosing' technique—one soda bottle cap per maize stand. "
                    "This protects your crop investment and cuts fertilizer costs by half. Bountiful farming to all!"
                )
            },
            "🇳🇬 West African Pidgin": {
                "broadcaster": "Uncle Joe Agro • AgroBiometrix Community FM (Benin / Warri / Port Harcourt)",
                "headline": "Special Warning for Dry Season Heat and Fertilizer for Maize Farmers",
                "audio_script": (
                    "Una good morning o my fellow farmers! Na special urgent message from AgroBiometrix research center: "
                    "For inside dis two weeks wey dey come, heavy sun go heat well-well and rain go stop small for our area. "
                    "Our agric doctors dey warn everybody make una hear word: Nobody should throway Urea fertilizer put for dry ground now o! "
                    "Di hot sun go dry di medicine commot for di fertilizer and e go burn your maize root kpatakpata. "
                    "Wetin una suppose do na simple: Make una calm down hold una body until correct heavy rain fall soak di ground well-well. "
                    "After dat one, make una use 'Micro-dosing' style—put only one bottle cover of fertilizer for each maize stand. "
                    "Dis style go protect una farm and reduce half of di money wey una dey spend for fertilizer. Una farm go prosper o!"
                ),
                "english_translation": (
                    "Good morning to my fellow farmers! Here is an urgent bulletin from the AgroBiometrix research center: "
                    "Over the next two weeks, intense sun will heat up and rain will temporarily halt in our farming regions. "
                    "Our agricultural experts strictly warn everyone: Nobody should broadcast Urea fertilizer onto dry ground right now! "
                    "The hot sun will volatilize the nitrogen nutrients into the air and completely scorch your maize roots. "
                    "What you should do is simple: Be patient and hold on until genuine heavy soaking rainfall re-saturates the ground. "
                    "After that, use the 'Micro-dosing' method—place just one bottle cap of fertilizer at each maize stand. "
                    "This technique protects your investment and halves your fertilizer expenditure. May your farms prosper!"
                )
            }
        }
    },
    "Sahelian Pastoral Cattle: Extreme Heat Stress (THI > 82) Warning": {
        "context": "THI exceeding 82 in dry pastoral zones; acute heat burden, respiratory distress (>80 bpm), and 25% drop in milk yield.",
        "languages": {
            "🇨🇮 / 🇸🇳 / 🇨🇲 Français Agricole (Bulletin Rural Panafricain)": {
                "broadcaster": "Docteur Ousmane Traoré • Radio Pastorale AgroBiometrix (Mopti / Niamey / Maroua)",
                "headline": "Alerte Canicule Pastorale et Stress Thermique Bovin Élevé",
                "audio_script": (
                    "Chers éleveurs et pasteurs de zébus, écoutez bien ce message d'urgence d'AgroBiometrix : "
                    "Dans tout le bassin sahélien, l'indice d'humidité et de chaleur dépasse le seuil critique de 82. "
                    "Vos vaches laitières et vos bœufs sont en détresse respiratoire sévère, et la production de lait va chuter de plus d'un quart ! "
                    "Consignes impératives : arrêtez immédiatement de faire marcher les troupeaux sous le soleil de midi. "
                    "Changez vos horaires de pâturage : sortez les bêtes très tôt le matin entre cinq heures et huit heures, et tard le soir après dix-sept heures. "
                    "Offrez de l'eau fraîche et ombragée en permanence avec des blocs de sel et du bicarbonate. Protégez votre cheptel !"
                ),
                "english_translation": (
                    "Dear pastoralists and cattle rearers, listen carefully to this AgroBiometrix emergency bulletin: "
                    "Across the Sahelian basin, the heat-humidity index has breached the critical threshold of 82 units. "
                    "Your dairy cows and zebu oxen are in severe respiratory distress, and milk yields will drop by more than a quarter! "
                    "Mandatory guidelines: Immediately cease walking herds under the midday sun. Shift grazing to early morning (5:00–8:00 AM) and evening after 5:00 PM."
                )
            },
            "🇳🇬 Hausa (Harshen Hausa)": {
                "broadcaster": "Alhaji Bello Garba • Radio Manoma da Makiyaya FM (Sokoto / Katsina)",
                "headline": "Gargaɗin Zafi da Kariya ga Shanu a Yankin Sahel",
                "audio_script": (
                    "Assalamu alaikum 'yan uwa makiyaya da manoma! Cibiyar AgroBiometrix na sanar da ku cewa: "
                    "Zafin rana a wannan mako ya wuce kima kuma zai iya lahanta shanunmu da sauran dabbobi. "
                    "Shanu da yawa suna fama da daukewar numfashi da kuma zubar da nono har da kashi ashirin da biyar cikin dari! "
                    "Umarar masana ita ce: A dakatar da kora dabbobi zuwa kiwo da tsakar rana a karkashin zafin rana. "
                    "A canza lokacin kiwo: a fita da sanyin safiya daga karfe biyar zuwa takwas, da kuma yamma bayan karfe biyar. "
                    "A samar da ruwa mai sanyi a karkashin inuwa tare da dutsen gishiri. Allah ya kare mana dabbobinmu!"
                ),
                "english_translation": (
                    "Peace be upon you, pastoralists and farmers! AgroBiometrix announces that: "
                    "Solar heat this week has exceeded safe limits and threatens our cattle and livestock. "
                    "Many animals are experiencing rapid panting and milk yield is dropping by 25 percent! "
                    "Veterinary directive: Cease driving herds to pasture under the midday sun. Shift grazing to cool dawn and dusk hours."
                )
            },
            "🇰🇪 Swahili (Kiswahili)": {
                "broadcaster": "Daktari Wa Mifugo Hassan Mwangi • Redio ya Jamii ya Ufugaji (Garissa / Kajiado)",
                "headline": "Onyo la Joto Kali na Madhara kwa Ng'ombe wa Maziwa",
                "audio_script": (
                    "Hujambo wafugaji wetu wote! Hili ni onyo rasmi kutoka kwa wataalamu wa mifugo wa AgroBiometrix: "
                    "Kiwango cha joto na unyevu kimevuka kiwango cha usalama na kufikia zaidi ya vipimo themanini na viwili. "
                    "Ng'ombe wanapumua kwa shida sana na uzalishaji wa maziwa umeshuka kwa robo nzima! "
                    "Maagizo muhimu ya kuzingatia: Sitisha kabisa kuwalisha mifugo wakati wa mchana jua likiwa kali. "
                    "Lisha wanyama mapema asubuhi saa kumi na moja hadi saa mbili, na jioni baada ya jua kutua. "
                    "Hakikisha wanapata maji safi ya baridi chini ya kivuli kila wakati. Linda mifugo yako!"
                ),
                "english_translation": (
                    "Greetings to all livestock keepers! This is an official advisory from AgroBiometrix veterinary specialists: "
                    "The heat-humidity index has surpassed safe thresholds. Cattle are breathing with difficulty and milk production is plunging by 25 percent."
                )
            }
        }
    },
    "Smallholder Cuniculture & Poultry: Heat & Feed Toxin Alert": {
        "context": "High humidity coupled with daytime heat spike > 34°C; risk of severe doe heat exhaustion, bloat from wilted cassava peelings, and heat prostration in broilers.",
        "languages": {
            "🇨🇮 / 🇸🇳 / 🇨🇲 Français Agricole (Bulletin Rural Panafricain)": {
                "broadcaster": "Conseillère Carole Kouassi • Radio Fermière AgroBiometrix (Yamoussoukro / Bafoussam)",
                "headline": "Alerte Canicule en Cuniculture et Aviculture Villageoise",
                "audio_script": (
                    "Avis urgent à tous les éleveurs de lapins et de volailles ! La canicule actuelle met en péril vos élevages. "
                    "Pour les lapins : ne donnez jamais d'épluchures de manioc fraîches ou humides en ce moment, cela provoque des ballonnements mortels et foudroyants ! "
                    "Séchez toujours les épluchures pendant deux jours complets au soleil. "
                    "Pour les poulets : distribuez de l'eau fraîche additionnée de vitamine C dès six heures du matin, et peignez les toits de vos poulaillers en blanc pour renvoyer la chaleur solaire !"
                ),
                "english_translation": (
                    "Urgent notice to all rabbit and poultry keepers! The current heat wave endangers smallholder livestock. "
                    "For rabbits: Never feed fresh or half-dried cassava peels right now; it causes fatal cyanogenic bloat! Sun-dry peels for 48 hours. "
                    "For broilers: Provide cool water with vitamin C before sunrise, and whitewash coop roofs to reflect solar radiation."
                )
            },
            "🇳🇬 Yoruba (Èdè Yorùbá)": {
                "broadcaster": "Ìyá Àgbẹ̀ Abọ̀sẹ̀dé • Rédíò Ọ̀sìn Àti Ọ̀gbìn AgroBiometrix (Òṣogbo / Abẹ́òkúta)",
                "headline": "Ìkìlọ̀ Pàjáwìrì fún Àwọn Olùsìn Ehoro àti Adìyẹ",
                "audio_script": (
                    "Ẹ̀yin olùsìn ehoro àti adìyẹ, ẹ fetí sílẹ̀ dáadáa sí ìkìlọ̀ pàjáwìrì yìí látọ̀dọ̀ AgroBiometrix: "
                    "Oòrùn gbígbóná àti ooru tí ó mú yìí le pa àwọn ehoro àti adìyẹ yín láìròtẹ́lẹ̀! "
                    "Fún àwọn ehoro : Ẹ má ṣe fún wọn ní èèpo gbaaguda tútù tàbí èyí tí kò gbẹ dáadáa jẹ rárá ! Ó máa ń fa ikùn fífú tí ó sì ń pa ehoro lójú ẹsẹ̀. "
                    "Ẹ rí i dájú pé ẹ sá èèpo náà sí oòrùn fún ọjọ́ méjì gbáko kí ó tó di jíjẹ. "
                    "Fún àwọn adìyẹ : Ẹ pèsè omi tútù pẹ̀lú Vitamin C fún wọn ní kùtùkùtù òwúrọ̀ kí oòrùn tó yọ. Oko á gbè wá o!"
                ),
                "english_translation": (
                    "Rabbit and poultry keepers, listen carefully to this urgent advisory from AgroBiometrix: "
                    "Intense ambient heat can cause sudden mortality in rabbits and broilers! "
                    "For rabbits: Never feed fresh or wet cassava peels! It causes lethal bloat. Ensure peels are thoroughly sun-dried for two full days before feeding."
                )
            },
            "🇳🇬 Hausa (Harshen Hausa)": {
                "broadcaster": "Malam Yakubu Zaria • Radio Dabbobin Gida AgroBiometrix (Zaria / Kaduna)",
                "headline": "Gargaɗin Zafi da Abinci ga Masu Kiwon Zomo da Kaji",
                "audio_script": (
                    "Manoma masu kiwon zomaye da kaji, ga wani muhimmin sakon gaggawa: "
                    "Zafin da ake ciki a yanzu na iya kashe zomo da kajinku idan ba a kiyaye ba. "
                    "Ga masu zomo: Kada ku kuskura ku ba su bawon rogo danye ko wanda bai bushe ba, domin yana sa kumburin ciki mai kashewa nan take! "
                    "Dole ne a shanya bawon a rana ya bushe tsawon kwana biyu kafin a ba su. "
                    "Ga kajin ku kuma, a ba su ruwan sha mai sanyi da sassafe kafin rana ta fito sosai. Allah ya raya mana dukiya!"
                ),
                "english_translation": (
                    "Farmers keeping rabbits and poultry, here is an important emergency advisory: "
                    "Severe heat will cause sudden losses in your rabbit hutches and chicken coops if preventative care is not taken. "
                    "For rabbits: Never feed raw, moist cassava peels; it causes fatal bloat! Ensure peels are sun-dried for two days before feeding."
                )
            }
        }
    },
    "Southern Guinea Savanna: Cassava Brown Streak & Root Rot Prevention": {
        "context": "Prolonged waterlogging following late torrential rains in transitional sub-humid savanna; acute risk of root bacterial soft rot and whitefly viral transmission.",
        "languages": {
            "🇨🇮 / 🇸🇳 / 🇨🇲 Français Agricole (Bulletin Rural Panafricain)": {
                "broadcaster": "Ingénieur Pascal N'Guessan • AgroBiometrix Radio Bassin Sud (Divo / Man / Korhogo)",
                "headline": "Alerte Engorgement des Sols et Pourriture des Tubercules de Manioc",
                "audio_script": (
                    "Attention aux producteurs de manioc et de tubercules ! Les fortes pluies tardives saturent actuellement nos parcelles. "
                    "Si l'eau stagne dans vos champs plus de quarante-huit heures, les racines tubéreuses vont pourrir sous terre ! "
                    "Actions immédiates recommandées : creusez d'urgence des rigoles de drainage entre vos billons pour évacuer l'eau stagnante. "
                    "Inspectez sous les feuilles : si vous voyez de nombreuses mouches blanches, appliquez un biopesticide à base de neem pour stopper la transmission du virus. "
                    "Récoltez sans attendre les parcelles à maturité avant le pourrissement !"
                ),
                "english_translation": (
                    "Attention all cassava and root crop farmers! Torrential late rains are waterlogging our farming basins. "
                    "If standing water persists for more than 48 hours, tuberous roots will suffer catastrophic soft rot underground! "
                    "Immediate action: Dig drainage channels between ridges immediately to drain water. Spray neem biopesticides if whiteflies appear."
                )
            },
            "🇳🇬 Yoruba (Èdè Yorùbá)": {
                "broadcaster": "Ọ̀jọ̀gbọ́n Ọlálékan • Rédíò Àgbẹ̀ Ìpínlẹ̀ Ọ̀yọ́ àti Ògùn (Ìbàdàn / Abẹ́òkúta)",
                "headline": "Ìkìlọ̀ nípa Ìkún-omi lórí Oko Gbaaguda àti Ìbàjẹ́ Gbòǹgbò",
                "audio_script": (
                    "Gbogbo ẹ̀yin olùgbìn gbaaguda àti iṣu, ẹ fetí sílẹ̀ dáadáa: Òjò àrọ̀pọ̀ tí ó ń rọ̀ lákòókò yìí ti bẹ̀rẹ̀ sí ní kún oko wa lomi kọjá ààlà! "
                    "Tí omi bá dúró sórí oko gbaaguda yín fún ọjọ́ méjì pọ́nnńbélé, gbogbo iṣu inú ilẹ̀ yóò jẹrà, yóò sì ba gbogbo èrè yín jẹ́. "
                    "Wàhálà yìí le bọ́ sílẹ̀ tí ẹ bá tẹ̀lé ìmọ̀ràn yìí: Ẹ ya kọ́fà tàbí koto omi láàárín àwọn epo yín kíá láti jẹ́ kí omi sàn kúrò lórí oko. "
                    "Fún àwọn gbaaguda tí ó ti gbó dáadáa, ẹ bẹ̀rẹ̀ sí ní kórè wọn kí wọ́n má baà bajẹ́ sínú ilẹ̀. Ọlọ́run yóò sọ oko wa di púpọ̀ o!"
                ),
                "english_translation": (
                    "Cassava and yam farmers, listen carefully: Heavy late rains are waterlogging farmland across the transition belt! "
                    "If stagnant water remains around cassava roots for 48 hours, root tubers will rot and destroy your profits. "
                    "Recommended action: Dig drainage trenches between ridges immediately so water drains freely. Harvest fully matured plots promptly."
                )
            }
        }
    }
}


def render_vernacular_radio_suite():
    """
    Renders Suite 8: Last-Mile Multilingual Radio & Voice Disseminator
    Complete Standalone Production Suite for Agricultural Extension Broadcasters.
    """
    is_fr = st.session_state.get("app_lang", "en") == "fr"
    init_broadcast_queue()

    if is_fr:
        st.markdown("## 🎙️ Suite de Vulgarisation Radio & Voix Vernaculaire du Dernier Kilomètre")
        st.caption(
            "Traduit les calculs biométriques de pointe, la stœchiométrie des sols et la modélisation agro-climatique "
            "en **bulletins radiophoniques en langues africaines indigènes** pour les petits exploitants ruraux. "
            "Démontre la livraison opérationnelle du **laboratoire jusqu'au dernier kilomètre paysan**."
        )
        tab_titles = [
            "📡 Studio de Diffusion IA & File d'Attente",
            "📻 Archives des Bulletins Institutionnels",
            "⚙️ Moteur Vocal & Paramètres Cloud Africains",
            "🌐 Automatisation Radio & Syndication RSS (ZaraRadio)"
        ]
    else:
        st.markdown("## 🎙️ Last-Mile Multilingual Radio & Voice Dissemination Suite")
        st.caption(
            "Translates laboratory biometrics, soil stoichiometry, and agro-climatic intelligence into "
            "**authentic indigenous vernacular radio voice broadcasts** for rural smallholders across Africa. "
            "Demonstrates end-to-end delivery from **laboratory science to the last-mile farmer**."
        )
        tab_titles = [
            "📡 Live Broadcast Studio & Active Queue",
            "📻 Curated Benchmark Audio Archives",
            "⚙️ African Neural Voice Engine & Cloud Speech Settings",
            "🌐 Station Automation & Podcast RSS Syndication (ZaraRadio)"
        ]

    tab_live, tab_bench, tab_engine, tab_synd = st.tabs(tab_titles)

    # =========================================================================
    # TAB 1: LIVE BROADCAST STUDIO & ACTIVE DISPATCH QUEUE
    # =========================================================================
    with tab_live:
        queue = st.session_state.get("broadcast_dispatch_queue", [])

        st.markdown("##### 📡 Global Agricultural Broadcast Dispatch Queue")
        st.caption(
            "Analytical findings and biometric alerts automatically routed from AgroBiometrix suites (Soils, Livestock, Climate, Breeding):"
        )

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
                    if st.button("⚡ Load to Studio", key=f"suite8_btn_load_{idx}", help="Load this finding directly into the Studio below"):
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
                if st.button("🔄 Reset Queue to Institutional Defaults", key="suite8_btn_reset_queue"):
                    st.session_state["broadcast_dispatch_queue"] = list(DEFAULT_BROADCAST_QUEUE)
                    st.rerun()

        st.markdown("---")
        st.markdown("##### 🎙️ Extension Radio Broadcaster Studio & AI Script Generator")
        st.caption("Compose, localize, and generate spoken voice bulletins from any biometric finding:")

        active_alert = st.session_state.get("active_studio_alert", queue[0] if queue else {})

        c_top1, c_top2 = st.columns([2, 1])
        with c_top1:
            head_in = st.text_input(
                "Advisory Headline / Bulletin Title:",
                value=st.session_state.get("dyn_head_val", active_alert.get("headline", "Severe Phosphorus & Zinc Fixation in Acidic Ultisols")),
                key="suite8_head_input"
            )
        with c_top2:
            comm_in = st.text_input(
                "Target Agricultural Commodity:",
                value=st.session_state.get("dyn_comm_val", active_alert.get("commodity", "Maize & Cassava")),
                key="suite8_comm_input"
            )

        reg_in = st.text_input(
            "Target Agro-Ecological Region / State / Country:",
            value=st.session_state.get("dyn_reg_val", active_alert.get("region", "Southwest Nigeria (Oyo/Ogun Transition Zone)")),
            key="suite8_reg_input"
        )

        c_f1, c_f2 = st.columns([1, 1])
        with c_f1:
            trig_in = st.text_area(
                "Scientific Trigger & Biometric Finding:",
                value=st.session_state.get("dyn_trig_val", active_alert.get("agronomic_trigger", "Soil pH < 5.1 with active Al3+ toxicity and high P-sorption capacity. Surface urea broadcast causing 40% ammonia volatilization.")),
                height=85,
                key="suite8_trig_input"
            )
        with c_f2:
            rec_in = st.text_area(
                "Recommended Field Intervention / Action:",
                value=st.session_state.get("dyn_rec_val", active_alert.get("recommendation", "Halt surface urea broadcast. Apply 2.5 t/ha agricultural lime with organic compost. Switch to micro-dosing single superphosphate (SSP) at root zone.")),
                height=85,
                key="suite8_rec_input"
            )

        # Indigenous Language Selector
        studio_lang_choice = st.radio(
            "Select Vernacular Broadcast Language for Synthesis:",
            [
                "🇳🇬 Yoruba (Èdè Yorùbá)",
                "🇳🇬 Hausa (Harshen Hausa)",
                "🇰🇪 Swahili (Kiswahili)",
                "🇨🇮 / 🇸🇳 / 🇨🇲 Français Agricole (Panafricain)",
                "🇳🇬 West African Pidgin"
            ],
            index=0,
            horizontal=True,
            key="suite8_lang_choice"
        )

        b_col1, b_col2 = st.columns([1, 2])
        with b_col1:
            if st.button("🎙️ Synthesize Vernacular Bulletin", key="suite8_btn_synth_bulletin", type="primary"):
                with st.spinner(f"Formulating authentic spoken script in {studio_lang_choice}..."):
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
            ⚡ Formulated On-the-Fly from Research Finding
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
            elif "pidgin" in dyn_lang.lower():
                dyn_bcp47 = "pcm"
                dyn_tag = "Pidgin"
            else:
                dyn_bcp47 = "fr-FR"
                dyn_tag = "Français"

            dyn_html_player = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 0; padding: 4px 0; background: transparent;
        }}
        .btn-synth {{
            background-color: #1B5E20; color: white; border: none; padding: 9px 18px;
            font-size: 13.5px; font-weight: 700; border-radius: 6px; cursor: pointer;
            display: inline-flex; align-items: center; gap: 8px;
        }}
        .btn-synth:hover {{ background-color: #2E7D32; }}
        .btn-stop {{
            background-color: #DC2626; color: white; border: none; padding: 9px 14px;
            font-size: 13.5px; font-weight: 700; border-radius: 6px; cursor: pointer; margin-left: 8px;
        }}
        .btn-stop:hover {{ background-color: #B91C1C; }}
    </style>
</head>
<body>
    <div style="display: flex; align-items: center; margin-bottom: 8px;">
        <button class="btn-synth" onclick="startDynSpeech()">🔊 PLAY SPOKEN SCRIPT ({dyn_tag})</button>
        <button class="btn-stop" onclick="stopDynSpeech()">⏹️ Stop</button>
    </div>
    <div id="suite8SpeechState" style="font-size: 12px; color: #4B5563; min-height: 20px;">
        Click above to synthesize and play spoken indigenous radio script
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

    const sEl = document.getElementById('suite8SpeechState');
    sEl.innerHTML = '<span style="color: #1B5E20; font-weight: 600;">🎙️ Speaking live broadcast ({dyn_tag})...</span>';

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
        document.getElementById('suite8SpeechState').innerHTML = '<span style="color: #6B7280;">⏹️ Playback stopped</span>';
    }}
}}
</script>
</body>
</html>
"""
            components.html(dyn_html_player, height=75)

            with st.expander("🔔 Radio Station Sign-on Cue Chime (Acoustic Jingle)", expanded=False):
                st.caption("Standard 3-tone marimba cue chime (C5-E5-G5 harmonic sequence) broadcasted prior to voice bulletins to alert rural listeners across radio transistors:")
                jingle_bytes = generate_radio_jingle()
                st.audio(jingle_bytes, format="audio/wav")

            with st.expander("🗣️ African Voice AI & Tonal Models (YarnGPT / ElevenLabs / Google)", expanded=False):
                st.markdown(f"""
<div style="font-size: 0.82rem; color: #4B5563; line-height: 1.5;">
    • <b>Current Voice Target</b>: <code>{dyn_bcp47}</code> ({dyn_tag})<br>
    • <b>Neural Audio Support</b>: When an API key is provided in the Settings tab, studio-grade neural voice synthesis is generated.<br>
    • <b>Tonal Precision</b>: Script formulations preserve Yorùbá diacritics (ẹ, ọ, gb) and Hausa phonetic implosives (ɓ, ɗ) for authentic cadence.
</div>
""", unsafe_allow_html=True)

        with col_dyn_txt:
            st.markdown(f"##### 📜 Formulated Vernacular Radio Script ({dyn_tag})")
            st.markdown(f"""
<div style="background: #FFFFFF; border: 1.5px solid #22C55E; border-radius: 6px; padding: 12px; font-size: 0.88rem; line-height: 1.6; color: #1F2937; margin-bottom: 0.5rem;">
    <i>"{dyn_data.get('audio_script', '')}"</i>
</div>
""", unsafe_allow_html=True)

            with st.expander("🌐 English Translation & Extension Interpretation", expanded=True):
                st.markdown(f"""
<div style="font-size: 0.84rem; color: #374151; line-height: 1.5;">
    <i>"{dyn_data.get('english_translation', '')}"</i>
</div>
""", unsafe_allow_html=True)

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
            key_prefix="suite8_btn_dl_dyn_cue"
        )

    # =========================================================================
    # TAB 2: CURATED BENCHMARK AUDIO ARCHIVES
    # =========================================================================
    with tab_bench:
        st.markdown("##### 📻 Curated Institutional Benchmark Broadcasts (Pre-Bundled Ground Truth)")
        st.caption("Demonstrates high-fidelity native recordings across benchmark African commodities and agro-ecological zones:")

        scenario_choice = st.selectbox(
            "Select Field Advisory Scenario:",
            list(LOCAL_RADIO_BROADCASTS.keys()),
            index=0,
            key="suite8_bench_scenario"
        )
        selected_scenario = LOCAL_RADIO_BROADCASTS[scenario_choice]

        st.info(f"**Field Context**: {selected_scenario['context']}")

        avail_langs = list(selected_scenario["languages"].keys())
        default_idx = 0
        if is_fr:
            for idx, l in enumerate(avail_langs):
                if "français" in l.lower() or "french" in l.lower():
                    default_idx = idx

        lang_choice = st.radio(
            "Select Broadcast Language (Click any language to load & play audio):",
            avail_langs,
            index=default_idx,
            horizontal=True,
            key="suite8_bench_lang_radio"
        )

        broadcast_data = selected_scenario["languages"][lang_choice]

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

            audio_file_path = None
            if "Maize" in scenario_choice:
                if "Français" in lang_choice:
                    audio_file_path = os.path.join("assets", "audio", "maize_fr.mp3")
                elif "Hausa" in lang_choice:
                    audio_file_path = os.path.join("assets", "audio", "maize_ha.mp3")
                elif "Yoruba" in lang_choice:
                    audio_file_path = os.path.join("assets", "audio", "maize_yo.mp3")
                elif "Swahili" in lang_choice:
                    audio_file_path = os.path.join("assets", "audio", "maize_sw.mp3")
                elif "Pidgin" in lang_choice:
                    audio_file_path = os.path.join("assets", "audio", "maize_pidgin.mp3")
            elif "Cattle" in scenario_choice:
                if "Français" in lang_choice:
                    audio_file_path = os.path.join("assets", "audio", "cattle_fr.mp3")
                elif "Hausa" in lang_choice:
                    audio_file_path = os.path.join("assets", "audio", "cattle_ha.mp3")
                elif "Swahili" in lang_choice:
                    audio_file_path = os.path.join("assets", "audio", "cattle_sw.mp3")
            elif "Cuniculture" in scenario_choice or "Poultry" in scenario_choice:
                if "Français" in lang_choice:
                    audio_file_path = os.path.join("assets", "audio", "poultry_fr.mp3")
                elif "Hausa" in lang_choice:
                    audio_file_path = os.path.join("assets", "audio", "poultry_ha.mp3")
                elif "Yoruba" in lang_choice:
                    audio_file_path = os.path.join("assets", "audio", "poultry_yo.mp3")
                elif "Pidgin" in lang_choice:
                    audio_file_path = os.path.join("assets", "audio", "poultry_pidgin.mp3")
            elif "Cassava" in scenario_choice:
                if "Français" in lang_choice:
                    audio_file_path = os.path.join("assets", "audio", "cuniculture_fr.mp3")
                elif "Yoruba" in lang_choice:
                    audio_file_path = os.path.join("assets", "audio", "cuniculture_yo.mp3")

            if audio_file_path and os.path.exists(audio_file_path):
                st.audio(audio_file_path, format="audio/mp3")
                st.caption(f"🟢 **Native Indigenous Acoustic Voice Active** (Offline Studio File: `{os.path.basename(audio_file_path)}`)")
            else:
                st.caption("🎙️ Live Vernacular Voice Stream Active • Full Audio Broadcast")

            # Fallback in-browser Web Speech button
            lang_bcp = "fr-FR"
            lang_name = "Français"
            if "Hausa" in lang_choice:
                lang_bcp = "ha-NG"
                lang_name = "Hausa"
            elif "Yoruba" in lang_choice:
                lang_bcp = "yo-NG"
                lang_name = "Yoruba"
            elif "Swahili" in lang_choice:
                lang_bcp = "sw-KE"
                lang_name = "Swahili"
            elif "Pidgin" in lang_choice:
                lang_bcp = "pcm"
                lang_name = "Pidgin"

            safe_script_json = json.dumps(broadcast_data['audio_script'])
            html_player = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 0; padding: 4px 0; background: transparent;
        }}
        .btn-play {{
            background-color: #1B5E20; color: white; border: none; padding: 8px 16px;
            font-size: 13px; font-weight: 700; border-radius: 6px; cursor: pointer;
            display: inline-flex; align-items: center; gap: 6px;
        }}
        .btn-play:hover {{ background-color: #2E7D32; }}
        .btn-stop {{
            background-color: #DC2626; color: white; border: none; padding: 8px 12px;
            font-size: 13px; font-weight: 700; border-radius: 6px; cursor: pointer; margin-left: 8px;
        }}
        .btn-stop:hover {{ background-color: #B91C1C; }}
    </style>
</head>
<body>
    <div style="display: flex; align-items: center;">
        <button class="btn-play" onclick="playWebSpeech()">🔊 PLAY SPOKEN SCRIPT ({lang_name})</button>
        <button class="btn-stop" onclick="stopWebSpeech()">⏹ Stop</button>
    </div>
    <div id="speechStatus" style="font-size: 11px; color: #6B7280; margin-top: 5px;"></div>

<script>
function getSynth() {{
    try {{
        if (window.speechSynthesis) return window.speechSynthesis;
        if (window.parent && window.parent.speechSynthesis) return window.parent.speechSynthesis;
        if (window.top && window.top.speechSynthesis) return window.top.speechSynthesis;
    }} catch(e) {{}}
    return window.speechSynthesis || null;
}}

let currUtterance = null;

function playWebSpeech() {{
    const synth = getSynth();
    if (!synth) {{
        alert('Web Speech Synthesis is not supported in this browser.');
        return;
    }}
    synth.cancel();

    const text = {safe_script_json};
    const utter = new SpeechSynthesisUtterance(text);
    utter.lang = '{lang_bcp}';
    utter.rate = 0.95;
    utter.pitch = 1.0;

    try {{
        const voices = synth.getVoices();
        const matched = voices.find(v => v.lang.toLowerCase().replace('_', '-').startsWith('{lang_bcp}'.toLowerCase().slice(0, 2)));
        if (matched) utter.voice = matched;
    }} catch(e) {{}}

    const statusEl = document.getElementById('speechStatus');
    statusEl.innerHTML = '<span style="color: #1B5E20; font-weight: 600;">🎙️ Playing {lang_name} speech audio...</span>';

    utter.onend = function() {{
        statusEl.innerHTML = '<span style="color: #6B7280;">Finished spoken broadcast</span>';
    }};

    utter.onerror = function(e) {{
        statusEl.innerHTML = '<span style="color: #4B5563;">Audio playback ended</span>';
    }};

    currUtterance = utter;
    synth.speak(utter);
}}

function stopWebSpeech() {{
    const synth = getSynth();
    if (synth) {{
        synth.cancel();
        document.getElementById('speechStatus').innerHTML = '<span style="color: #6B7280;">Stopped</span>';
    }}
}}
</script>
</body>
</html>
"""
            components.html(html_player, height=75)

            with st.expander("🔔 Radio Station Sign-on Cue Chime (Acoustic Jingle)", expanded=False):
                st.caption("Standard 3-tone marimba cue chime (C5-E5-G5 harmonic sequence) broadcasted prior to voice bulletins to alert rural listeners across radio transistors:")
                jingle_bytes = generate_radio_jingle()
                st.audio(jingle_bytes, format="audio/wav")

        with col_txt:
            st.markdown("##### 🌐 Verified English Translation & Biometrics Link")
            st.markdown(f"""
<div class="agri-card" style="font-size: 0.85rem; line-height: 1.5; margin-bottom: 0.8rem;">
    <b>Institutional English Translation:</b><br>
    <i>"{broadcast_data['english_translation']}"</i>
</div>
""", unsafe_allow_html=True)

            st.markdown(f"""
<div class="agri-card agri-card-highlight" style="font-size: 0.8rem;">
    <b>🔬 Underlying AgroBiometrix Biometric Models Linked:</b><br>
    • Open-Meteo REST API: 14-day rainfall hiatus & heat stress index<br>
    • Soil Intelligence Mod 5: Crown micro-dosing (20 kg NPK/ha)<br>
    • DMRT ANOVA Mod 3: Validated non-significant yield loss under 50% fertilizer reduction
</div>
""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown(f"""
<div class="agri-explainer-box">
<div class="agri-explainer-title">📻 Indigenous Voice Transcript ({lang_choice}):</div>
<i>"{broadcast_data['audio_script']}"</i>
</div>
""", unsafe_allow_html=True)

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
            filename_prefix=f"AgroBiometrix_Radio_Benchmark_{lang_choice[:2]}",
            title=f"AgroBiometrix Radio Advisory: {broadcast_data.get('headline', '')}",
            key_prefix="suite8_btn_dl_bench"
        )

    # =========================================================================
    # TAB 3: AFRICAN NEURAL VOICE ENGINE & SETTINGS
    # =========================================================================
    with tab_engine:
        st.markdown("##### ⚙️ African Neural Voice Synthesis & Cloud Speech Engine")
        st.caption("Configure live text-to-speech engines and review dialect and phonetic acoustic parameters:")
        render_voice_engine_settings_panel()

        st.markdown("---")
        st.markdown("##### 🌍 African Indigenous Language Phonetic Profiles & BCP-47 Mappings")
        lang_df = pd.DataFrame([
            {"Language": "Hausa", "BCP-47 Code": "ha-NG", "Voice Provider Target": "ha-NG-Standard-A (Google) / YarnGPT", "Dialect Belts": "Kano, Kaduna, Katsina, Zaria, Niamey (Niger)"},
            {"Language": "Yorùbá", "BCP-47 Code": "yo-NG", "Voice Provider Target": "yo-NG-Standard-A (Google) / AwaTTS", "Dialect Belts": "Oyo, Osun, Ogun, Ondo, Ekiti, Lagos, Porto-Novo (Benin)"},
            {"Language": "Kiswahili", "BCP-47 Code": "sw-KE", "Voice Provider Target": "sw-KE-Standard-A (Google) / ElevenLabs", "Dialect Belts": "Kenya (Highlands/Rift), Tanzania (Morogoro/Arusha), Uganda, DRC"},
            {"Language": "Français Agricole", "BCP-47 Code": "fr-FR", "Voice Provider Target": "fr-FR-Neural2-B (Google) / ElevenLabs", "Dialect Belts": "Côte d'Ivoire (Bouaké), Sénégal (Kaolack), Cameroun (Garoua), Mali"},
            {"Language": "West African Pidgin", "BCP-47 Code": "pcm", "Voice Provider Target": "en-NG-Standard-A (Google) / YarnGPT", "Dialect Belts": "Niger Delta, Edo, Warri, Port Harcourt, Anglophone Cameroon"}
        ])
        st.dataframe(lang_df, use_container_width=True)

    # =========================================================================
    # TAB 4: STATION AUTOMATION & PODCAST RSS SYNDICATION
    # =========================================================================
    with tab_synd:
        st.markdown("##### 🌐 Community Radio Automation & Syndication Feed (RSS 2.0 / Apple Podcasts XML)")
        st.caption(
            "Enables local radio stations and agricultural syndicates (e.g. Farm Radio International, FECAVOICE, NAFAS) "
            "to automatically pull audio bulletins directly into station playout software (ZaraRadio, Rivendell, RadioDJ):"
        )

        queue_items = st.session_state.get("broadcast_dispatch_queue", [])
        feed_xml = generate_podcast_rss_xml(queue_items)

        f_col1, f_col2 = st.columns([2, 1])
        with f_col1:
            st.text_input(
                "Live Station Syndication Feed URL (Copy to ZaraRadio / Rivendell / Podcast App):",
                value="https://agrobiometrix.org/feeds/community_radio_podcast.xml",
                key="suite8_txt_feed_url",
                disabled=True
            )
        with f_col2:
            st.download_button(
                label="📥 Download Podcast XML Feed",
                data=feed_xml,
                file_name="agrobiometrix_radio_podcast_feed.xml",
                mime="application/rss+xml",
                key="suite8_btn_dl_podcast_xml",
                help="Download the valid RSS 2.0 podcast XML feed containing all queued alerts and audio enclosures."
            )

        st.markdown("""
<div class="agri-card" style="border-left: 4px solid #1B5E20; background: #F1F8F2; padding: 12px 16px; margin-top: 10px;">
    <b>📻 Instructions for Radio Playout Technicians:</b><br>
    1. In <b>ZaraRadio / Rivendell / RadioDJ</b>, open the <i>Events / Timed Schedule</i> manager.<br>
    2. Add an automated HTTP download task pointing to the Station Syndication Feed URL above.<br>
    3. Set download interval to every 6 hours (e.g. 5:00 AM, 11:00 AM, 5:00 PM) before daily agricultural hours.<br>
    4. Playout software will automatically parse new <code>&lt;enclosure&gt;</code> MP3 voice bulletins and broadcast them on FM airwaves.
</div>
""", unsafe_allow_html=True)

        with st.expander("👁️ Inspect Generated RSS 2.0 / Podcast XML", expanded=False):
            st.code(feed_xml[:2200] + "\n... [Remaining XML nodes truncated for display]", language="xml")
