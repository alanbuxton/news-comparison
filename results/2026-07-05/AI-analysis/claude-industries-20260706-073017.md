# Industries Analysis — 20260706-073017

*Model: claude-opus-4-7 | Max articles per topic per provider: 15*

*Provider labels were anonymised. See `decode-key-20260706-073017.json` to decode.*

---

```json
{
  "query_type": "industries",
  "providers": [
    {
      "label": "A",
      "axes": {
        "precision":         {"score": 6, "evidence": ["Strong TP on 'Converter Foil' with Hindalco Q4 results, GIADEC €300m aluminium foil plant MoU; but 33% mkt-report share (139/426) drags precision — e.g. 14/20 LIQUIDS | Southern Africa are Exclusive Press market reports", "PACKAGING | Oceania is 18/20 mkt-reports (Modified Atmosphere, Tube, Wine, Lip Care, Bubble Wrap) — surplus SEO noise", "CLEANING SUPPLIES | New England mixes wrong-entity like Terex dividend, Lantheus FDA CRL, Schneider EcoCare UPS with genuine TPs (Unilever New Haven, Fraser Commercial Services)", "Film Distribution | Midwest returned a Disney/toy plastic packaging article — FP-entity vs movies intent"]},
        "coverage":          {"score": 9, "evidence": ["answered 28/29 topics; only 'BOPET | CN' returned no results", "Deep results on 'PROFESSIONAL SERVICES | LATAM' with Broadfield São Paulo, Tilt-Blipay, Allianz Brazil, Bain-Advent Amil bid", "Road Freight | Europe covered with Ceva-Paack, CMA CGM Notre Dame, Wrist Group acquisitions"]},
        "recency_integrity": {"score": 10, "evidence": ["Header: no-date: 0 (0%), stale: 0 (0%) across 426 articles", "All Film | CN entries dated within 90 days (BOPP Plastech July 3, ByteDance June items)"]},
        "story_quality":     {"score": 8, "evidence": ["Substantive summaries e.g. 'Hindalco Q4 Results: Net profit drops 51% YoY to ₹2,597 crore' with detail on aluminium/copper", "'Skanska builds industrial facility in Karmøy, Norway, for NOK 1.1 billion' — clear scope", "Some Cision PR Newswire entries are one-line headlines only (e.g. 'Terex Announces Quarterly Dividend')"]},
        "trust":             {"score": 10, "evidence": ["Header: errors: 0", "Sources include Bloomberg, Reuters, Business Wire, Zawya, Economic Times — no suspicious URL patterns", "Dup rate 2/426 (0%)"]}
      },
      "verdict": "Broad topic coverage with clean dates and zero errors, but 33% market-report share and off-topic wrong-entity results in cleaning/tolling/film-distribution topics pull precision down."
    },
    {
      "label": "B",
      "axes": {
        "precision":         {"score": 6, "evidence": ["Converter Foil | Northern America returns on-topic USMCA aluminium review and White House Section 232 adjustment — genuine TPs", "OIL/FUEL | SEA has 5 clean TPs (Indonesia B50 rollout, Reuters Asia energy crisis)", "Some FP-not-news: Missouri Film Office incentive page for Film Distribution reads more like a program page than news", "Only 28 total articles across 13 topics limits room for FP but proportion of mkt-reports (5/28 = 18%) is moderate"]},
        "coverage":          {"score": 2, "evidence": ["answered 13/29 topics; 16 topics returned zero (BOARD Eastern Asia, BOPET CN, CLEANING SUPPLIES, HR SERVICES, LABORATORY Africa, PAPER Northern Europe, PE Resins US, Packaging Boxes IN, Road Freight Europe, SOLVENTS both, and more)", "Only 28 total articles — thinnest in the run", "Whey Ingredients only 3 articles but all TP (Guardian, DairyReporter Arla-DMK, DCA whey price)"]},
        "recency_integrity": {"score": 10, "evidence": ["Header: no-date: 0 (0%), stale: 0 (0%)", "All Converter Foil | NA entries dated April-June 2026"]},
        "story_quality":     {"score": 7, "evidence": ["Solid summaries e.g. 'Delta Air Lines added Liberia to its global cargo embargo list' with context on narcotics enforcement (LOGISTICS)", "Whey Ingredients Guardian entry cites '€1,700 per tonne — a record high and a 50% rise'", "Some entries are terse policy summaries (Council/Consilium steel deal)"]},
        "trust":             {"score": 2, "evidence": ["Header: errors: 189 — catastrophic error rate dwarfing 28 delivered articles", "10 errors each on BOARD Eastern Asia, Cocoa Asia Pacific, Converter Foil, HR SERVICES, LABORATORY Africa, SOLVENTS with no results returned", "Sources look legitimate (Reuters, Guardian, DairyReporter, White House)"]}
      },
      "verdict": "When it returns something the content is on-topic and well-summarized, but 189 errors and 16/29 empty topics make it structurally unreliable."
    },
    {
      "label": "C",
      "axes": {
        "precision":         {"score": 5, "evidence": ["Strong TP examples: Billerud BCTMP interim report for BOARD Eastern Asia; Novelis 10-K for Converter Foil; Ingredion-Tate & Lyle for Whey Ingredients; USDA Dairy Market News for Cheese/Cultures", "But many CLEANING SUPPLIES entries are corporate 'About Us' pages (Fortune Brands, Unilever homepage, Nyco Products, ISSA trade association) — flagged as not-news by the provider's own summaries", "LABORATORY | Africa returns Labotec + Anton Paar LinkedIn post — one is a social-media post which the summary itself calls out; Polymer Char is a supplier product page", "PE Resins | US mixes real news (Syntex polymer price story) with supplier product pages (Suke Plastics, Fujian Gulei product page)"]},
        "coverage":          {"score": 4, "evidence": ["answered 16/29 topics; 13 empty including BOPET CN, Construction Europe, Converting Machines SEA, Film Distribution, Film CN, IT&Telecom N.Africa, LIQUIDS S.Africa, Molasses, Oil/Fuel SEA, Packaging Oceania, Paper N.Europe, Packaging Boxes IN, SOLVENTS N.Europe", "Only 47 total articles"]},
        "recency_integrity": {"score": 10, "evidence": ["Header: no-date: 0 (0%), stale: 0 (0%)", "All Road Freight | Europe entries dated April-May 2026"]},
        "story_quality":     {"score": 8, "evidence": ["Rich analyst-style summaries e.g. Ingredion acquiring Tate & Lyle 'approximately US$3.6 billion' with strategic context", "Road Freight Europe entries name GEODIS hubs in Germany/Poland, XPO AI pricing tools, DSV strategic review with actionable detail", "S&P Global aluminium 'supply crisis' story well-summarized"]},
        "trust":             {"score": 8, "evidence": ["Header: errors: 0, dup: 0", "Cites Bloomberg, Reuters, FT, S&P Global, USDA, SEC — solid sources", "Some URLs point at supplier product pages (sukeplastics.com, gulei-petrochemical.com) rather than news, but no hallucinated URLs detected"]}
      },
      "verdict": "High-quality summaries and clean dates on the topics it does answer, but heavy reliance on About/product pages in some verticals and 13 unanswered topics limit usefulness."
    },
    {
      "label": "D",
      "axes": {
        "precision":         {"score": 2, "evidence": ["Header: no-date: 2142 (100%) — every article missing a date, so by rubric all are FP-no-date", "Massive off-topic drift: Film | CN returns 'German union calls for walkouts at Deutsche's Postbank' and 'Bayer completes acquisition of Perfuse Therapeutics'", "Cheese/Cultures/Milk Powders US mixes on-topic dairy with generic Suppliers/Airbus Defence pages and AgriFood signals wraps", "Molasses | Oceania returns MLG Oz Gruyere Mining contract, Homebuilder Berkeley annual profit, Serendip Holdings — wrong-entity FPs", "Many Reuters/TradingView links show 'More news from Reuters' navigation scraps, not article body"]},
        "coverage":          {"score": 8, "evidence": ["answered 29/29 topics with 2142 total articles", "Every queried entity got something back, e.g. BOPET CN, Film Distribution Midwest, Molasses Oceania all populated"]},
        "recency_integrity": {"score": 0, "evidence": ["Header: no-date: 2142 (100%) — ground truth: every single article carries [NO DATE ⚠]", "Impossible for user or agent to verify whether items fall within past 90 days"]},
        "story_quality":     {"score": 3, "evidence": ["Many summaries are boilerplate navigation text: 'More news from Reuters Dec 22, 2025 Reuters Mergers and acquisitions'", "PAPER | N.Europe entry 'Tellusgruppen Gets Two Municipal Staffing Contracts' — headline only, no informative body", "Some substantive summaries do exist (WSJ Novelis Oswego restart, Reuters aluminium crisis) but drowned out by scraped nav chrome"]},
        "trust":             {"score": 6, "evidence": ["Header: errors: 0", "Sources are legitimate (Reuters, WSJ, Bloomberg, ICIS, Mining.com) but 100% no-date suggests broken metadata extraction, undermining trustworthiness", "Dup rate 35/2142 (2%)"]}
      },
      "verdict": "Answered every topic and no errors, but 100% missing dates and heavy nav-chrome scraping make the volume nearly unusable for a professional needing recency-verified insight."
    },
    {
      "label": "E",
      "axes": {
        "precision":         {"score": 8, "evidence": ["Strong on-topic TP: BOARD Eastern Asia includes Metsä Board Milan studio, Bobst Masterfold, JK Paper BCTMP commercial production, China corrugated pricing detail", "Cheese/Cultures/Milk Powders US covers USDA reports, Nara Organics botulism, whey shortage, dairy exports — all on-topic", "Some FP-entity slippage e.g. HR SERVICES | Mid Atlantic 'New Jersey charges employers for Medicaid workers' is national policy — arguably relevant to CSR/health insurance intent", "Only 7% mkt-report share (88/1337) — much lower than A"]},
        "coverage":          {"score": 10, "evidence": ["answered 29/29 topics with 1337 articles; every intent covered including BOPET CN (Chinese-language PET pricing) and Molasses Oceania (Fiji Sugar Corp harvest crisis)", "Converter Foil returns 47 articles including LME price moves, Vedanta Q1 output, AAI import duty appeal"]},
        "recency_integrity": {"score": 10, "evidence": ["Header: no-date: 0 (0%), stale: 0 (0%) across 1337 articles", "Fresh July 2026 dates on BOARD, BOPET, Film CN, Cheese, Converter Foil topics"]},
        "story_quality":     {"score": 8, "evidence": ["Detailed summaries e.g. 'Vedanta Aluminium Metal Limited opened FY27 with higher output... record 632,000 tonnes' with source context", "Cheese US: 'US nonfat dry milk prices hit record high in May... Wholesale dairy prod...' from The Dairy Site", "Occasional truncated Chinese-language summaries in BOPET/Film CN but still information-dense"]},
        "trust":             {"score": 9, "evidence": ["Header: errors: 0, dup: 19/1337 (1%)", "Sources include Reuters, Bloomberg, Business Line, Alcircle, Palm Oil Magazine, ETV Bharat, Freight News — mostly legitimate trade press", "A few less-known sources (yrules.com, wownews24x7) but no hallucinated URL patterns detected"]}
      },
      "verdict": "Highest coverage with strong dating and low duplication; occasional wrong-entity slippage and heavy reliance on trade-press aggregators are the main weaknesses."
    }
  ]
}
```

## Notes

The most striking pattern is the recency-integrity split: A, B, C, and E all deliver 0% no-date content, while D returns 2,142 articles with 100% missing dates — an all-or-nothing metadata failure that makes D's superficially impressive coverage nearly worthless for a 90-day industry-exposure query. B's other failure mode (189 errors vs 28 delivered articles) is equally structural. Provider volume ranges from B's 28 to D's 2,142, but useful volume — on-topic, dated, informative — clusters around A (426) and E (1,337).

Among the stronger providers, A's chief weakness is the 33% market-report share (139/426), which dominates topics like PACKAGING Oceania (18/20 mkt-reports) and Cocoa APAC (4/4), and its wrong-entity drift into cinema for Film CN's plastic-film intent and into fire-truck lawsuits for CLEANING SUPPLIES. E's weakness is a reliance on second-tier trade aggregators and a smattering of wrong-region/wrong-entity results (e.g. New Jersey Medicaid policy under HR SERVICES Mid Atlantic is arguably on-intent but is really a national story). C's summaries are the most analyst-friendly when present, but 13 empty topics and a habit of returning supplier About/product pages as "articles" limit its practical value.

---

## Recomputed scorecard (harness — authoritative)

Axis scores are the model's; `weighted`, `final`, caps and the ranking
are recomputed by the harness. If numbers in the raw output above
disagree, this table wins.

| Rank | Provider | precision | coverage | recency_integrity | story_quality | trust | weighted | final | caps |
|---|---|---|---|---|---|---|---|---|---|
| 1 | E | 8 | 10 | 10 | 8 | 9 | 8.85 | 8.85 | — |
| 2 | A | 6 | 9 | 10 | 8 | 10 | 8.1 | 8.1 | — |
| 3 | C | 5 | 4 | 10 | 8 | 8 | 6.45 | 6.45 | — |
| 4 | B | 6 | 2 | 10 | 7 | 2 | 5.35 | 4.0 | trust |
| 5 | D | 2 | 8 | 0 | 3 | 6 | 3.65 | 3.65 | recency_hard, precision |
