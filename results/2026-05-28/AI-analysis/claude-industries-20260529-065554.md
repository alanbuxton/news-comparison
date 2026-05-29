# Industries Analysis — 20260529-065554

*Model: claude-opus-4-7 | Max articles per topic per provider: 15*

*Provider labels were anonymised. See `decode-key-20260529-065554.json` to decode.*

---

```json
{
  "query_type": "industries",
  "providers": [
    {
      "label": "A",
      "axes": {
        "precision":         {"score": 5, "evidence": [
          "BOARD Eastern Asia returned only 'Pulp and Paper Chemicals Market to Reach US$ 33.53 Billion by 2034' — a global market-report landing page, off-topic for the regional query",
          "Converter Foil global topic dominated by BP chairman ouster stories (e.g., 'Ousted BP chairman hits back at lies') — wrong entity for foil/aluminium",
          "SOLVENTS Northern Europe is largely BP chairman ouster coverage rather than solvents news",
          "Film Distribution Midwest returned 1 article ('Marcus Theatres names Jeffry Tomachek') which is on-topic and clean"
        ]},
        "coverage":          {"score": 5, "evidence": [
          "Several queried topics returned only 1 article (LABORATORY Africa, LIQUIDS Southern Africa, LOGISTICS Western Africa, Road Freight Europe, Film Distribution Midwest)",
          "BOARD Eastern Asia produced only 1 weak market report",
          "PE Resins US, Cheese/Milk Powders US, Cocoa Asia Pacific produced 10–14 results each — reasonable",
          "Total of 153 articles across ~24 topics — thin per-topic"
        ]},
        "recency_integrity": {"score": 10, "evidence": [
          "Header: no-date: 0, stale (>90d): 0 across 153 articles",
          "Dates within 90-day window for all topics (e.g., Cheese/Milk Powders US ranges 2026-03-16 to 2026-05-26)"
        ]},
        "story_quality":     {"score": 7, "evidence": [
          "Cheese/Milk Powders US: 'Maola Local Dairies Introduces Maola Strawberry Whole Milk' summary too thin",
          "CONSTRUCTION Europe: 'UK construction slump deepens as ready-mix concrete sales tumble' with concrete stat (1.1% fall) is informative",
          "Converter Foil: 'Hindalco, Nalco shares jump up to 5%' includes specific price data ($3,672.50/tonne)",
          "Several market-report headlines provide CAGR numbers but no real news"
        ]},
        "trust":             {"score": 9, "evidence": [
          "Header: errors: 0, dup: 0",
          "URLs appear legitimate (S&P Global, PR Newswire, Reuters, etc.)",
          "Packaging Boxes IN includes one suspicious 2028-11-04 dated article (future date beyond window)"
        ]}
      },
      "weighted": 6.25,
      "caps_applied": [],
      "final": 6.25,
      "verdict": "Clean dates and no errors but thin coverage and noticeable off-topic drift (BP chairman in solvents, market reports in board) drag precision down."
    },
    {
      "label": "B",
      "axes": {
        "precision":         {"score": 6, "evidence": [
          "BOARD Eastern Asia: strong on-topic results ('Nippon Paper assessing impacts after deadly Washington mill implosion', 'Holmen expands lightweight containerboard range')",
          "CLEANING SUPPLIES New England: drift to unrelated stories ('LabLabee × Algérie Télécom', 'Spain blocks prediction markets Polymarket Kalshi')",
          "Molasses Oceania flooded with off-topic items (Zoomcar IPO, Westpac stock, Unitree Robotics IPO)",
          "PE Resins US largely on-topic ('Polyethylene price uptrend stalls as demand cools', 'May pricing bullish for most bales')"
        ]},
        "coverage":          {"score": 10, "evidence": [
          "1373 articles across ~28 topics; every topic returned 40+ articles",
          "Strong per-entity hits: Cheese/Milk Powders US ('U.S. Dairy Output Sees Strongest Multi-Month Growth Since 2003')",
          "Converter Foil Northern America: deep coverage of aluminium prices, Section 232 tariffs"
        ]},
        "recency_integrity": {"score": 10, "evidence": [
          "Header: no-date: 0, stale (>90d): 0 across 1373 articles",
          "All dates within May 2026 window for most topics"
        ]},
        "story_quality":     {"score": 8, "evidence": [
          "Strong financial detail: 'BP plc removed its chairman, Albert Manifold, with immediate effect on 26 May'",
          "Construction Europe: 'NEOM Cancels High-Speed Rail Between Oxagon and The Line' with EUR 1.4bn figure",
          "Some summaries truncated mid-sentence ('[...]' artefacts) but typically actionable"
        ]},
        "trust":             {"score": 7, "evidence": [
          "Header: errors: 8 (in PROFESSIONAL SERVICES LATAM topic)",
          "Header: dup: 30 — Financial Stability Review duplicates across 5 language URLs counted as TPs",
          "Most sources are reputable (Reuters, Bloomberg, S&P, FT, Nikkei)"
        ]}
      },
      "weighted": 7.65,
      "caps_applied": [],
      "final": 7.65,
      "verdict": "Massive volume with strong topical hits but inconsistent precision — geographic/entity drift in several topics, some duplicate clutter, and 8 errors."
    },
    {
      "label": "C",
      "axes": {
        "precision":         {"score": 6, "evidence": [
          "Cheese/Milk Powders US: many entries are supplier 'About' pages (AGT Food investor relations, ofi ingredients page, Nouryon strategy) — FP-not-news",
          "LIQUIDS Southern Africa: dominated by supplier product pages (Classic Solvents, Birla Carbon, Kampak) — not news",
          "LABORATORY Africa: Anton Paar, Labotec entries are vendor profile pages",
          "Construction Europe and Distribution Services Northern America entries are mostly legit news"
        ]},
        "coverage":          {"score": 5, "evidence": [
          "85 articles across 24 topics; thin per-topic (CONVERTING/Southern Asia: 1, PACKAGING Oceania: 1, PAPER Northern Europe: 1)",
          "PE Resins US has 5 substantive items, Cheese/Milk Powders US 10",
          "Some queried industries returned only supplier directories rather than news"
        ]},
        "recency_integrity": {"score": 10, "evidence": [
          "Header: no-date: 0, stale (>90d): 0 across 85 articles",
          "Dates within window for all observed entries"
        ]},
        "story_quality":     {"score": 6, "evidence": [
          "Where genuine news appears, summaries are informative ('Electrolux Group and Midea Group form long-term strategic partnership in North America')",
          "Supplier-page summaries are boilerplate ('ofi describes itself as a global ingredient supplier')",
          "Some entries explicitly flag they are 'supplier discovery' not news"
        ]},
        "trust":             {"score": 7, "evidence": [
          "Header: errors: 1 (in HR SERVICES Mid Atlantic)",
          "URLs are real (Symrise, Electrolux, Stora Enso) but several are corporate site landing pages rather than dated news",
          "No duplicates"
        ]}
      },
      "weighted": 6.2,
      "caps_applied": [],
      "final": 6.2,
      "verdict": "Curated and clean on metadata but heavy reliance on supplier 'About' and directory pages instead of actual news limits real value."
    },
    {
      "label": "D",
      "axes": {
        "precision":         {"score": 5, "evidence": [
          "BOPET CN: nearly all items are market-research forecast reports (Towardspackaging, Insightace, IndexBox) — FP-not-news beyond ≤2 quota",
          "Film Distribution Midwest: heavy on market-research reports (Verified Market Report, Market Research World, Allied Market Research)",
          "OIL/FUEL South-eastern Asia and Cheese/Milk Powders US contain some real news (Reuters, Al Jazeera, Guardian)",
          "PE Resins US returned only 1 article (Syntex America blog) plus 4 errors"
        ]},
        "coverage":          {"score": 4, "evidence": [
          "63 articles across ~21 topics; Film | CN returned 0 articles (10 errors)",
          "PE Resins US: 1 article only",
          "Distribution Services Northern America: 1 article (forecast report)",
          "Multiple topics have just 1–3 results"
        ]},
        "recency_integrity": {"score": 10, "evidence": [
          "Header: no-date: 0, stale (>90d): 0",
          "Dates fall within 90-day window"
        ]},
        "story_quality":     {"score": 6, "evidence": [
          "Where real news: OIL/FUEL Southeast Asia ('Indonesia has raised its mandatory biodiesel blending rate from 40% to 50%') is informative",
          "Market report summaries provide CAGR numbers but little strategic news",
          "BOPET CN summaries are boilerplate forecast language"
        ]},
        "trust":             {"score": 5, "evidence": [
          "Header: errors: 14 (Film | CN: 10 errors; PE Resins US: 4 errors)",
          "High error count is significant given small total volume",
          "URLs appear legitimate where present"
        ]}
      },
      "weighted": 5.5,
      "caps_applied": [],
      "final": 5.5,
      "verdict": "Small return set dominated by market-research forecast pages with 14 errors and one topic returning nothing — limited utility for strategic news."
    },
    {
      "label": "E",
      "axes": {
        "precision":         {"score": 2, "evidence": [
          "BOPET CN: largely unrelated ('Beijing AstronStone Aerospace Technology' funding, 'China pharma industry not impacted by Beijing scrutiny')",
          "Film CN: includes 'China Original Pickle' and 'China Popcorn Variety Pack' IndexBox market pages — unrelated",
          "Many entries are IndexBox market-analysis store pages — FP-not-news",
          "Converter Foil topic includes 'Boutique bank deal champions long-term greed' — unrelated"
        ]},
        "coverage":          {"score": 8, "evidence": [
          "1876 articles across 28 topics; ~40-90 per topic",
          "Topical hits exist but buried in noise (e.g., Construction Europe 'Eurozone construction activity down in Jan')"
        ]},
        "recency_integrity": {"score": 0, "evidence": [
          "Header: no-date: 1876 of 1876 — every article lacks a date",
          "Cannot verify recency for any item; rubric treats no-date as critical FP"
        ]},
        "story_quality":     {"score": 4, "evidence": [
          "Many entries truncated or boilerplate ('1. Modeling Logic 2. Source Register' from IndexBox)",
          "Some summaries informative (Construction Europe: 'Private equity dealmaking in construction & engineering surged to record levels in Q4 2025')",
          "Repeated navigation/menu text degrades usability"
        ]},
        "trust":             {"score": 6, "evidence": [
          "Header: errors: 0, dup: 27",
          "URLs are legitimate (Reuters, Bloomberg, WSJ, ICIS) but content extraction is poor",
          "Duplicate ECB Financial Stability Review across language versions in PAPER Northern Europe"
        ]}
      },
      "weighted": 3.8,
      "caps_applied": ["recency_hard", "precision"],
      "final": 3.8,
      "verdict": "Massive volume undermined by 100% missing dates and heavy off-topic drift (IndexBox catalogues, pickle/popcorn pages under Film CN); fails recency integrity test."
    }
  ],
  "ranking": ["B", "A", "C", "D", "E"],
  "ranking_rationale": {
    "1st": "B: high coverage, clean dates, mostly on-topic real news despite duplicate and entity-drift issues",
    "2nd": "A: smallest clean set with perfect recency but coverage is thin and some topics drift off-entity",
    "3rd": "C: curated/dated cleanly but leans on supplier 'About' pages rather than news",
    "4th": "D: small volume, mostly market-research reports, 14 errors and one topic with zero results",
    "5th": "E: largest set but 100% no-date and heavy off-topic IndexBox catalogue noise triggers hard caps"
  }
}
```

## Notes

The run shows a sharp split between volume-oriented crawlers (B, E) and curated providers (A, C, D). B is the only volume provider that paired scale with dated, mostly on-topic results — but it still leaks BP-chairman governance stories into the SOLVENTS topic and dilutes Molasses Oceania with unrelated Westpac/Unitree items, suggesting weak entity disambiguation. E's complete absence of dates is decisive: even with 1,876 items, an analyst cannot trust recency, and the content itself often consists of IndexBox store landing pages for unrelated commodities (pickles, popcorn) under industry queries.

B's honest weaknesses: 30 near-duplicate Financial Stability Review entries across language URLs inflate counts, 8 errors in the LATAM topic suggest fragility, and several topics (CLEANING SUPPLIES New England, Molasses Oceania) show clear topic-classifier failures where the provider returned global business news rather than the queried industry. Despite this, B's combination of dated recent items from reputable outlets (Reuters, Bloomberg, S&P, FT, Nikkei) and per-topic depth is unmatched in this run.