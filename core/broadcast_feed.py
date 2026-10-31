"""
AgroBiometrix - Automated Agricultural Radio RSS 2.0 & Podcast Syndication Feed
Converts all live dynamic biometric dispatches and curated ground-truth bulletins
into an official, RFC-compliant RSS 2.0 Podcast XML feed for community radio automation software
(ZaraRadio, Rivendell, RadioDJ, StationPlaylist, and mobile podcast clients).
"""

import datetime
import xml.sax.saxutils as saxutils
from typing import List, Dict, Any


def generate_podcast_rss_xml(
    dispatches: List[Dict[str, Any]],
    station_title: str = "AgroBiometrix Last-Mile Community Radio Network",
    station_link: str = "https://agrobiometrix.org/radio",
    base_audio_url: str = "https://agrobiometrix.org/assets/audio"
) -> str:
    """
    Builds a standards-compliant RSS 2.0 Podcast XML feed.
    Compatible with:
    - Terrestrial FM Station Playout Software (ZaraRadio, Rivendell, RadioDJ)
    - Podcast Catchers & Feed Readers (Apple Podcasts, AntennaPod, VLC)
    - Telecom IVR Audio Servers
    """
    now_rfc = datetime.datetime.now(datetime.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
    
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:content="http://purl.org/rss/1.0/modules/content/">',
        '  <channel>',
        f'    <title>{saxutils.escape(station_title)}</title>',
        f'    <link>{saxutils.escape(station_link)}</link>',
        '    <description>Authentic indigenous vernacular agricultural bulletins and climate biometrics for smallholders across Sub-Saharan Africa in Yorùbá, Hausa, Kiswahili, Français Agricole, and West African Pidgin.</description>',
        '    <language>mul</language>',
        f'    <lastBuildDate>{now_rfc}</lastBuildDate>',
        f'    <pubDate>{now_rfc}</pubDate>',
        '    <docs>https://www.rssboard.org/rss-specification</docs>',
        '    <generator>AgroBiometrix Scientific Consortium v2.4</generator>',
        '    <managingEditor>broadcast@agrobiometrix.org (AgroBiometrix Extension Dispatch)</managingEditor>',
        '    <webMaster>tech@agrobiometrix.org (AgroBiometrix Engineering)</webMaster>',
        '    <itunes:author>AgroBiometrix Science Hub</itunes:author>',
        '    <itunes:summary>Multilingual vernacular agricultural extension advisories grounded in laboratory biometrics.</itunes:summary>',
        '    <itunes:category text="Science">',
        '      <itunes:category text="Life Sciences"/>',
        '    </itunes:category>',
        '    <itunes:category text="News">',
        '      <itunes:category text="Daily News"/>',
        '    </itunes:category>',
        '    <itunes:explicit>no</itunes:explicit>',
    ]

    for item in dispatches:
        item_id = item.get("id", f"DISP-{hash(str(item))}")
        headline = item.get("headline", "Agricultural Advisory")
        commodity = item.get("commodity", "Mixed Agriculture")
        region = item.get("region", "Sub-Saharan Africa")
        trigger = item.get("agronomic_trigger", "")
        recommendation = item.get("recommendation", "")
        module = item.get("source_module", "AgroBiometrix Analytical Engine")
        
        # Audio file link
        audio_filename = item.get("audio_file", "maize_ha.mp3")
        enclosure_url = f"{base_audio_url}/{audio_filename}"
        
        # Detailed HTML description for podcast catchers and radio cueing
        desc_html = f"""
<![CDATA[
<p><strong>[AgroBiometrix Last-Mile Extension Broadcast]</strong></p>
<p><strong>Target Commodity:</strong> {commodity} | <strong>Agro-Ecological Region:</strong> {region}</p>
<p><strong>Source Biometrics:</strong> {module}</p>
<p><strong>Agronomic Trigger:</strong> {trigger}</p>
<p><strong>Recommended Action:</strong> {recommendation}</p>
<hr/>
<p><em>Broadcasted by AgroBiometrix Consortium for community radio stations, agricultural extension agents, and rural listening cooperatives.</em></p>
]]>
""".strip()

        xml_lines.extend([
            '    <item>',
            f'      <title>{saxutils.escape(f"[{commodity} - {region}] {headline}")}</title>',
            f'      <description>{desc_html}</description>',
            f'      <link>{saxutils.escape(station_link)}</link>',
            f'      <guid isPermaLink="false">{saxutils.escape(item_id)}</guid>',
            f'      <pubDate>{now_rfc}</pubDate>',
            f'      <enclosure url="{saxutils.escape(enclosure_url)}" length="1048576" type="audio/mpeg"/>',
            '      <itunes:duration>00:00:50</itunes:duration>',
            '      <itunes:explicit>no</itunes:explicit>',
            '    </item>'
        ])

    xml_lines.extend([
        '  </channel>',
        '</rss>'
    ])

    return "\n".join(xml_lines)
