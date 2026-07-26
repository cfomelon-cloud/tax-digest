#!/usr/bin/env python3
"""One-off generator for the 19-26 July 2026 backfill editions.

Writes digests/YYYY-MM-DD.html for each edition, rewrites data/manifest.json,
and merges source keys into data/covered.json. Mirrors the site's HTML style.
"""
import json, os, html, re
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))

def norm_key(url):
    u = url.strip().lower()
    u = re.sub(r'^https?://', '', u)
    u = re.sub(r'^www\.', '', u)
    u = u.split('#')[0].split('?')[0].rstrip('/')
    return u

def src_line(sources):
    parts = []
    for label, url in sources:
        parts.append('<a href="{}">{}</a>'.format(html.escape(url), html.escape(label)))
    return ' · '.join(parts)

# Each edition: date, headline, blurb, lead(html|None), blocks[], quiet(list of jurisdiction names), secondary(str|None)
# block: {flag, name, badge:(cls,label)|None, items:[...]}  item: {tag:(cls,label), body(html), sources[], adviser(html|None), firm(html|None)}
EDITIONS = [
 {
  "date":"2026-07-19",
  "headline":"Singapore weighs fund-manager tax cuts to counter Hong Kong",
  "blurb":"Quiet across most jurisdictions. Reports that MAS is reviewing Singapore's fund-manager tax concession to stay competitive with Hong Kong's proposed carried-interest package.",
  "lead":None,
  "blocks":[
    {"flag":"🇸🇬","name":"Singapore","badge":("mod","Reported"),"items":[
      {"tag":("r","Reported"),
       "body":"<strong>MAS reviewing fund-manager tax concession to counter Hong Kong.</strong> Per an FT report (carried by Bloomberg), the Monetary Authority of Singapore has been consulting investment firms on staying competitive, including possibly lowering the fund-manager tax concession rate (reported toward ~10% vs the 17% headline) so savings can flow to portfolio managers. Prompted by Hong Kong's proposed carried-interest / privately-offered-fund package. No final measure — a review, not an announced change.",
       "sources":[("Business Standard (carrying FT/Bloomberg)","https://www.business-standard.com/world-news/singapore-authorities-eye-tax-cuts-for-fund-managers-to-stay-competitive-126071900409_1.html"),("Bloomberg","https://www.bloomberg.com/news/articles/2026-07-19/singapore-weighs-hedge-fund-tax-cuts-to-be-more-competitive-ft")],
       "adviser":"Relevant to family offices and fund principals weighing the HK vs Singapore hub decision — a signal Singapore may defend its position on cost, but nothing to act on until a concrete proposal emerges.","firm":None},
    ]},
  ],
  "quiet":["UK","US","China","Hong Kong"],
  "secondary":"No material developments in-window across Italy, Portugal, Australia, Canada or Taiwan.",
 },
 {
  "date":"2026-07-20",
  "headline":"UK change of government: Burnham PM, Healey Chancellor; gilts sell off",
  "blurb":"Andy Burnham becomes PM and names John Healey Chancellor (replacing Starmer/Reeves); gilts sell off on 'fiscal flexibility' remarks. Plus a US Tax Court QTIP valuation ruling and firm commentary on the UK Elborne IHT case.",
  "lead":"<strong>Top move.</strong> The <strong>UK has a new government</strong>: Andy Burnham became Prime Minister on 20 July and appointed <strong>John Healey</strong> as Chancellor (replacing Rachel Reeves) — reshaping the autumn Budget outlook for private clients. Gilts sold off as Burnham signalled 'flexibility within the fiscal rules.'",
  "blocks":[
    {"flag":"🇬🇧","name":"United Kingdom","badge":("hi","Material development"),"items":[
      {"tag":("c","Confirmed"),
       "body":"<strong>Andy Burnham becomes PM; John Healey named Chancellor.</strong> Burnham formally became Prime Minister on 20 July 2026 and, in a surprise, appointed John Healey (ex-Defence Secretary, with prior Treasury experience) as Chancellor, replacing Rachel Reeves. Healey is seen as relatively fiscally cautious; the manifesto 'tax lock' on the main rates of income tax, employee NIC and VAT is expected to hold.",
       "sources":[("GOV.UK — ministerial appointments (official)","https://www.gov.uk/government/news/ministerial-appointments-july-2026"),("Bloomberg","https://www.bloomberg.com/news/articles/2026-07-20/john-healey-named-chancellor-by-new-uk-pm-andy-burnham")],
       "adviser":"Sets the frame for everything that follows: with the rate-lock retained, private-client revenue pressure points to CGT, IHT reliefs, property and continued fiscal drag at the autumn Budget.","firm":None},
      {"tag":("r","Reported"),
       "body":"<strong>Gilts sell off on 'fiscal flexibility' remarks.</strong> UK government bonds fell after Burnham signalled he would seek flexibility within the fiscal rules; the 10-year yield rose to break 5% and the 30-year approached ~5.75%, among the highest in the G7 — reflecting investor concern about looser discipline.",
       "sources":[("CityAM","https://www.cityam.com/borrowing-costs-jump-after-burnham-fiscal-flexibility-remarks/")],
       "adviser":None,
       "firm":"<strong>Firm &amp; professional commentary:</strong> Paris Smith (Anthony Nixon) published a client note on the Court of Appeal's <em>Elborne v HMRC</em> decision (handed down ~13 July) upholding the 'double trust / home loan' IHT scheme, while cautioning the outcome could differ today under DOTAS/GAAR. <a href=\"https://parissmith.co.uk/blog/inheritance-tax-on-family-home-elborne/\">Paris Smith</a>"},
    ]},
    {"flag":"🇺🇸","name":"United States","badge":("mod","Confirmed"),"items":[
      {"tag":("c","Confirmed"),
       "body":"<strong>Tax Court: state law governs QTIP remainder valuation (Lewis v. Commissioner, T.C. Memo 2026-58).</strong> The Tax Court held that state law — not the §7520 tables — governs valuation of remainder interests on a QTIP trust termination, and that gift values are reduced under §2207A net-gift mechanics. A useful data point for QTIP unwinds, GRAT/remainder valuations and net-gift planning for HNW families.",
       "sources":[("Current Federal Tax Developments (Ed Zollars)","https://www.currentfederaltaxdevelopments.com/blog/2026/7/20/valuation-of-remainder-interest-gifts-upon-trust-termination-state-law-and-net-gift-adjustments-in-lewis-v-commissioner")],
       "adviser":None,"firm":None},
    ]},
  ],
  "quiet":["China","Hong Kong","Singapore"],
  "secondary":"No material developments in-window across Italy, Portugal, Australia, Canada or Taiwan.",
 },
 {
  "date":"2026-07-21",
  "headline":"Burnham scraps electricity VAT for six months; HMRC IHT receipts hit record £2.3bn",
  "blurb":"UK: Burnham removes VAT on domestic electricity for six months from October; HMRC inheritance-tax receipts reach a record £2.3bn for the quarter as frozen bands bite.",
  "lead":"<strong>Top move.</strong> The new UK government's first tax measure — <strong>VAT scrapped on domestic electricity</strong> for six months from October — lands the same week HMRC reports <strong>record IHT receipts</strong>, underscoring how frozen thresholds keep pulling estates into charge.",
  "blocks":[
    {"flag":"🇬🇧","name":"United Kingdom","badge":("hi","Material development"),"items":[
      {"tag":("c","Confirmed"),
       "body":"<strong>Electricity VAT cut 5%&rarr;0% for six months.</strong> Burnham announced removal of VAT on domestic electricity across GB (with equivalent NI funding) from 1 October 2026 to 31 March 2027, as cost-of-living relief. Independent analysis (Martin Lewis) put the real-terms benefit at roughly £20 over the period, as a ~3% price-cap rise lands at the same time. Costed at around £0.85bn.",
       "sources":[("ITV News","https://www.itv.com/news/2026-07-21/andy-burnham-announces-tax-cut-on-energy-bills-from-october"),("MoneySavingExpert (analysis)","https://www.moneysavingexpert.com/news/2026/07/electricity-bills-vat-cut-martin-lewis-analysis/")],
       "adviser":"Little direct HNW impact, but note it as a spending commitment that widens the autumn Budget funding gap — reinforcing the case for revenue-raisers elsewhere.","firm":None},
      {"tag":("c","Confirmed"),
       "body":"<strong>HMRC inheritance-tax receipts hit record £2.3bn.</strong> HMRC data showed IHT receipts of £2.3bn for the three months to June 2026 — a record for the period, up £96m year-on-year — with frozen nil-rate bands dragging more estates into the net. Stamp-duty receipts were also up.",
       "sources":[("CityAM","https://www.cityam.com/iht-receipts-hit-record-high-as-rachel-reeves-frozen-bands-raid-plague-brits/"),("HMRC receipts bulletin (GOV.UK)","https://www.gov.uk/government/statistics/hmrc-tax-and-nics-receipts-for-the-uk")],
       "adviser":"Fiscal drag on estates is accelerating; combined with the April-2027 pensions-into-IHT change and the £1m BPR/APR cap, this strengthens the case for reviewing gifting, trusts and life cover now.","firm":None},
    ]},
  ],
  "quiet":["US","China","Hong Kong","Singapore"],
  "secondary":"No material developments in-window across Italy, Portugal, Australia, Canada or Taiwan.",
 },
 {
  "date":"2026-07-22",
  "headline":"Burnham walks back personal-allowance unfreeze; ~£22bn gap points to autumn tax rises",
  "blurb":"UK: Burnham rows back on lifting the frozen £12,570 personal allowance; ~£22bn of unfunded pledges fuels 'guaranteed' autumn tax-rise talk. Industry warns MAS that managers eye a Hong Kong move.",
  "lead":"<strong>Top move.</strong> Two UK signals harden the outlook: Burnham <strong>walks back</strong> any personal-allowance unfreeze (the freeze stays), and analysts put the government's unfunded pledges near <strong>£22bn</strong> — making autumn revenue-raisers look near-certain.",
  "blocks":[
    {"flag":"🇬🇧","name":"United Kingdom","badge":("mod","Reported"),"items":[
      {"tag":("r","Reported"),
       "body":"<strong>Burnham walks back the personal-allowance unfreeze.</strong> After appearing to hint the frozen £12,570 income-tax allowance could rise, Burnham rowed back, with No.10 declining to commit to unfreezing thresholds. The freeze (running to April 2028) — a major fiscal-drag revenue-raiser — is likely to stay.",
       "sources":[("Professional Adviser","https://www.professionaladviser.com/news/4533237/burnham-income-tax-allowance-increase-suggestion-reports"),("Bloomberg","https://www.bloomberg.com/news/articles/2026-07-22/burnham-walks-back-suggestion-he-ll-lift-uk-income-tax-threshold")],
       "adviser":"Plan on the freeze holding; watch the £100k–£125,140 personal-allowance taper and continued drag into higher bands.","firm":None},
      {"tag":("r","Reported"),
       "body":"<strong>~£22bn of unfunded pledges → autumn tax rises 'guaranteed'.</strong> Analysis identified roughly £22bn of Burnham-government commitments not in official forecasts (energy VAT cut, extra defence, other pledges). With the manifesto ring-fencing income tax, VAT and employee NIC, commentators flagged pension tax relief, CGT and IHT reliefs as likely targets — nothing announced.",
       "sources":[("CityAM","https://www.cityam.com/healey-faces-22bn-black-hole-after-spending-pledges/")],
       "adviser":"The revenue will most plausibly come from CGT, IHT reliefs, property and fiscal drag. The pre-Budget window favours acting early on CGT disposals and large gifts.","firm":None},
    ]},
    {"flag":"🇸🇬","name":"Singapore / Hong Kong","badge":("mod","Reported"),"items":[
      {"tag":("r","Reported"),
       "body":"<strong>AIMA warns MAS that managers eye a Hong Kong move.</strong> The Alternative Investment Management Association told MAS that hedge-fund and asset managers are weighing relocation to Hong Kong, citing HK's proposed carried-interest break and pointing to <em>individual</em> taxation as 'the decisive lever' for mobile talent — urging lower taxes and headcount-linked relief. Industry submission, not a tax change.",
       "sources":[("Yahoo Finance (carrying Bloomberg)","https://sg.finance.yahoo.com/news/hedge-fund-stars-looking-quit-021504289.html")],
       "adviser":"Reinforces the HK vs Singapore competitive dynamic for family offices and principals — a factor in siting decisions, though no rule has changed.","firm":None},
    ]},
  ],
  "quiet":["US","China"],
  "secondary":"No material developments in-window across Italy, Portugal, Australia, Canada or Taiwan.",
 },
 {
  "date":"2026-07-23",
  "headline":"Quiet day — Canada opens consultation on draft tax legislation",
  "blurb":"A light day. Canada's Finance Department opened consultation on draft legislative proposals (FAPI, Disability Tax Credit and technical measures); limited direct private-client content. Priority jurisdictions otherwise quiet.",
  "lead":None,
  "blocks":[
    {"flag":"🇨🇦","name":"Canada","badge":("mod","Confirmed"),"items":[
      {"tag":("c","Confirmed"),
       "body":"<strong>Finance opens consultation on draft tax legislation.</strong> The Department of Finance released draft legislative proposals for consultation — technical amendments spanning the Disability Tax Credit, foreign accrual property income (FAPI), hybrid-mismatch rules, transfer pricing and GST/HST. Largely business/technical; the main private-client touch-points are FAPI (families with foreign holding structures) and the DTC.",
       "sources":[("Finance Canada (official)","https://www.canada.ca/en/department-finance/news/2026/07/government-launches-consultation-on-draft-legislation-for-various-tax-measures.html")],
       "adviser":"Families with foreign holding companies should note the FAPI amendments; otherwise limited HNW impact.","firm":None},
    ]},
  ],
  "quiet":["UK","US","China","Hong Kong","Singapore"],
  "secondary":"Aside from Canada (above), no material developments in-window across Italy, Portugal, Australia or Taiwan.",
 },
 {
  "date":"2026-07-24",
  "headline":"China brings offshore trusts into income tax (20%); US QDOT technical fix; Australia estate-relevant drafts",
  "blurb":"China's MOF/STA clarify a 20% individual income tax on residents' offshore-trust income with a 90-day disclosure window — the week's biggest private-client move. Plus a US QDOT regulation correction and Australian estate/family-law drafts.",
  "lead":"<strong>Top cross-border move.</strong> <strong>China</strong> has brought <strong>offshore trusts</strong> into individual income tax — Announcement 2026 No. 21 (MOF + State Taxation Administration) sets a <strong>20%</strong> charge on residents' trust income with a 90-day penalty-waiver disclosure window. A serious hit to mainland HNW families' offshore-trust succession structures and their HK/Singapore advisers.",
  "blocks":[
    {"flag":"🇨🇳","name":"China (Mainland)","badge":("hi","Material development"),"items":[
      {"tag":("c","Confirmed"),
       "body":"<strong>Offshore trusts brought into IIT (Announcement 2026 No. 21).</strong> The Ministry of Finance and State Taxation Administration jointly clarified that Chinese resident individuals must declare and pay individual income tax on income from transferring assets into offshore trusts and on income during the trust's life — taxed as 'income from transfer of property' or as 'interest, dividends and bonuses,' both at the flat <strong>20%</strong> rate, across settlement, operation and liquidation. A <strong>90-day voluntary-disclosure grace period</strong> waives late-payment surcharges; establishment-stage retroactive tax is waived for trusts running over three years, though lifetime income remains reportable. Framed as enforcement of existing law, not new legislation.",
       "sources":[("MOF / State Taxation Administration announcement, via Xinhua (official)","https://english.news.cn/20260724/b4210103695a49b89ab6178813f71721/c.html"),("State Taxation Administration — full text (chinatax.gov.cn)","https://jiangsu.chinatax.gov.cn/art/2026/7/24/art_23636_13143.html"),("Bloomberg","https://www.bloomberg.com/news/articles/2026-07-24/china-targets-offshore-trusts-in-sweeping-tax-clampdown")],
       "adviser":"Closes a core succession-planning route for mainland HNW families and extends the CRS/offshore-income enforcement drive. Affected clients should use the 90-day disclosure window rather than wait for an STA notice, and revisit offshore-trust settlor status, distribution timing and the three-year threshold. HK and Singapore advisers serving mainland families should expect restructuring queries and tighter source-of-wealth scrutiny.",
       "firm":"<strong>Firm &amp; professional commentary:</strong> As at publication, dedicated big-4 / private-client law-firm client alerts (Withers, KPMG, Baker McKenzie, Zhong Lun, Han Kun) had not yet been indexed within the window; these typically follow within days and will be captured as they appear."},
    ]},
    {"flag":"🇺🇸","name":"United States","badge":("low","Technical"),"items":[
      {"tag":("c","Confirmed"),
       "body":"<strong>Treasury correction to final QDOT (§2056A) regulations.</strong> Treasury/IRS published a correction to TD 10050, the final rules on qualified domestic trusts (relevant to estates with a non-citizen surviving spouse). Purely technical — cross-reference and drafting fixes, no policy change — but the only in-window federal cross-border private-client item.",
       "sources":[("Federal Register (official)","https://www.federalregister.gov/documents/2026/07/24/2026-15008/revising-qualified-domestic-trust-regulations-under-section-2056a-to-update-outdated-references-and")],
       "adviser":None,"firm":None},
    ]},
    {"flag":"🇦🇺","name":"Australia","badge":("mod","Reported"),"items":[
      {"tag":("r","Reported"),
       "body":"<strong>Estate- and family-law-relevant drafts surface.</strong> Reported in a professional-body technical bulletin: draft rules consolidating foreign-resident CGT withholding variations (allowing variation to nil for deceased estates, relationship breakdowns, tax-exempt entities and mortgagee sales), and new Family Law regulations empowering the Minister to direct super trustees on valuing a member's interest — both relevant to HNW estates and divorce splits.",
       "sources":[("IFPA technical bulletin (24 Jul)","https://ifpa.com.au/24-july-2026/")],
       "adviser":"Single-source and technical — worth monitoring for the primary ATO/instrument confirmation, but relevant to estate and matrimonial private-client matters.","firm":None},
    ]},
  ],
  "quiet":["UK","Hong Kong","Singapore"],
  "secondary":"Aside from Australia (above), no material developments in-window across Italy, Portugal, Canada or Taiwan.",
 },
 {
  "date":"2026-07-25",
  "headline":"Quiet day — Neidle questions whether Scotland's 48p top rate raises anything",
  "blurb":"A light day. Tax Policy Associates (Dan Neidle) argues Scotland's 48% additional rate may sit past the peak of the Laffer curve, raising little net revenue once migration and income-shifting are counted. Priority jurisdictions otherwise quiet.",
  "lead":None,
  "blocks":[
    {"flag":"🇬🇧","name":"United Kingdom","badge":("mod","Commentary"),"items":[
      {"tag":("a","Analyst-option"),
       "body":"<strong>Expert commentary — Scotland's 48p top rate 'may raise little or nothing'.</strong> Tax Policy Associates (Dan Neidle) argues Scotland's 48% additional rate may sit past the peak of the Laffer curve — raising little or no net revenue once behavioural responses (migration and income-shifting by higher earners) are accounted for. Relevant to Scottish-resident HNW clients and residence-planning conversations.",
       "sources":[("Tax Policy Associates","https://taxpolicy.org.uk/2026/07/25/scotland-48p-top-rate-laffer-curve/")],
       "adviser":"A useful evidence point for Scottish-domiciled high earners weighing residence; analysis, not policy.","firm":None},
    ]},
  ],
  "quiet":["US","China","Hong Kong","Singapore"],
  "secondary":"No material developments in-window across Italy, Portugal, Australia, Canada or Taiwan.",
 },
 {
  "date":"2026-07-26",
  "headline":"Quiet day — no new items; the week's major developments carried in earlier editions",
  "blurb":"A quiet Sunday. Nothing genuinely new in the last 48h that was not already covered — China's offshore-trust rules (24 Jul) and the UK change-of-government thread (20–22 Jul) are in their dated editions.",
  "lead":None,
  "blocks":[],
  "quiet":["UK","US","China","Hong Kong","Singapore"],
  "secondary":"No material developments in-window across the secondary jurisdictions. See the 24 July edition (China offshore trusts) and 20–22 July editions (UK change of government) for the week's main private-client developments.",
 },
]

TAG = {"c":"c","r":"r","a":"a"}

def render_item(it):
    out = []
    tag_cls, tag_lbl = it["tag"]
    body = it["body"]
    out.append('<li><span class="tag {}">{}</span> {}'.format(tag_cls, html.escape(tag_lbl), body))
    if it.get("sources"):
        out.append('<br><span style="font-size:13px">Sources: {}</span>'.format(src_line(it["sources"])))
    out.append('</li>')
    tail = []
    if it.get("adviser"):
        tail.append('<div class="read-box"><strong>Adviser read:</strong> {}</div>'.format(it["adviser"]))
    if it.get("firm"):
        tail.append('<p class="feas">{}</p>'.format(it["firm"]))
    return ''.join(out), ''.join(tail)

def render_edition(ed):
    d = datetime.strptime(ed["date"], "%Y-%m-%d")
    nice = d.strftime("%A %d %B %Y")
    parts = []
    parts.append('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    parts.append('<title>Private Client Tax Digest — {}</title>\n<link rel="stylesheet" href="../style.css">\n</head>\n<body>'.format(d.strftime("%d %B %Y")))
    parts.append('<header class="site"><div class="wrap"><h1>Private Client Tax Digest</h1><p>Cross-border tax updates for high-net-worth individuals, families &amp; their advisers</p></div></header>')
    parts.append('<main><div class="wrap"><article>')
    parts.append('<a class="back" href="../index.html">&larr; All editions</a>')
    parts.append('<h1>Daily edition — {}</h1>'.format(nice))
    parts.append('<p class="sub">Priority: UK · US · China · Hong Kong · Singapore · Secondary: Italy · Portugal · Australia · Canada · Taiwan</p>')
    parts.append('<p class="legend" style="background:#f6f8fa;border:1px solid #e5e7eb;border-radius:8px;padding:10px 14px;"><strong>Strictly the last ~48 hours, no repeats.</strong> Only developments genuinely published/announced in roughly the past two days and not covered before. Quiet jurisdictions are marked as such. Tags: <span class="tag c">Confirmed</span>, <span class="tag r">Reported</span>, <span class="tag a">Analyst-option</span>.</p>')
    if ed.get("lead"):
        parts.append('<div class="lead">{}</div>'.format(ed["lead"]))
    if ed["blocks"]:
        parts.append('<h2>Developments</h2>')
        for b in ed["blocks"]:
            badge = ''
            if b.get("badge"):
                bcls, blbl = b["badge"]
                badge = ' <span class="badge {}">{}</span>'.format(bcls, html.escape(blbl))
            parts.append('<div class="jur"><h3>{} {}{}</h3><ul>'.format(b["flag"], html.escape(b["name"]), badge))
            tails = []
            for it in b["items"]:
                li, tail = render_item(it)
                parts.append(li)
                if tail: tails.append(tail)
            parts.append('</ul>')
            parts.extend(tails)
            parts.append('</div>')
    if ed.get("quiet"):
        parts.append('<h2>Quiet in-window</h2>')
        parts.append('<p style="font-size:14px;margin:6px 0;">No new items in the last 48h for: <strong>{}</strong>.</p>'.format(html.escape(", ".join(ed["quiet"]))))
    if ed.get("secondary"):
        parts.append('<h2>Secondary jurisdictions</h2><p style="font-size:14px;margin:6px 0;">{}</p>'.format(ed["secondary"]))
    parts.append('<p class="foot">Compiled under strict last-48h, no-repeat rules; part of the 19–26 July 2026 backfill. Tags: Confirmed = legislated/announced; Reported = briefed or under consultation; Analyst-option = commentator advocacy, not policy. Sources cross-checked for reputability and accessibility where practicable. Not tax advice.</p>')
    parts.append('</article></div></main>')
    parts.append('<footer class="site"><div class="wrap">Private Client Tax Digest · updated daily · <a href="../index.html">all editions</a></div></footer>')
    parts.append('</body>\n</html>\n')
    return '\n'.join(parts)

# write editions
covered = set()
manifest = []
for ed in EDITIONS:
    path = os.path.join(ROOT, "digests", ed["date"] + ".html")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(render_edition(ed))
    manifest.append({"date":ed["date"],"file":"digests/{}.html".format(ed["date"]),
                     "headline":ed["headline"],"blurb":ed["blurb"]})
    for b in ed["blocks"]:
        for it in b["items"]:
            for _, url in it.get("sources", []):
                covered.add(norm_key(url))

# manifest.json (newest first)
manifest.sort(key=lambda e: e["date"], reverse=True)
with open(os.path.join(ROOT, "data", "manifest.json"), "w", encoding="utf-8") as fh:
    json.dump(manifest, fh, indent=2, ensure_ascii=False)

# merge covered.json
cp = os.path.join(ROOT, "data", "covered.json")
with open(cp, "r", encoding="utf-8") as fh:
    cj = json.load(fh)
existing = set(cj.get("keys", []))
merged = sorted(existing | covered)
cj["keys"] = merged
with open(cp, "w", encoding="utf-8") as fh:
    json.dump(cj, fh, indent=2, ensure_ascii=False)

print("Wrote {} editions; manifest {} entries; covered {} keys ({} new).".format(
    len(EDITIONS), len(manifest), len(merged), len(covered - existing)))
