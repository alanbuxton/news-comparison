# Industries Analysis — 20261025-174159

*Model: claude-opus-4-7 | Max articles per topic per provider: 20*

*Provider labels were anonymised. See `decode-key-20261025-174159.json` to decode.*

---

```json
{
  "query_type": "industries",
  "providers": [
    {
      "label": "A",
      "axes": {
        "precision":         {"score": 8, "evidence": ["CONSTRUCTION | Europe: 20/20 on-topic (Holcim Q3, Rexel Q3, German construction orders surge, Balfour Beatty Birkhill Wood substation)", "PAPER | Northern Europe: dense substantive coverage (Essity Q3, Billerud Q3, Norske Skog, UPM CFO change)", "LOGISTICS | Western Africa: strong relevance (CMA CGM congestion surcharges for Tema/Freetown/Monrovia, DHL Domestic Select in Nigeria, Uber exits Nigeria)", "mkt-report: 3 (1%), not-news: 0, only 1 dup out of 276 — very clean"]},
        "coverage":          {"score": 7, "evidence": ["answered: 18/20 topics", "Converter Foil | Northern America and Molasses | Oceania returned NO RESULTS", "Whey Ingredients | Northern Europe thin (4 articles) and LABORATORY | Africa thin (4 articles, mostly off-topic Transnet/Wabtec/UFlex)"]},
        "metadata_integrity": {"score": 10, "evidence": ["no-date: 0 (0%), stale: 0 (0%), no-publisher: 0 (0%) across 276 rows", "Every row carries publisher name e.g. 'The Manufacturer', 'Bloomberg', 'Investing.com'"]},
        "story_quality":     {"score": 8, "evidence": ["CONSTRUCTION | Europe Holcim Q3 summary gives EBIT growth and guidance upgrade specifics", "PE Resins | US Trinseo restructuring summary explains lender mediation", "LOGISTICS | Western Africa DHL Domestic Select summary describes product scope and pricing posture"]},
        "trust":             {"score": 8, "evidence": ["errors: 1 across 276 rows", "No hallucinated-looking URLs; mainstream domains (bloomberg.com, reuters.com, investing.com, prnewswire.com)", "LABORATORY | Africa shows weak topical fit (Transnet/Wabtec locomotive deal labeled as laboratory) — borderline mis-tagging rather than fabrication"]}
      },
      "verdict": "Clean metadata, strong publisher attribution, and substantive summaries across most topics, but two full misses and some off-topic padding in LABORATORY | Africa."
    },
    {
      "label": "B",
      "axes": {
        "precision":         {"score": 6, "evidence": ["HR SERVICES | Mid Atlantic: Hilb Group PA acquisition and US Bank/Verra Mobility fleet toll items are on-topic", "LOGISTICS | Western Africa: Maersk WAF reorganisation and Loadstar West Africa congestion are both relevant", "Whey Ingredients | Northern Europe: Arla Foods Ingredients clear-shake and DairyReporter WPC80 pricing items are on-topic", "Of what little was returned, essentially all articles are relevant — but sample sizes are tiny (1–3 per topic)"]},
        "coverage":          {"score": 1, "evidence": ["answered: 7/20 topics with 13 NO RESULTS RETURNED (CONVERTING AND FINISHING MACHINES, Cheese/US, Converter Foil, EXTERNAL MANUFACTURING, Film/CN, IT & TELECOM/N.Africa, LABORATORY/Africa, Molasses/Oceania, PACKAGING/Oceania, PAPER/N.Europe, PE Resins/US, PROFESSIONAL SERVICES/LATAM, SOLVENTS)", "Only 12 total articles across 20 topics"]},
        "metadata_integrity": {"score": 9, "evidence": ["no-date: 0, stale: 0, no-publisher: 0 across the 12 rows returned", "Publishers named (PrintWeek India, The Hindu BusinessLine, DairyReporter, GlobeNewswire)"]},
        "story_quality":     {"score": 7, "evidence": ["Packaging Boxes | IN: South Indian 20% hike summary quantifies kraft price moves from Rs 30/kg to Rs 38.50/kg", "LIQUIDS | Southern Africa Henkel 75-year summary explains sectors served", "Road Freight | Europe TrasportoEuropa item cites Q1 2026 contract-vs-spot divergence"]},
        "trust":             {"score": 2, "evidence": ["errors: 118 across 20 topics — overwhelming failure rate", "Multiple topics (PROFESSIONAL SERVICES/LATAM 12 errors, Cheese/US 9 errors, PE Resins/US 8 errors) returned nothing but errors", "Operational unreliability dominates"]}
      },
      "verdict": "When it returns something it's clean and relevant, but a 118-error, 7/20 answered run is essentially unusable."
    },
    {
      "label": "C",
      "axes": {
        "precision":         {"score": 7, "evidence": ["CONSTRUCTION | Europe: tightly relevant (Inwido Q3 order growth, VINCI Iberian data center, BAM/A.Hak acquisition, Elevion/Techem)", "Film | CN: on-topic but heavily non-English (Chinese text in rows 1,2,3,4,7,12,13,15,17,19,20)", "LABORATORY | Africa: strong fit (SANAS tenders, Pwani University calibration, Alfred H Knight Maputo lab, KEMRI tenders)", "PROFESSIONAL SERVICES | LATAM: mixed — Sibos LatAm, Latin Lawyer M&A, Latham ranking are on-topic but ~8 of 20 rows are Spanish/Portuguese which stresses the 'English language' TP rule"]},
        "coverage":          {"score": 10, "evidence": ["answered: 20/20 topics", "Converter Foil | Northern America and Molasses | Oceania both answered where A failed", "Consistent 20 articles per topic across the run"]},
        "metadata_integrity": {"score": 4, "evidence": ["no-publisher: 400 (100%) — every row flagged", "Rubric treats no-publisher at ~half the severity of no-date and 'should not push this axis below about 5' alone — but combined with 100% rate (not a modest share) a 4 is warranted", "Domains are visible (eurogypsum.org, vinci.com, bam.com) so credibility is recoverable but degraded"]},
        "story_quality":     {"score": 7, "evidence": ["CONSTRUCTION | Europe BAM/A.Hak summary names deal rationale and sector focus", "LABORATORY | Africa Wallace Instruments summary explains Cote d'Ivoire natural-rubber focus", "Film | CN rows carry long raw Chinese text that an English-reading user cannot evaluate without translation"]},
        "trust":             {"score": 8, "evidence": ["errors: 0 across 400 rows", "URLs look legitimate (vinci.com, bam.com, reuters.com, spglobal.com)", "No suspicious patterns detected"]}
      },
      "verdict": "Full topic coverage and zero errors, but the universal missing-publisher pattern and heavy non-English content in Chinese/LATAM topics are real usability costs."
    },
    {
      "label": "D",
      "axes": {
        "precision":         {"score": 2, "evidence": ["mkt-report: 98 (24%) and not-news: 27 (7%) — nearly a third of 400 rows are flagged noise", "Molasses | Oceania: 14 of 20 are market-report landing pages (Spherical Insights, IndexBox, Future Market Insights, Fairfield) plus 5 not-news LinkedIn posts — classic SEO dreck dominates", "SOLVENTS: 15 of 20 are market-size reports (openpr.com, businessmarketinsights.com, mordorintelligence.com)", "CONVERTING AND FINISHING MACHINES | S.Asia: multiple Chinese/Japanese translation pages, Indian Hindi listings, and 8 market-reports — e.g. 'Growth of the Converting Equipment Market Fueled by Rising' from openpr.com", "Packaging Boxes | IN: 7 rows are Justdial directory listings (not news) — e.g. 'Packaging Box in Bilaspur-chhattisgarh'"]},
        "coverage":          {"score": 9, "evidence": ["answered: 20/20 topics", "Returned 20 articles per topic including Molasses | Oceania and Converter Foil | N.America"]},
        "metadata_integrity": {"score": 4, "evidence": ["no-publisher: 400 (100%) across every row", "no-date: 0 and stale: 0 are solid, but 100% missing publisher degrades the data uniformly", "Several rows are domain-only (linkedin.com, openpr.com, giiresearch.com) — these domains do not help readers trust the content"]},
        "story_quality":     {"score": 4, "evidence": ["Many 'summaries' are just raw table-of-content fragments or boilerplate ('Press release from: The Business Research Company')", "Packaging Boxes | IN Justdial entries read like SEO ad copy, not article summaries", "Some genuinely useful rows exist (Road Freight Eurostat, Golden Triangle Polymers cracker summary) but drown in boilerplate"]},
        "trust":             {"score": 5, "evidence": ["errors: 0", "URLs like 'linkedin.com/pulse/...' and 'openpr.com' and 'giiresearch.com' are legitimate but low-signal; prompts user to question source selection", "No evidence of hallucinated facts, but Justdial listings presented as topical news (e.g. 'Market research indicates that the growth of the Indian packaging box industry will be further accelerated') suggest poor source hygiene"]}
      },
      "verdict": "Full topic coverage but swamped with market-report landing pages, LinkedIn posts, directory listings and SEO fluff — the 24% mkt-report share plus 7% not-news share make this a precision disaster."
    },
    {
      "label": "E",
      "axes": {
        "precision":         {"score": 9, "evidence": ["CONSTRUCTION | Europe: 9/9 tightly on-topic (Holcim 2027 outlook, Dutch hybrid heat pump mandate, VINCI Energies Vattenfall contract, EU Commission reasoned opinions on NBRPs)", "LOGISTICS | Western Africa: 13/13 tightly on-topic (Maersk WAF reorg via Algeciras, NIPOST Abuja enforcement, Lekki Port HMM-ONE service, Bolt Send 6M deliveries)", "Whey Ingredients | Northern Europe: 11/11 relevant (Vesper WPC80 pricing, FrieslandCampina Borculo expansion, Arla Videbæk heat-system)", "mkt-report: 2 (1%), not-news: 0, dup: 0 across 148 rows"]},
        "coverage":          {"score": 9, "evidence": ["answered: 20/20 topics including the ones A missed (Converter Foil 3 articles, Molasses | Oceania 5 articles)", "Fewer articles per topic (3–13 range) but every topic has something; LABORATORY | Africa only 4 and Converter Foil only 3 — thin on edge topics"]},
        "metadata_integrity": {"score": 10, "evidence": ["no-date: 0, stale: 0, no-publisher: 0 across 148 rows", "Every row carries both date and named publisher (Cyprus Mail, Reuters, PrintWeek, DairyReporter, Vesper)"]},
        "story_quality":     {"score": 9, "evidence": ["Packaging Boxes | IN kraft paper summary quantifies the 22-25% rise and ₹7-10/kg impact and names WICMA", "Whey Ingredients | N.Europe FrieslandCampina summary names Borculo WPI capacity doubling and €90m commitment", "LOGISTICS | W.Africa Maersk WAF summary names affected services (WAF1/3/5/6) and timing (December 2026)"]},
        "trust":             {"score": 9, "evidence": ["errors: 0 across 148 rows", "URLs are mainstream and legitimate (reuters.com, aljazeera.com, foodbusinessnews.net, abc.net.au)", "LABORATORY | Africa row 1 (BioSpectrum Asia 'Life science industry in South Africa') self-identifies as a March 2024 interview but is listed with October 2026 date — a single provenance flag"]}
      },
      "verdict": "Lowest article volume but the cleanest returns — strong precision, zero errors, zero missing metadata, informative summaries, and nothing was skipped."
    }
  ]
}
```

## Notes

The most striking pattern across the run is the inverse relationship between volume and precision. Provider D delivered the maximum 400 articles with 24% market-report pollution and 100% missing publishers, including entire topic lists (Molasses | Oceania, SOLVENTS, Packaging Boxes | IN with Justdial directory entries) that read as SEO landing pages rather than news. Provider C also returned 400 rows with 100% missing publishers but was dramatically cleaner on topicality — the publisher gap is a formatting/pipeline issue, not a judgment issue, and the Chinese-language dominance of its Film | CN topic (and partial Spanish/Portuguese in LATAM) is a usability drag for an English-only consumer. Provider B's 118 errors across 20 topics is the single most alarming operational signal in the run.

Provider E's strength is restraint: 148 articles total, zero errors, zero missing dates or publishers, zero duplicates, and summaries that typically quantify the story (percentage moves, named plants, dollar figures). Its honest weaknesses are thin coverage on hard topics (3 articles on Converter Foil, 4 on LABORATORY | Africa) and one dateline problem — the BioSpectrum Asia row stamped October 2026 but describing a 2024 interview. Provider A is similarly disciplined on metadata but took two topic DNFs (Converter Foil, Molasses | Oceania) and showed topical drift on LABORATORY | Africa where locomotive-services deals were labeled as lab coverage.

---

## Recomputed scorecard (harness — authoritative)

Axis scores are the model's; `weighted`, `final`, caps and the ranking
are recomputed by the harness. If numbers in the raw output above
disagree, this table wins.

| Rank | Provider | precision | coverage | metadata_integrity | story_quality | trust | weighted | final | caps |
|---|---|---|---|---|---|---|---|---|---|
| 1 | E | 9 | 9 | 10 | 9 | 9 | 9.15 | 9.15 | — |
| 2 | A | 8 | 7 | 10 | 8 | 8 | 8.1 | 8.1 | — |
| 3 | C | 7 | 10 | 4 | 7 | 8 | 7.3 | 7.0 | metadata_soft |
| 4 | D | 2 | 9 | 4 | 4 | 5 | 4.45 | 4.45 | metadata_soft, precision |
| 5 | B | 6 | 1 | 9 | 7 | 2 | 5.0 | 4.0 | trust |
