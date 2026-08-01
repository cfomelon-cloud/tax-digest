#!/usr/bin/env python3
"""Regenerate index.html from data/manifest.json.

Run after adding a new digest entry to data/manifest.json.
Manifest is a JSON array of {date, file, headline, blurb} objects; optional
headline_zh / blurb_zh add a Traditional-Chinese version for the language toggle
(falls back to the English text when absent). Newest date first. Stdlib only.
"""
import json
import html
import os
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(ROOT, "data", "manifest.json")
OUT = os.path.join(ROOT, "index.html")


def fmt_date(d: str) -> str:
    try:
        return datetime.strptime(d, "%Y-%m-%d").strftime("%A %d %B %Y")
    except ValueError:
        return d


def bi(en_text: str, zh_text: str) -> str:
    """Inline bilingual span pair."""
    return ('<span class="en">{}</span><span class="zh" lang="zh-Hant">{}</span>'
            .format(en_text, zh_text))


def main() -> None:
    with open(MANIFEST, "r", encoding="utf-8") as fh:
        entries = json.load(fh)
    entries.sort(key=lambda e: e.get("date", ""), reverse=True)

    cards = []
    for e in entries:
        en_h = html.escape(e.get("headline", ""))
        zh_h = html.escape(e.get("headline_zh") or e.get("headline", ""))
        en_b = html.escape(e.get("blurb", ""))
        zh_b = html.escape(e.get("blurb_zh") or e.get("blurb", ""))
        cards.append(
            """      <a class="card-link" href="{file}" style="text-decoration:none;color:inherit">
        <div class="card">
          <div class="date">{date_h}</div>
          <h3>{headline}</h3>
          <p>{blurb}</p>
          <span class="read">{read}</span>
        </div>
      </a>""".format(
                file=html.escape(e.get("file", "#")),
                date_h=html.escape(fmt_date(e.get("date", ""))),
                headline=bi(en_h, zh_h),
                blurb=bi(en_b, zh_b),
                read=bi("Read edition &rarr;", "閱讀日報 &rarr;"),
            )
        )

    updated = fmt_date(entries[0]["date"]) if entries else ""

    page = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Private Client Tax Digest</title>
<script>try{{if(localStorage.getItem('pctd-lang')==='zh')document.documentElement.classList.add('lang-zh');}}catch(e){{}}</script>
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="site"><div class="wrap"><div class="toprow">
<div><h1>Private Client Tax Digest</h1>
<p class="en">Cross-border tax updates for high-net-worth individuals, families &amp; their advisers</p>
<p class="zh" lang="zh-Hant">為高淨值人士、家族及其顧問提供的跨境稅務資訊</p>
<div class="meta">{meta}</div></div>
<div class="ctrls"><button id="ttsbtn" class="lang-btn" onclick="readAloud()">🔊 Read</button><button id="langtoggle" class="lang-btn" onclick="toggleLang()">繁中</button></div>
</div></div></header>

<main><div class="wrap">
<div class="legend en">A blended daily brief: every reputable cross-border private-client tax article and commentary published in the last ~24 hours (English and Chinese). Items tagged <span class="tag c">Confirmed</span> (legislated / announced), <span class="tag r">Reported</span> (briefed / under consultation), <span class="tag a">Analyst-option</span> (advocated, not policy). Not tax advice.</div>
<div class="legend zh" lang="zh-Hant">綜合每日簡報：收錄過去約24小時內所有可靠的跨境私人客戶稅務新聞與評論（中英文）。標籤：<span class="tag c">已確認</span>（已立法／公告）、<span class="tag r">已披露</span>（諮詢中）、<span class="tag a">分析觀點</span>（非官方政策）。本文非稅務意見。</div>

<h2 style="font-size:17px;margin:22px 0 6px">{trackers_h}</h2>
<p style="font-size:13.5px;color:#5b6472;margin:0 0 8px">{trackers_sub}</p>
<a class="card-link" href="trackers/elborne.html" style="text-decoration:none;color:inherit"><div class="card"><div class="date">{el_tag}</div><h3>{el_h}</h3><p>{el_b}</p><span class="read">{open_t}</span></div></a>
<a class="card-link" href="trackers/china-offshore-trusts.html" style="text-decoration:none;color:inherit"><div class="card"><div class="date">{cn_tag}</div><h3>{cn_h}</h3><p>{cn_b}</p><span class="read">{open_t}</span></div></a>

<h2 style="font-size:17px;margin:22px 0 6px">{editions_h}</h2>

{cards}

</div></main>

<footer class="site"><div class="wrap">Private Client Tax Digest · {foot}</div></footer>
<script src="app.js"></script>
</body>
</html>
""".format(
        updated=html.escape(updated),
        meta=bi("Priority: UK &middot; US &middot; China &middot; Hong Kong &middot; Singapore &nbsp;|&nbsp; Secondary: Italy &middot; Portugal &middot; Australia &middot; Canada &middot; Taiwan &nbsp;|&nbsp; Updated " + html.escape(updated),
                "重點：英國 &middot; 美國 &middot; 中國 &middot; 香港 &middot; 新加坡 &nbsp;|&nbsp; 次要：義大利 &middot; 葡萄牙 &middot; 澳洲 &middot; 加拿大 &middot; 台灣 &nbsp;|&nbsp; 更新於 " + html.escape(updated)),
        trackers_h=bi("Story trackers", "專題追蹤"),
        trackers_sub=bi("Living roundups that pull together all verified commentary on a major development as firm alerts roll in.",
                        "彙整某一重大議題所有已核實評論的持續更新頁，隨事務所快訊陸續補充。"),
        el_tag=bi("UK · Inheritance tax", "英國 · 遺產稅"),
        el_h=bi("Elborne v HMRC — home-loan IHT scheme upheld", "Elborne 訴 HMRC — 房貸型遺產稅架構獲上訴法院支持"),
        el_b=bi("Court of Appeal (13 Jul) commentary tracker: ICLG, Paris Smith, Professional Adviser, RPC and more; marquee-firm briefings pending.",
                "上訴法院（7月13日）評論追蹤：ICLG、Paris Smith、Professional Adviser、RPC 等；大型事務所簡報待發布。"),
        cn_tag=bi("China · Trusts", "中國 · 信託"),
        cn_h=bi("China offshore-trust income tax (Announcement 2026 No. 21)", "中國離岸信託個人所得稅（2026年第21號公告）"),
        cn_b=bi("24 Jul announcement tracker: official/primary sources and the first firm alerts.",
                "7月24日公告追蹤：官方／第一手來源，及首批事務所快訊。"),
        open_t=bi("Open tracker &rarr;", "開啟追蹤 &rarr;"),
        editions_h=bi("Daily editions", "每日日報"),
        foot=bi("updated daily · built automatically", "每日更新 · 自動產生"),
        cards="\n".join(cards),
    )

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(page)
    print("Wrote {} with {} edition(s).".format(OUT, len(entries)))


if __name__ == "__main__":
    main()
