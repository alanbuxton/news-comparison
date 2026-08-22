# Industries Analysis — 20260822-181459

*Model: claude-opus-4-7 | Max articles per topic per provider: 15*

*Provider labels were anonymised. See `decode-key-20260822-181459.json` to decode.*

---

```json
{
  "query_type": "industries",
  "providers": [
    {
      "label": "A",
      "axes": {
        "precision":         {"score": 6, "evidence": ["CONSTRUCTION|Europe returned strong on-topic items like 'PORR awarded contract for X-FAB semiconductor factory in Germany' and Welsh wind farm contract, but also off-topic 'JD.com offers concessions in EU probe of Ceconomy takeover' (retail M&A, not construction)", "Cheese/Milk Powders|US included 4 MKT-REPORT items and off-topic 'NH gets another $7 million from PFAS drinking water settlements' — chemical litigation, not food ingredients", "Film|CN (BOPP/BOPET/PE) polluted by cinema-adjacent 'Hollyland lance le Pyro 5 4K' and 'HSG Emerges as Leading Bidder to Buy Stake in Leica Camera' — wrong-entity film", "mkt-report: 44 (16%) across the run inflates volume with market-research SEO pages"]},
        "coverage":          {"score": 9, "evidence": ["answered: 20/20 topics with 270 articles total", "Molasses|Oceania returned only 1 article and it was a MKT-REPORT, and Converter Foil|NA only 1 article — thin but present", "PAPER|Northern Europe well-covered with Metsä, Stora Enso, Valmet, Södra actual news"]},
        "metadata_integrity": {"score": 10, "evidence": ["no-date: 0 (0%), stale: 0 (0%), no-publisher: 0 (0%), dup: 1 (0%) per header"]},
        "story_quality":     {"score": 7, "evidence": ["PAPER|Northern Europe summaries like Metsä €25M Muoto investment and Stora Enso Veitsiluoto closure give actionable detail", "Some items truncated ('Land O'Lakes Expands Tulare Dairy Protein Production' one-line summary)", "Market report items give numeric detail but are boilerplate SEO"]},
        "trust":             {"score": 9, "evidence": ["errors: 0 per header", "Sources span reputable outlets (Reuters, AP, SCMP, Business Standard, Mining Weekly) with plausible URLs"]}
      },
      "verdict": "Broad, dated, well-sourced coverage with clean metadata, but ~16% market-report noise and recurring wrong-entity matches (JD.com/Ceconomy in Construction, Leica in Film-CN) dilute precision."
    },
    {
      "label": "B",
      "axes": {
        "precision":         {"score": 9, "evidence": ["CONSTRUCTION|Europe: Eurostat construction production, S&P Global UK Construction PMI, Cemex EU cartel — all strictly on-topic strategic developments", "Film|CN (BOPP/BOPET/PE): ChemAnalyst BOPET price drop, Zhonglun New Materials BOPP line commissioning, China packaging rules — all match the plastic-film intent", "Whey|Northern Europe: Arla-DMK merger, DMK €26M Edewecht WPC80 plant, Vivici €12.5M EIC grant — precisely on-intent", "mkt-report: only 2 (1%) across the entire run"]},
        "coverage":          {"score": 8, "evidence": ["answered: 20/20 topics, 167 articles", "HR SERVICES|Mid Atlantic only 4 articles and Molasses|Oceania only 3, but each is genuinely relevant (Maryland FAMLI, Queensland sugar terminals)", "Converter Foil|NA covered with Ball Corp earnings, Century Aluminum restart, tariff proclamations"]},
        "metadata_integrity": {"score": 10, "evidence": ["no-date: 0 (0%), stale: 0, no-publisher: 0, dup: 0 per header"]},
        "story_quality":     {"score": 9, "evidence": ["Road Freight|Europe: 'European road-freight benchmark showed contract rates at 148.0 index points, up 7.9 points quarter on quarter' — quantified and decision-ready", "PE Resins|US: 'US LDPE Prices Fall 16.54% in Early July 2026' with cited drivers", "Summaries consistently include figures, dates and named actors"]},
        "trust":             {"score": 9, "evidence": ["errors: 0", "Sources include Reuters, Eurostat, European Commission, S&P Global, Chicago Fed, FDA, IRU — high-credibility mix"]}
      },
      "verdict": "Small article counts per topic but exceptionally clean: on-topic, informative summaries, credible sources and zero metadata defects; the only weakness is thinner volume than some rivals."
    },
    {
      "label": "C",
      "axes": {
        "precision":         {"score": 6, "evidence": ["Molasses|Oceania (sugar & sweeteners intent) is dominated by Fiji sugar-industry stories (Lautoka mill, FSC privatisation) — relevant to sugar sector but geographically Fiji/Oceania edge cases; also includes off-region 'Indonesian govt tightens refined sugar imports'", "LOGISTICS|Western Africa mostly on-topic (Lekki Port, CMA CGM KORA EXPRESS, MSC feeder) but includes IndexBox market report", "Film|CN heavily polluted by ag-investor Chinese-language pages ('复合集流体PP基膜国产化','德冠新材') and 4 duplicates flagged", "HR SERVICES|Mid Atlantic tightly on-topic (Maryland FAMLI, Alliant/Nava, Aramark/Penn Medicine direct plan)"]},
        "coverage":          {"score": 10, "evidence": ["answered: 20/20 with 400 articles, ~20 per topic across the board", "LABORATORY|Africa returned real items like Talbot SANAS-accredited lab, UNBS Uganda food-safety labs, Africa CDC procurement notice"]},
        "metadata_integrity": {"score": 5, "evidence": ["no-publisher: 400 (100%) — every row shows only a domain in parentheses; publisher name never surfaced", "no-date: 0, stale: 0, dup: 7 (2%) — dates fully present so the severe axis is intact", "Per the rubric, no-publisher is the lesser defect but at 100% it is still material"]},
        "story_quality":     {"score": 6, "evidence": ["Summaries often show raw HTML-scrape artefacts: 'Production in construction down by 1.3% in the euro area and by 1.0% in the EU - Euro indicators - Eurostat ... down by 1.3% in ...'", "Chinese-language rows in Film|CN show minimal English summary, forcing click-through", "Better items (e.g. Emirates NBD/HSBC Egypt, Nigeria NPERA law) do carry decision-ready content"]},
        "trust":             {"score": 8, "evidence": ["errors: 0", "URLs point to real domains (ec.europa.eu, reuters.com, businessday.ng, mysteel.com); no hallucination pattern"]}
      },
      "verdict": "Very deep coverage with 20 articles per topic, but the universal missing-publisher tag, scraped/truncated summaries and pockets of foreign-language or wrong-entity noise (Film|CN Chinese ag-invest pages) drag down usability."
    },
    {
      "label": "D",
      "axes": {
        "precision":         {"score": 3, "evidence": ["mkt-report: 143 (36%) — over a third of results are market-research/SEO landing pages, far beyond the ≤2/topic tolerance", "Molasses|Oceania: 17 of 20 items are MKT-REPORT (LinkedIn/openPR/IndexBox forecast pages), essentially no real news", "SOLVENTS: 15 of 20 items are MKT-REPORT (Ketones Market Size, Ethyl Acetate Market forecasts)", "Converter Foil|NA mixes genuine Reuters items with LinkedIn 'Aluminium Foil Market Regional Performance' SEO posts"]},
        "coverage":          {"score": 10, "evidence": ["answered: 20/20, 400 articles, 20 per topic uniformly"]},
        "metadata_integrity": {"score": 5, "evidence": ["no-publisher: 400 (100%) — publisher name absent on every row (only domain shown)", "no-date: 0, stale: 0, dup: 2 (0%) — the severe axis is clean", "Consistent with rubric: universal no-publisher caps this axis around 5"]},
        "story_quality":     {"score": 4, "evidence": ["Cheese/Milk Powders|US: 'Chr. Hansen Holding, Fonterra, DowDuPont, DSM, Archer Daniels Midland, Saputo, Arla Foods, and CSK Food are key players' — vendor list, no news", "Packaging|Oceania item 1 summary is a bare company list ('Smurfit Westrock, International Paper, DS Smith…')", "Molasses|Oceania rows return market-report tables and CAGR sentences instead of story text"]},
        "trust":             {"score": 7, "evidence": ["errors: 0", "URLs resolve to real market-research domains, but heavy LinkedIn-pulse and openPR reliance ('linkedin.com/pulse/...','openpr.com/news/...') reduces editorial trust"]}
      },
      "verdict": "Uniform 20-per-topic depth is undercut by 36% market-report share, universal missing publishers and boilerplate 'key players' summaries — technically comprehensive but low signal for a strategic reader."
    },
    {
      "label": "E",
      "axes": {
        "precision":         {"score": 7, "evidence": ["IT & TELECOM|Northern Africa returned strong on-topic items: MTN Ghana 80-site expansion, Ethio Telecom-Huawei partnership, Ookla 5G North Africa review", "Cheese/Milk Powders|US: Cowsmo 'Big 7 pivot to protein and cheese' and DairyNews 'Record Cheese Production' are on-intent", "Only 4 MKT-REPORT items across 34 articles (12%)"]},
        "coverage":          {"score": 3, "evidence": ["answered: 12/20 topics — 8 topics returned '[NO RESULTS RETURNED ⚠]' including CONVERTING AND FINISHING MACHINES|Southern Asia, Film|CN, HR SERVICES|Mid Atlantic, LABORATORY|Africa, LIQUIDS|Southern Africa, LOGISTICS|Western Africa, Molasses|Oceania, SOLVENTS", "Where it did answer, article counts are thin (Whey|Northern Europe: 1 article; PROFESSIONAL SERVICES|LATAM: 1 article; Road Freight|Europe: 1 article)"]},
        "metadata_integrity": {"score": 10, "evidence": ["no-date: 0, stale: 0, no-publisher: 0, dup: 0 per header"]},
        "story_quality":     {"score": 7, "evidence": ["IT&TELECOM summaries specify numeric detail: 'MTN Ghana announced a $1.1 billion investment plan to construct 80 new network sites'", "Arla-DMK Whey item gives strategic context", "Some entries are aggregator/index pages ('Industry News & Developments Archives - Page 2 of 21')"]},
        "trust":             {"score": 4, "evidence": ["errors: 3 per header — non-trivial rate over only 34 articles", "PE Resins|US errors surfaced, and the two visible PE-Resins items are both MKT-REPORT (ChemOrbis landing, Precedence US Polyolefin)"]}
      },
      "verdict": "When it answers it stays close to the intent with clean metadata, but 40% of topics return nothing and 3 errors on a small base make it unreliable as a primary source."
    },
    {
      "label": "F",
      "axes": {
        "precision":         {"score": 2, "evidence": ["mkt-report: 105 (58%) — the majority of results are market-research SEO pages (MarketDataForecast, FortuneBusinessInsights, MarketsandMarkets, Precedence)", "SELF-REPORTED: 59% of its 181 articles scored below 0.2; HR SERVICES|Mid Atlantic answered with 9 articles best-scored only 0.069 — it knew the topic was poor", "LOGISTICS|Western Africa polluted by wrong-entity 'ISWAP logistics suppliers' Boko Haram counter-insurgency stories ('Troops Arrest Two Suspected ISWAP Logistics Suppliers In Borno')", "Molasses|Oceania is 5 of 6 MKT-REPORT plus a CELH zero-sugar energy-drink piece — nothing on Oceania sugar/molasses supply"]},
        "coverage":          {"score": 6, "evidence": ["answered: 20/20 but many topics are thin: LABORATORY|Africa 1 article, Packaging|Oceania 4, Converter Foil|NA 2", "Volume padded by market reports rather than real coverage of the queried region/industry"]},
        "metadata_integrity": {"score": 3, "evidence": ["no-publisher: 181 (100%) — universal", "no-date: 16 (9%) — the severe defect: rows like 'Lathe Machine Market Size, Share' and 'LFZ, Firm Announce Joint Venture' carry [NO DATE ⚠]", "dup: 5 (3%) including 5 duplicates of the ICIS rLDPE pricing release in PE Resins|US"]},
        "story_quality":     {"score": 3, "evidence": ["Many summaries are navigation/site-map text: 'Read + Brands - FreightWaves - American Shipper - Modern Shipper' (Road Freight|Europe Amazon LTL item)", "HR SERVICES rows include 'BMC Site Map' and generic ResearchGate abstracts, unusable for a business reader", "Facebook/Instagram/LinkedIn social-post rows in Converting Machines and HR SERVICES"]},
        "trust":             {"score": 3, "evidence": ["errors: 0 in header, but LOGISTICS|Western Africa is dominated by military/insurgency stories that were retrieved on a keyword match to 'logistics suppliers' — indicates weak entity resolution", "Provider self-reported that a whole topic (HR SERVICES) was answered with 9 items it scored ≤0.069 — returning results it knew were poor"]}
      },
      "verdict": "High mkt-report share, universal missing publishers, 9% missing dates, wrong-entity 'ISWAP logistics' matches and self-flagged low-quality answers make this the least trustworthy result set for a strategic reader."
    }
  ]
}
```

## Notes

The run splits cleanly into two shapes. Providers A and B behave like curated newsrooms: dated, publisher-named, mostly on-intent, with A wider (270 articles, 16% market-report) and B narrower but cleaner (167 articles, 1% market-report, uniformly quantified summaries). Providers C and D fill exactly 20 rows per topic and pay for it with a universal missing-publisher tag and, for D, a 36% market-report share plus vendor-list "summaries." E is a coverage disaster (8 of 20 topics empty) but what it does return is on-topic. F is the worst signal-to-noise here: 58% market reports, 9% no-date, wrong-entity "ISWAP logistics" hits in Western Africa, social-post rows in HR SERVICES, and it self-reported that 59% of its own articles scored below 0.2 with an entire topic answered from items it scored ≤0.069.

Where the axes look strong for A and B, the honest weaknesses remain: A drags cinema/retail-M&A into Construction and Film-CN, and it carries 44 market-report rows; B's per-topic counts are modest (HR SERVICES only 4, Molasses only 3), so a caller who needs bulk exploration rather than a briefing will find it thin. C's 400-article depth is real but the scraped, truncated summary style ("Down by 1... in the EU ... 2026 edition of Key figures") means a reader still has to click through, and its Film-CN topic pulls in Chinese-language ag-investor pages that a US/EU analyst can't act on.

---

## Recomputed scorecard (harness — authoritative)

Axis scores are the model's; `weighted`, `final`, caps and the ranking
are recomputed by the harness. If numbers in the raw output above
disagree, this table wins.

| Rank | Provider | precision | coverage | metadata_integrity | story_quality | trust | weighted | final | caps |
|---|---|---|---|---|---|---|---|---|---|
| 1 | B | 9 | 8 | 10 | 9 | 9 | 8.95 | 8.95 | — |
| 2 | A | 6 | 9 | 10 | 7 | 9 | 7.8 | 7.8 | — |
| 3 | C | 6 | 10 | 5 | 6 | 8 | 6.95 | 6.95 | metadata_soft |
| 4 | D | 3 | 10 | 5 | 4 | 7 | 5.45 | 5.0 | metadata_soft, precision |
| 5 | E | 7 | 3 | 10 | 7 | 4 | 6.2 | 4.0 | trust |
| 6 | F | 2 | 6 | 3 | 3 | 3 | 3.25 | 3.25 | metadata_hard, trust, precision |

---

## Provider self-reported relevance (harness — authoritative)

What each provider said about its own results. Never used to filter them. "Weak items" are queries the provider answered while scoring every article it returned below 0.2.

| Provider | scored | median | weak items | read |
|---|---|---|---|---|
| Syracuse | 0/270 | — | 0 | returns no relevance score — caller cannot triage its results |
| Perplexity Agent | 0/167 | — | 0 | returns no relevance score — caller cannot triage its results |
| Exa | 0/400 | — | 0 | returns no relevance score — caller cannot triage its results |
| Perplexity Search | 0/400 | — | 0 | returns no relevance score — caller cannot triage its results |
| Linkup | 0/34 | — | 0 | returns no relevance score — caller cannot triage its results |
| Tavily | 181/181 | 0.162 | 1 | 59% of its results scored below 0.2; 1 items answered with 9 articles it scored entirely below 0.2 ⚠ |
