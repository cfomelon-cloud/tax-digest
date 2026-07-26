#!/usr/bin/env python3
"""Regenerate index.html from data/manifest.json.

Run this after adding a new digest entry to data/manifest.json.
The manifest is a JSON array of objects: {date, file, headline, blurb}.
Newest date is shown first. No external dependencies (standard library only).
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


def main() -> None:
    with open(MANIFEST, "r", encoding="utf-8") as fh:
        entries = json.load(fh)
    entries.sort(key=lambda e: e.get("date", ""), reverse=True)

    cards = []
    for e in entries:
        cards.append(
            """      <a class="card-link" href="{file}" style="text-decoration:none;color:inherit">
        <div class="card">
          <div class="date">{date_h}</div>
          <h3>{headline}</h3>
          <p>{blurb}</p>
          <span class="read">Read edition &rarr;</span>
        </div>
      </a>""".format(
                file=html.escape(e.get("file", "#")),
                date_h=html.escape(fmt_date(e.get("date", ""))),
                headline=html.escape(e.get("headline", "")),
                blurb=html.escape(e.get("blurb", "")),
            )
        )

    updated = fmt_date(entries[0]["date"]) if entries else ""

    page = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Private Client Tax Digest</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="site"><div class="wrap">
<h1>Private Client Tax Digest</h1>
<p>Cross-border tax updates for high-net-worth individuals, families &amp; their advisers</p>
<div class="meta">Priority: UK &middot; US &middot; China &middot; Hong Kong &middot; Singapore &nbsp;|&nbsp; Secondary: Italy &middot; Portugal &middot; Australia &middot; Canada &middot; Taiwan &nbsp;|&nbsp; Updated {updated}</div>
</div></header>

<main><div class="wrap">
<div class="legend">
A blended daily brief: the day's genuinely new cross-border moves, a short block for each priority jurisdiction, and the secondary five surfaced when material. Items tagged <span class="tag c">Confirmed</span> (legislated / announced), <span class="tag r">Reported</span> (briefed / under consultation), <span class="tag a">Analyst-option</span> (advocated, not policy). Not tax advice.
</div>

<h2 style="font-size:17px;margin:22px 0 6px">Story trackers</h2>
<p style="font-size:13.5px;color:#5b6472;margin:0 0 8px">Living roundups that pull together all verified commentary on a major development as firm alerts roll in.</p>
<a class="card-link" href="trackers/elborne.html" style="text-decoration:none;color:inherit"><div class="card"><div class="date">UK · Inheritance tax</div><h3>Elborne v HMRC — home-loan IHT scheme upheld</h3><p>Court of Appeal (13 Jul) commentary tracker: ICLG, Paris Smith, Professional Adviser, RPC and more; marquee-firm briefings pending.</p><span class="read">Open tracker &rarr;</span></div></a>
<a class="card-link" href="trackers/china-offshore-trusts.html" style="text-decoration:none;color:inherit"><div class="card"><div class="date">China · Trusts</div><h3>China offshore-trust income tax (Announcement 2026 No. 21)</h3><p>24 Jul announcement tracker: official/primary sources now; genuine firm alerts pending (expected early August).</p><span class="read">Open tracker &rarr;</span></div></a>

<h2 style="font-size:17px;margin:22px 0 6px">Daily editions</h2>

{cards}

</div></main>

<footer class="site"><div class="wrap">Private Client Tax Digest · updated daily · built automatically</div></footer>
</body>
</html>
""".format(updated=html.escape(updated), cards="\n".join(cards))

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(page)
    print("Wrote {} with {} edition(s).".format(OUT, len(entries)))


if __name__ == "__main__":
    main()
