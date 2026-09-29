# Industries Analysis — 20260928-070223

*Model: claude-opus-4-7 | Max articles per topic per provider: 15*

*Provider labels were anonymised. See `decode-key-20260928-070223.json` to decode.*

---

```json
{
  "query_type": "industries",
  "providers": [
    {
      "label": "A",
      "axes": {
        "precision":         {"score": 9, "evidence": ["Film|CN returned on-intent BOPP/BOPET/PE items like 'Sidike RMB 1.652bn BOPET expansion' and 'SunSirs China Polyethylene Prices'", "Converter Foil|Northern America items are aluminium-foil-relevant (Canada 50% counter-tariff on HS 7607 foil; Commerce anti-circumvention on aluminium containers)", "HR SERVICES|Mid Atlantic returned genuinely regional/intent-matched pieces (Baltimore Sun ACA rate, PA Pennie 16% hike, Marsh Stanchina Mid-Atlantic)", "only 1 mkt-report across 120 articles (SOLVENTS openPR INEOS Hull), no dup, no wrong-entity noise"]},
        "coverage":          {"score": 9, "evidence": ["answered: 20/20; LABORATORY|Africa thin (2 articles) and LIQUIDS|Southern Africa thin (3) but non-empty", "SOLVENTS returned only 3 articles including Celanese acetyls price hike — small but on-intent"]},
        "metadata_integrity": {"score": 10, "evidence": ["no-date: 0, stale: 0, no-publisher: 0 across 120 rows", "publishers named e.g. Reuters, Cyprus Mail, FIEC, Packaging Dive"]},
        "story_quality":     {"score": 9, "evidence": ["Summaries carry specific figures — 'UK construction PMI 44.3', 'Krones ₹315-crore Vemagal plant', 'Metsä Fibre 160 employees Joutseno'", "Summaries let user judge without clicking on IT & TELECOM Egypt/Algeria stories"]},
        "trust":             {"score": 10, "evidence": ["errors: 0; URLs point to real outlets (reuters.com, canada.ca, pulpapernews.com)", "no hallucination markers observed"]}
      },
      "verdict": "Small article counts but nearly every row is on-intent, dated, and attributed to a named publisher — a curated feed with no metadata rot."
    },
    {
      "label": "B",
      "axes": {
        "precision":         {"score": 3, "evidence": ["mkt-report: 131/400 (33%) — CONSTRUCTION|Europe topic has 13/20 flagged (e.g., 'Spain Construction Market 2026-2031', 'Europe Ventilation Market Share')", "Molasses|Oceania: 13/20 mkt-report, most items are accio.com/mordorintelligence forecasts, not news", "Packaging Boxes|IN filled with justdial.com directory listings ('Packaging Box in Allahabad', 'Packaging Box in Lucknow') — FP-not-news", "Film|CN carries directory pages (b2bdata.baidu.com 'Top 10 Bopp Film Manufacturers', made-in-china.com supplier listings)"]},
        "coverage":          {"score": 9, "evidence": ["answered: 20/20 with 20 articles each including thin topics (LABORATORY|Africa, LIQUIDS|Southern Africa)"]},
        "metadata_integrity": {"score": 5, "evidence": ["no-date: 0, stale: 0 — strong on dates", "no-publisher: 400/400 (100%) — every row shows only the domain in parentheses (e.g., openpr.com, linkedin.com, indexbox.io)"]},
        "story_quality":     {"score": 5, "evidence": ["Some summaries are informative (e.g., UPM-Sappi Reuters excerpt)", "Many summaries are boilerplate market-report blurbs — 'CAGR of X.X%' repeated across LABORATORY, PACKAGING, SOLVENTS", "Justdial entries have generic 'The Indian packaging box market has witnessed significant transformations' text"]},
        "trust":             {"score": 6, "evidence": ["errors: 0", "URLs resolve to real domains but many are content-farm/SEO pages (openpr.com, natlawreview.com press releases, LinkedIn Pulse posts)"]}
      },
      "verdict": "Consistently answers every query with volume, but a third of articles are market-report SEO pages and directory listings, and no publisher is ever named — high-noise, low-signal."
    },
    {
      "label": "C",
      "axes": {
        "precision":         {"score": 4, "evidence": ["CONSTRUCTION|Europe dominated by finance/M&A wire noise unrelated to building intent (Emlak Konut Bursa land, Kalpataru LMG Nasdaq listing, Northvolt recycling)", "HR SERVICES|Mid Atlantic returned wrong-topic analyst-call items (Humana upgrade, Royal Caribbean debt, Homebuilders/Berkshire) not HR/CSR/employee-benefits/fleet", "PE Resins|US mixed with off-intent items (Tarkett wall base, QatarEnergy LNG contracts, GPGI class action) that aren't PE-resin news", "Converter Foil|Northern America and Molasses|Oceania returned NO RESULTS"]},
        "coverage":          {"score": 5, "evidence": ["answered: 18/20 — 'Converter Foil|Northern America' and 'Molasses|Oceania' both empty", "Whey Ingredients|Northern Europe returned only 3 articles; Film|CN only 1; LABORATORY|Africa only 2"]},
        "metadata_integrity": {"score": 10, "evidence": ["no-date: 0, stale: 0, no-publisher: 0; timestamps precise to seconds"]},
        "story_quality":     {"score": 7, "evidence": ["Summaries include concrete figures (Eaton €810m COL acquisition; Smurfit Westrock CMPC deal)", "Some entries are pure wire headlines with little detail (e.g., 'Lifeway: Q2 Earnings Snapshot')"]},
        "trust":             {"score": 9, "evidence": ["errors: 0; sources are recognisable outlets (Reuters, Bloomberg, PR Newswire, Business Wire)"]}
      },
      "verdict": "Excellent metadata and reputable sources, but a strong finance/M&A wire bias pushes many results off the queried industry intent, and two topics returned nothing at all."
    },
    {
      "label": "D",
      "axes": {
        "precision":         {"score": 5, "evidence": ["mkt-report: 56/400 (14%) — LABORATORY|Africa has 10/20 IndexBox forecast pages ('Universal dip Cell Kit Market in Nigeria', 'FPLC Systems Market in Nigeria')", "Some topics are strong on-intent (PAPER|Northern Europe UPM-Sappi coverage; Road Freight|Europe with IAA, Uber Freight Krakow; PACKAGING|Oceania PKN articles)", "CONSTRUCTION|Europe carries relevant Eurostat/PMI/FIEC pieces mixed with market-report noise", "Cheese/Milk Powders|US has USDA reports, Cheese Reporter, Terrain — genuinely on-intent"]},
        "coverage":          {"score": 10, "evidence": ["answered: 20/20 with 20 articles each; LABORATORY|Africa and Molasses|Oceania non-empty"]},
        "metadata_integrity": {"score": 5, "evidence": ["no-date: 0, stale: 0", "no-publisher: 400/400 (100%) — domains shown but named outlets never surface (e.g., pulpapernews.com, packagingnews.com.au, reuters.com)"]},
        "story_quality":     {"score": 7, "evidence": ["Summaries carry specifics (Metsä Group €25m Muoto investment; Sharp autoinjector expansion Allentown; Eurostat July construction -0.3%)", "IndexBox and openPR entries carry generic forecast prose"]},
        "trust":             {"score": 8, "evidence": ["errors: 0; URLs point to real domains including reputable trade press (packagingnews.com.au, pulpapernews.com, freightwaves.com)"]}
      },
      "verdict": "Broadest coverage with generally on-topic trade-press content, weakened by ~14% market-report share and by never surfacing a publisher name."
    },
    {
      "label": "E",
      "axes": {
        "precision":         {"score": 8, "evidence": ["The 16 articles returned are largely on-intent (Ineos Hull acetyls SOLVENTS; Arla Foods Ingredients retrofit for Whey|Northern Europe; PPWR PAPER|Northern Europe)", "HR SERVICES|Mid Atlantic returned Meridian/TNA fleet partnership and SHRM cost-outlook — both intent-matched", "No mkt-report flags, no dup, no obvious FP-entity"]},
        "coverage":          {"score": 2, "evidence": ["answered: 9/20 — 11 topics returned NO RESULTS including CONSTRUCTION|Europe, Film|CN, Cheese/Milk Powders|US, Packaging Boxes|IN, Molasses|Oceania, LABORATORY|Africa"]},
        "metadata_integrity": {"score": 10, "evidence": ["no-date: 0, stale: 0, no-publisher: 0; publishers named (Automotive Fleet, Ecofin Agency, PULPAPERnews)"]},
        "story_quality":     {"score": 9, "evidence": ["Summaries are analytical and specific ('EU WPC80 prices reached €25,995/mt in August 2026, up 122% YoY'; 'INEOS mothballing 200,000t ethyl acetate, 500,000t acetic acid at Saltend')"]},
        "trust":             {"score": 8, "evidence": ["errors: 0; sources are recognisable (Ecofin, PULPAPERnews, DairyReporter)", "One URL is just a bare domain (w.media) for the Telecom Egypt story — thinner provenance"]}
      },
      "verdict": "When it returns anything the article is high-quality and on-intent, but it left more than half the queries empty — unusable as a primary source."
    }
  ]
}
```

## Notes

The run splits sharply into two failure modes. B and D deliver 20 articles per topic but never name a publisher and lean heavily on market-research SEO pages — B's 33% mkt-report share and B's Justdial directory listings for Indian packaging queries are the clearest examples of volume-over-signal. C and E, by contrast, carry clean metadata but each has its own hole: C leaves two topics empty and drifts into generic finance-wire coverage for HR SERVICES and PE Resins, while E answers fewer than half the queries at all.

A is the only provider that combines complete answer rate, named publishers, dated rows, and topic-appropriate trade-press sources — but its honest weakness is thinness: LABORATORY|Africa returned two articles, LIQUIDS|Southern Africa three, SOLVENTS three. A user who needs breadth on those exact topics may still have to supplement it, and its low article counts mean it is easier for A to look clean than for the higher-volume providers.

---

## Recomputed scorecard (harness — authoritative)

Axis scores are the model's; `weighted`, `final`, caps and the ranking
are recomputed by the harness. If numbers in the raw output above
disagree, this table wins.

| Rank | Provider | precision | coverage | metadata_integrity | story_quality | trust | weighted | final | caps |
|---|---|---|---|---|---|---|---|---|---|
| 1 | A | 9 | 9 | 10 | 9 | 10 | 9.3 | 9.3 | — |
| 2 | E | 8 | 2 | 10 | 9 | 8 | 7.25 | 7.25 | — |
| 3 | D | 5 | 10 | 5 | 7 | 8 | 6.75 | 6.75 | metadata_soft |
| 4 | C | 4 | 5 | 10 | 7 | 9 | 6.3 | 6.3 | — |
| 5 | B | 3 | 9 | 5 | 5 | 6 | 5.25 | 5.0 | metadata_soft, precision |
