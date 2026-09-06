# Industries Analysis — 20260906-213406

*Model: claude-opus-4-7 | Max articles per topic per provider: 15*

*Provider labels were anonymised. See `decode-key-20260906-213406.json` to decode.*

---

```json
{
  "query_type": "industries",
  "providers": [
    {
      "label": "A",
      "axes": {
        "precision":         {"score": 6, "evidence": [
          "CONSTRUCTION|Europe surfaces off-topic items: 'Haier Announces Global Partnership with UEFA Champions League' and 'Apple sued for alleged patent infringement by German company BASF' — neither is European construction/HVAC/electrical",
          "SOLVENTS: multiple wrong-entity Reliance/telecom items ('What's up with… Gamma, Jio, Mobily', 'What Reliance and Rolls-Royce mean for India's fighter jet ambitions') pollute the acetone/EA/MEK intent",
          "PE Resins|US contains 'Tarkett expands Johnsonite wall base portfolio' — flooring, not PE resin",
          "Most results in PAPER|Northern Europe, LOGISTICS|Western Africa, Road Freight|Europe are clean on-topic strategic stories (Metsä, UPM/Sappi, Dangote, Tata-Iveco)"
        ]},
        "coverage":          {"score": 8, "evidence": [
          "answered: 18/20 topics — Converter Foil|Northern America and Molasses|Oceania returned zero",
          "Thin coverage on Film|CN (1 article) and LABORATORY|Africa (1 article) and Whey Ingredients|Northern Europe (2 articles)",
          "Strong coverage on PACKAGING|Oceania (16), PE Resins|US (20), Road Freight|Europe (20)"
        ]},
        "metadata_integrity": {"score": 10, "evidence": [
          "Header: no-date 0 (0%), stale 0 (0%), no-publisher 0 (0%)",
          "Publishers named on every row (Reuters, Bloomberg, ChemAnalyst, Plastics News, etc.)"
        ]},
        "story_quality":     {"score": 8, "evidence": [
          "PE Resins|US summaries name deals and figures: 'Descartes acquires fulfillment provider Extensiv for $120M'",
          "Road Freight|Europe: 'Tata Motors will offer 14.10 euros per common share... acceptance period running from September 7 to October 26'",
          "Some snippets are one-line stubs, e.g. 'UK construction slides again, pulled down by weak housebuilding, PMI shows'"
        ]},
        "trust":             {"score": 10, "evidence": [
          "errors: 0 in header",
          "URLs resolve to recognisable outlets (reuters.com, bloomberg.com, globenewswire.com)"
        ]}
      },
      "verdict": "Clean metadata and reputable sources with mostly on-topic strategic coverage, but two empty topics and stray off-topic contamination (UEFA, Apple/BASF, Reliance telecom) drag precision."
    },
    {
      "label": "B",
      "axes": {
        "precision":         {"score": 2, "evidence": [
          "mkt-report: 136 (34%) of results — Molasses|Oceania alone has 16 market-report landing pages; LABORATORY|Africa 12; Film|CN 12; SOLVENTS 16",
          "Converter Foil|Northern America dominated by IndexBox/openpr/LinkedIn market-outlook pages rather than news",
          "PACKAGING|Oceania includes 'Top 10 Paper Bag Manufacturers Serving Australia' from cnlipack.com — directory-style listicle",
          "HR SERVICES|Mid Atlantic mixes in generic globals like 'ESG and Human Capital Disclosure Platform Market' rather than Mid-Atlantic HR news"
        ]},
        "coverage":          {"score": 10, "evidence": [
          "answered: 20/20 topics, 20 articles per topic including Converter Foil|Northern America and Molasses|Oceania that others missed",
          "Every queried entity produced results, even niche ones like LABORATORY|Africa"
        ]},
        "metadata_integrity": {"score": 5, "evidence": [
          "no-publisher: 400 (100%) — every row flagged NO PUBLISHER ⚠, only domains visible",
          "no-date 0 (0%), stale 0 (0%) — dates fully populated",
          "Domains are typically visible (reuters.com, bloomberg.com, linkedin.com) so credibility is degraded not absent"
        ]},
        "story_quality":     {"score": 4, "evidence": [
          "Many summaries are LinkedIn post excerpts or market-report bullet lists: 'Key Players ... - Transdev Group - MoveInSync...'",
          "Content often reads as boilerplate, e.g. Molasses topic snippets are all CAGR forecasts",
          "Real news items when present (EU UPM-Sappi Reuters) do carry usable summaries"
        ]},
        "trust":             {"score": 7, "evidence": [
          "errors: 0 in header",
          "Heavy reliance on SEO/market-research domains (openpr.com, indexbox.io, linkedin.com pulse, mordorintelligence.com) lowers source credibility even though URLs are real"
        ]}
      },
      "verdict": "Full coverage and clean dates, but the results are dominated by market-research landing pages and LinkedIn posts with every publisher missing, making the feed noisy and low-signal for a strategic buyer."
    },
    {
      "label": "C",
      "axes": {
        "precision":         {"score": 9, "evidence": [
          "Only 1 mkt-report across 167 articles",
          "CONSTRUCTION|Europe results are tightly on-intent: 'Bravida acquires electrical contractor Åslunds El', 'Instalco lands NCC contract in Stockholm worth SEK 100m'",
          "SOLVENTS results all address ethyl acetate/acetone/MEK: 'Wanhua, Formosa shut combined 1.41mln t/y phenol-acetone units'",
          "HR SERVICES|Mid Atlantic includes on-region items like Sentara-Anthem Virginia dispute and Marsh 8.2% cost forecast"
        ]},
        "coverage":          {"score": 10, "evidence": [
          "answered: 20/20 topics with no [NO RESULTS RETURNED] items",
          "Even hard topics answered: LABORATORY|Africa (6 items incl. WAHO/Guinea-Bissau, Ethiopia FDA), Molasses|Oceania (6 incl. Rocky Point mill, Mackay Sugar cyberattack)"
        ]},
        "metadata_integrity": {"score": 10, "evidence": [
          "Header: no-date 0, stale 0, no-publisher 0",
          "Named publishers on every row (Reuters, USDA AMS, European Commission, ChemOrbis)"
        ]},
        "story_quality":     {"score": 9, "evidence": [
          "Summaries convey the actionable fact: 'US LDPE prices declined sharply in early July as weak downstream demand, abundant availability and lower ethylene costs...'",
          "Cheese/US: 'USDA Dairy Market News reported August 2026 product price averages of $1.5985 per pound for nonfat dry milk...'",
          "Molasses|Oceania: STL taking over six Queensland terminals — precise scope"
        ]},
        "trust":             {"score": 10, "evidence": [
          "errors: 0",
          "URLs point to primary sources (ec.europa.eu, ams.usda.gov, whitehouse.gov, reuters.com, spglobal.com)"
        ]}
      },
      "verdict": "Tight, on-intent results with primary-source URLs and clean metadata across all 20 topics; the only limitation is smaller volume per topic (6–14 items), which some users may see as thinness."
    },
    {
      "label": "D",
      "axes": {
        "precision":         {"score": 5, "evidence": [
          "Only 20 articles total; 3 are mkt-reports (15%)",
          "PACKAGING|Oceania returned a generic vendor blog 'How Can Corrugated Paper Box Solutions Transform Modern Packaging Trends?' from chenxingpack.com — FP-not-news",
          "Cheese|US result 'UK Milk Utilisation Trends 2026' is UK-focused, off-region",
          "PE Resins|US: 'Polimerica News: Bioplastics and Regulatory Updates' is Italian regulatory not US PE"
        ]},
        "coverage":          {"score": 2, "evidence": [
          "answered: 8/20 topics — 12 topics returned NO RESULTS (Converter Foil, External Manufacturing, Film|CN, IT&Telecom N.Africa, Laboratory|Africa, Liquids|S.Africa, Logistics|W.Africa, Molasses|Oceania, Road Freight|Europe, Solvents, Whey|N.Europe, CONVERTING machines)",
          "Even answered topics are thin (1–5 items)"
        ]},
        "metadata_integrity": {"score": 9, "evidence": [
          "no-date 0, stale 0, no-publisher 0 in header",
          "Publishers named (BRG News, Cowsmo, IndexBox, Precedence Research)"
        ]},
        "story_quality":     {"score": 6, "evidence": [
          "Summaries are readable, e.g. Cheese|US: 'USDA's May 2026 report highlights a record U.S. cheese production of 1.28 billion pounds, a 2% increase'",
          "But some are vague market-outlook prose without specific companies or deals"
        ]},
        "trust":             {"score": 3, "evidence": [
          "errors: 10 in header (all in Film|CN)",
          "Half of Film|CN attempts errored out",
          "URLs resolve but heavy reliance on lower-tier outlets (chenxingpack.com vendor page)"
        ]}
      },
      "verdict": "Very low volume, majority of topics unanswered, and a 10-error cluster on Film|CN — a coverage and reliability failure despite clean dates on what little was returned."
    },
    {
      "label": "E",
      "axes": {
        "precision":         {"score": 5, "evidence": [
          "mkt-report: 64 (16%) — Laboratory|Africa has 14 IndexBox market reports out of 20, and Solvents 6, Molasses 4",
          "SOLVENTS returns off-topic 'MEK Price Trend Q2 2026' KeweX Site pages and Solvay/TSMC hydrogen-peroxide (not ethyl acetate/acetone/MEK intent match — though some acetone content is on-topic)",
          "HR SERVICES|Mid Atlantic is on-region and on-intent (Maryland FAMLI, Sentara-Anthem Virginia, King Risk Partners Mid-Atlantic)",
          "PACKAGING|Oceania is largely on-intent (Australian PKN news, Recorp beverage cans, EPR debate)"
        ]},
        "coverage":          {"score": 10, "evidence": [
          "answered: 20/20 topics, all 20 items returned per topic",
          "Molasses|Oceania answered with real Queensland/Fiji cane stories alongside market reports",
          "Whey|N.Europe fully answered with Arla, FrieslandCampina, Vesper data"
        ]},
        "metadata_integrity": {"score": 5, "evidence": [
          "no-publisher: 400 (100%) — every row flagged NO PUBLISHER ⚠, only domains shown",
          "no-date 0 (0%), stale 0 (0%) — dates fully populated",
          "Domains typically credible (reuters.com, bloomberg.com, chemorbis.com, ec.europa.eu, packagingnews.com.au) so degradation is partial"
        ]},
        "story_quality":     {"score": 7, "evidence": [
          "Solid deal detail e.g. Road Freight|Europe: '203,359 trucks above 3.5 tonnes were registered across the European Union, EFTA countries and the United Kingdom'",
          "Whey|N.Europe: 'Arla Foods Ingredients revenue rose 19.3% to €867 million'",
          "Some IndexBox/openpr snippets are boilerplate CAGR bullets that add little"
        ]},
        "trust":             {"score": 8, "evidence": [
          "errors: 0",
          "Mix of tier-1 outlets (Reuters, Bloomberg, ec.europa.eu, whitehouse-adjacent) and lower-tier openpr/LinkedIn/IndexBox pages",
          "9 duplicates flagged (2%)"
        ]}
      },
      "verdict": "Comprehensive coverage with generally strong sources and rich summaries, but universal missing publisher labels and a meaningful market-report share (especially in Laboratory|Africa and Solvents) dilute precision and metadata trust."
    }
  ]
}
```

## Notes

The starkest split in this run is between providers that returned news and providers that returned market-research SEO pages. B and E both answered all 20 topics with 20 items each, but B's 34% mkt-report share and E's 16% share reveal how much of that "coverage" is IndexBox/openpr/LinkedIn Pulse padding rather than actual reporting — most visible in Laboratory|Africa, Molasses|Oceania, and SOLVENTS. Both also strip publisher names from every row, forcing the reader to judge credibility from the domain alone. D is the coverage failure of the run: 12 of 20 topics empty and 10 errors clustered on Film|CN.

C is the cleanest by every quality axis measured — zero errors, zero missing dates, zero missing publishers, one mkt-report across 167 articles, and primary-source URLs (ec.europa.eu, ams.usda.gov, whitehouse.gov). Its honest weakness is volume: 4–14 articles per topic where B and E return 20, so a user who wants exhaustive scanning may feel it thin. A sits between the two poles — clean metadata and reputable outlets, but two zero-result topics (Converter Foil, Molasses|Oceania) and off-topic contamination in CONSTRUCTION|Europe (Haier/UEFA, Apple/BASF) and SOLVENTS (Reliance telecom) keep precision from being top-tier.

---

## Recomputed scorecard (harness — authoritative)

Axis scores are the model's; `weighted`, `final`, caps and the ranking
are recomputed by the harness. If numbers in the raw output above
disagree, this table wins.

| Rank | Provider | precision | coverage | metadata_integrity | story_quality | trust | weighted | final | caps |
|---|---|---|---|---|---|---|---|---|---|
| 1 | C | 9 | 10 | 10 | 9 | 10 | 9.5 | 9.5 | — |
| 2 | A | 6 | 8 | 10 | 8 | 10 | 7.9 | 7.9 | — |
| 3 | E | 5 | 10 | 5 | 7 | 8 | 6.75 | 6.75 | metadata_soft |
| 4 | B | 2 | 10 | 5 | 4 | 7 | 5.1 | 5.0 | metadata_soft, precision |
| 5 | D | 5 | 2 | 9 | 6 | 3 | 4.85 | 4.0 | trust |
