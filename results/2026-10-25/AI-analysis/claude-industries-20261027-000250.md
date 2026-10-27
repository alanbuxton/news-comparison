# Industries Analysis — 20261027-000250

*Model: claude-opus-4-7 | Max articles per topic per provider: 20*

*Provider labels were anonymised. See `decode-key-20261027-000250.json` to decode.*

---

```json
{
  "query_type": "industries",
  "providers": [
    {
      "label": "A",
      "axes": {
        "precision": {"score": 3, "evidence": [
          "Molasses | Oceania: 14/20 flagged mkt-report plus 5 not-news — the topic is essentially a wall of SEO market-report pages (openpr, actualmarketresearch, accio.com, LinkedIn posts) with virtually no real news",
          "SOLVENTS: 15/20 mkt-report flags — same pattern, dominated by valuemarketresearch, giiresearch, coherentmarketinsights pages",
          "Converting and Finishing Machines | Southern Asia: Hindi-language promotional page from cndypress.com and Taiwanese machine-tool business roundups show weak entity/geography matching",
          "Run-wide: mkt-report 98/400 (24%), not-news 27/400 (7%) — roughly a third of returned rows are either SEO reports or social/forum/About pages"
        ]},
        "coverage": {"score": 9, "evidence": [
          "answered: 20/20 topics with 20 articles each — every queried industry/geography got a full result set",
          "PE Resins | US and Paper | Northern Europe show substantive, geographically on-topic coverage (Argus, Mysteel, Schjødt, Metsä)"
        ]},
        "metadata_integrity": {"score": 4, "evidence": [
          "no-publisher: 400/400 (100%) — every row shows only a domain in parentheses, no named outlet, across all 20 topics",
          "no-date: 0 (0%) and stale: 0 (0%) — dates are complete, which prevents the severe cap",
          "dup: 3 (1%) — minor"
        ]},
        "story_quality": {"score": 6, "evidence": [
          "Cheese/US items like 'U.S. cheese and butter are now among the cheapest in the world' carry informative multi-sentence summaries",
          "Several rows carry non-English snippets (Chinese, Japanese, Korean, Hindi) in Converting Machines/SA and Film/CN that a US/EU consumer cannot action without translation",
          "Market-report rows (e.g., 'Europe HVAC Market to Reach USD 58.67 Billion') carry generic forecast boilerplate rather than story detail"
        ]},
        "trust": {"score": 7, "evidence": [
          "errors: 0 across 20 topics",
          "URLs resolve to recognizable domains (reuters.com, globenewswire.com, argusmedia.com)",
          "Heavy use of openpr/einpresswire/LinkedIn/giiresearch inflates the apparent news volume with low-credibility sources"
        ]}
      },
      "verdict": "Full breadth and date hygiene, but a quarter of results are SEO market-report pages and every row is missing a named publisher."
    },
    {
      "label": "B",
      "axes": {
        "precision": {"score": 9, "evidence": [
          "Converter Foil | Northern America: 3 tight on-topic items (Novelis Bay Minette coil, ITC five-year review, SMM North America export data) with no SEO filler",
          "Paper | Northern Europe: Mondi Q3 EBITDA, Metsä Board Kemi winder, Stora Enso Veitsiluoto sawmill — all substantive strategic news",
          "mkt-report: 2/148 (1%) and not-news: 0 — essentially no SEO/social contamination",
          "Logistics | Western Africa: 13 articles all directly on West Africa air/ocean/delivery (Lekki Port HMM-ONE, Bolt Send 6M deliveries, Cotonou cargo rebound)"
        ]},
        "coverage": {"score": 7, "evidence": [
          "answered: 20/20 but article counts are low — Converter Foil/NA has only 3 articles, HR Services/Mid Atlantic only 5, Molasses/Oceania 5",
          "Several entities within topics still get real coverage (Mondelēz paper trays in Nordics, Pulpex Glasgow for Paper/N.Europe)",
          "Total articles: 148 — meaningfully less breadth per topic than A, D or E"
        ]},
        "metadata_integrity": {"score": 10, "evidence": [
          "no-date: 0, stale: 0, no-publisher: 0 across all 148 rows",
          "Every row carries both a named publisher and a date (e.g., 'Reuters', 'Packaging Europe', 'IRU')",
          "dup: 0"
        ]},
        "story_quality": {"score": 9, "evidence": [
          "Summaries are consistently full-sentence and decision-useful (e.g., Dow Q4 PE 7¢/5¢ hike details, FrieslandCampina Borculo WPI capacity doubling)",
          "Paper | N.Europe Mondi Q3 summary gives €196m EBITDA vs €223m with cost drivers — enough to decide without clicking"
        ]},
        "trust": {"score": 10, "evidence": [
          "errors: 0",
          "Sources skew to established outlets (Reuters, Al Jazeera, Packaging Europe, PULPAPERnews, Argus, ICIS)",
          "No suspicious URL patterns observed"
        ]}
      },
      "verdict": "Cleanest results in the run — named publishers everywhere, no SEO/social noise, but low article volume per topic trims coverage."
    },
    {
      "label": "C",
      "axes": {
        "precision": {"score": 4, "evidence": [
          "mkt-report: 29/104 (28%) — a very high share of SEO market-research pages (Mordor Intelligence, Persistence Market Research, Grand View, Expert Market Research)",
          "Molasses | Oceania: 4 of 5 rows are market reports or a LinkedIn post from Mackay Sugar (NOT-NEWS flag), leaving essentially no real news",
          "PE Resins | US: 'Dow starts up new 600,000 t/yr HDPE/LLDPE swing unit' sourced to pmarketresearch.com rather than Dow or a trade outlet — second-hand SEO citation"
        ]},
        "coverage": {"score": 5, "evidence": [
          "answered: 20/20 but Professional Services | LATAM returned only 1 article, Converter Foil | NA only 2, Laboratory | Africa only 3",
          "Total articles: 104 — thinnest returns per topic across providers",
          "Multiple topics (PE Resins, SOLVENTS, Film/CN) returned mostly undated market-report pages"
        ]},
        "metadata_integrity": {"score": 2, "evidence": [
          "no-date: 84/104 (81%) — four out of five rows have no publication date at all, severely degrading the ability to tell if a story is this week or two years old",
          "no-publisher: 0 — publishers are named, which partially offsets but does not fix the date problem",
          "stale: 0 (indeterminate given missing dates)"
        ]},
        "story_quality": {"score": 6, "evidence": [
          "When present, summaries carry useful numbers (USDA August cheese 1.25bn lbs +1.4% YoY)",
          "Many market-report rows read as forecast boilerplate ('India CNC market USD 8.5bn in 2025, USD 12.4bn by 2034')",
          "Laboratory | Africa 'Life science industry in South Africa' is flagged in-text as actually a March 2024 interview despite the Oct 2026 search date"
        ]},
        "trust": {"score": 6, "evidence": [
          "errors: 0",
          "C itself flags one row as a March 2024 interview — honest self-disclosure but indicates date mislabeling upstream",
          "Reliance on secondary SEO citations (pmarketresearch, grandviewresearch) for primary industry claims lowers reliability"
        ]}
      },
      "verdict": "Heavy market-report tilt and 81% missing dates make this set hard to trust even where the headlines are plausibly on-topic."
    },
    {
      "label": "D",
      "axes": {
        "precision": {"score": 7, "evidence": [
          "Construction | Europe: Holcim Q3 guidance upgrade, Rexel Q3, German construction orders +23%, Balfour Beatty Birkhill Wood — strongly on-topic, substantive strategic news",
          "mkt-report: 3/276 (1%) and not-news: 0 — far less SEO contamination than A/C/E",
          "Professional Services | LATAM: substantial drift to Meta's $25B New Mexico privacy ruling — US state court case, not LATAM professional services (CONSULTING/FINANCIAL/LEGAL)",
          "HR Services | Mid Atlantic: UnitedHealth Q3, Humana NanoKnife, AngioDynamics coverage — insurance/health news but mostly national not Mid-Atlantic-specific"
        ]},
        "coverage": {"score": 6, "evidence": [
          "answered: 18/20 — Converter Foil | Northern America and Molasses | Oceania returned 0 results (NO RESULTS RETURNED)",
          "Film | CN returned only 1 article — a single market-report-flagged piece from einpresswire",
          "Where results do appear, counts are strong (20 each for Construction, HR Services, Logistics, Packaging, Paper, PE Resins)"
        ]},
        "metadata_integrity": {"score": 10, "evidence": [
          "no-date: 0, stale: 0, no-publisher: 0 across all 276 returned rows",
          "Named publishers include Bloomberg, Reuters, Investing.com, Business Wire, Yahoo Finance",
          "dup: 1/276 (<1%)"
        ]},
        "story_quality": {"score": 8, "evidence": [
          "Finance-oriented summaries carry concrete figures (Holcim 5.4% share surge, CHF 67.06; Kuehne+Nagel EBIT +53%)",
          "Paper topic entries from Investing.com include slide-deck summaries with margin and cash-flow detail",
          "Occasional terse one-liners (Myers Industries dividend) are adequate but light"
        ]},
        "trust": {"score": 7, "evidence": [
          "errors: 1 (reported in SOLVENTS topic header)",
          "Over-representation of Investing.com and Yahoo Finance aggregator links rather than primary sources",
          "Logistics/WAfrica Chariot lithium story is a West Australian financial-markets item mapped to West Africa logistics — tangential match"
        ]}
      },
      "verdict": "Financial-wire tilt gives strong metadata and credible outlets, but two topics returned nothing and LATAM professional-services drifted into unrelated US litigation."
    },
    {
      "label": "E",
      "axes": {
        "precision": {"score": 5, "evidence": [
          "Film | CN: multiple Chinese-language SZSE announcements (斯迪克 BOPET expansion, 国风新材 half-year) are genuinely on-topic but require Mandarin — plus 4 duplicates among 20",
          "mkt-report: 3/400 (<1%) and not-news: 1 — much less SEO filler than A or C",
          "HR Services | Mid Atlantic: Charles County employee health center, NJ 2027 health insurance rates, Maryland FAMLI — tightly on-geo and on-topic",
          "SOLVENTS 'Top 15 Companies in Global Acetone Market' from sphericalinsights is a ranked market-research page not flagged as mkt-report but functionally boilerplate"
        ]},
        "coverage": {"score": 9, "evidence": [
          "answered: 20/20 topics with 20 articles each (400 total)",
          "Molasses | Oceania actually returned Oceania-specific entities (Fiji Sugar Corporation Labasa, Isis-related items absent but FSC, Wilmar Myanmar) rather than global reports",
          "Whey Ingredients | N.Europe hits FrieslandCampina, Arla, Norrmejerier, DCA — all on-geography"
        ]},
        "metadata_integrity": {"score": 4, "evidence": [
          "no-publisher: 400/400 (100%) — every row carries only a parenthetical domain",
          "no-date: 0, stale: 0 — dates universally present",
          "dup: 5/400 (1%)"
        ]},
        "story_quality": {"score": 7, "evidence": [
          "Summaries often provide operational detail (Visy A$30m Smithfield corrugator with 33% output lift; Novelis Bay Minette first coil with 600kt capacity)",
          "Chinese-language rows in Film | CN leave an English-only reader guessing (国风新材 half-year)",
          "Longer form summaries in Paper | N.Europe (Billerud Q3 SEK 10.166bn, Metsä Board half-year) are decision-ready"
        ]},
        "trust": {"score": 8, "evidence": [
          "errors: 0",
          "Mixes primary company sites (visy.com, novelis.com, braskem.com) with trade press (packagingdive, pulpapernews, dairyreporter)",
          "Occasional secondary blog/aggregator (dalimss.news, brewersassocation.org) appears for Ethereal Machines and German foil exports"
        ]}
      },
      "verdict": "Strong breadth and dates with mostly on-topic substantive stories, but every row hides the publisher name behind a bare domain."
    }
  ]
}
```

## Notes

The run exposes a clean split between two provider strategies. B and D sit at opposite ends of a volume/precision trade: B returns ~7 articles per topic but every row has a named publisher, a date, and a decision-useful summary from an outlet you can place (Reuters, Packaging Europe, Argus). D returns ~14 per topic from financial-wire aggregators (Investing.com, Yahoo Finance, Business Wire) with similarly clean metadata, but two topics came back empty and the LATAM professional-services topic drifted into Meta's New Mexico privacy verdict — a US litigation story with no LATAM angle. A, C and E all answered every topic with 20 articles, but A and E hide the publisher behind a bare domain on 100% of rows, and C simply has no date on 81% of rows, which the rubric treats as a severe metadata failure.

The honest weakness of B is thin per-topic volume (Converter Foil/NA has 3 rows, HR Services 5), so a user wanting a wide scan would see fewer leads. D's weakness is topic-level coverage holes plus a tendency to confuse geographic/industry scope when the query is nuanced. The surprising pattern is how much SEO market-research content (openpr, giiresearch, Mordor, Persistence, accio.com, indexbox) still floods A and C — in Molasses and SOLVENTS these providers returned sets that were 70–80% forecast landing pages rather than news.

---

## Recomputed scorecard (harness — authoritative)

Axis scores are the model's; `weighted`, `final`, caps and the ranking
are recomputed by the harness. If numbers in the raw output above
disagree, this table wins.

| Rank | Provider | precision | coverage | metadata_integrity | story_quality | trust | weighted | final | caps |
|---|---|---|---|---|---|---|---|---|---|
| 1 | B | 9 | 7 | 10 | 9 | 10 | 8.9 | 8.9 | — |
| 2 | D | 7 | 6 | 10 | 8 | 7 | 7.4 | 7.4 | — |
| 3 | E | 5 | 9 | 4 | 7 | 8 | 6.4 | 6.4 | metadata_soft |
| 4 | A | 3 | 9 | 4 | 6 | 7 | 5.4 | 5.0 | metadata_soft, precision |
| 5 | C | 4 | 5 | 2 | 6 | 6 | 4.5 | 4.5 | metadata_hard |
