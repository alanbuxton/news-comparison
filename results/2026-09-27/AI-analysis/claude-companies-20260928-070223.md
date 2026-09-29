# Companies Analysis — 20260928-070223

*Model: claude-opus-4-7 | Max articles per company per provider: 15*

*Provider labels were anonymised. See `decode-key-20260928-070223.json` to decode.*

---

```json
{
  "query_type": "companies",
  "providers": [
    {
      "label": "A",
      "axes": {
        "precision":         {"score": 9, "evidence": ["Alpek: all 6 articles are on-topic company news (S&P/BMV IPC inclusion, Q2 earnings, UK PET safeguard investigation)", "Coles: 13 clean articles on ACCC Kalgoorlie tribunal, electric supermarket opening, FY26 results", "Linklaters: all 8 articles are firm-specific (Wachtell hire, Paul Weiss hires, Webber Wentzel alliance end)", "0 mkt-report, 0 dup, 0 stale — extremely clean feed"]},
        "coverage":          {"score": 7, "evidence": ["answered: 35/42; 7 companies returned no results (BERKSHIRE LABELS, Fritz Foss, NUBIZ PLASTIC, SEERTECH SOLUTIONS, Sigma Chemtrade, TRICON DRY CHEMICALS, ZETA TECHNICAL SERVICES)", "Only 1 article each for CHEP, Dine Cartonnages, ICOF EUROPE, IMPACT RETAIL", "Spelling variant Klockner/Klöckner: only 38% overlap — inconsistent across spellings"]},
        "metadata_integrity": {"score": 10, "evidence": ["Header shows no-date: 0 (0%), stale: 0 (0%), no-publisher: 0 (0%)", "Every article carries a named publisher (Reuters, Bloomberg, Gulf News, ABC News, etc.)", "Every article carries a valid date within window"]},
        "story_quality":     {"score": 9, "evidence": ["Coles ABC News summary explains $1.1B profit and $235M underpayment provision distinctly", "Dominion Energy Reuters summary quotes $1 billion/year Virginia supplier program specifics", "Gandhar Oil summaries include specific figures (₹205.9 crore PAT, 689% YoY)", "Summaries are informative enough to decide clickthrough without boilerplate"]},
        "trust":             {"score": 10, "evidence": ["errors: 0 in header", "URLs point to legitimate publishers (reuters.com, bloomberg.com, gov.uk, abc.net.au)", "No suspicious URL patterns observed"]}
      },
      "verdict": "Cleanest feed in the run with excellent metadata and summaries, but leaves 7/42 companies unanswered and shows spelling-variant fragility on Klockner/Klöckner."
    },
    {
      "label": "B",
      "axes": {
        "precision":         {"score": 4, "evidence": ["BERKSHIRE LABELS: 20 results but nearly all are Berkshire Hathaway (Buffett succession, Berkshire Residential Investments MF1 acquisition) — wrong-entity FPs", "CHEP: results dominated by Cheplapharm/Sanofi pharma deal and Vishay CHEP thin-film resistors — wrong entities", "Fritz Foss: 20 results none about the entity (Rapidus arkivet, osapiens, GNU GPL Wikipedia)", "NUBIZ PLASTIC: results are National Plastic Industries, InterTabac, Nubo bio company — wrong entities", "Dine Cartonnages: Dine Brands Global (IHOP/Applebee's) dominates — wrong entity", "TRICON DRY CHEMICALS: results are Tricon Energy, Trinity Capital, Tri Polarcon — wrong entities"]},
        "coverage":          {"score": 9, "evidence": ["answered: 42/42 — every queried entity produced results", "Spelling variants Klockner/Klöckner both answered with 74% overlap", "But nominal coverage inflated by wrong-entity matches"]},
        "metadata_integrity": {"score": 5, "evidence": ["Header: no-date 0 (0%), stale 0 (0%), no-publisher 839 (100%) — every row missing publisher name", "Domain shown in parentheses (linkedin.com, finance.yahoo.com, investing.com) partly compensates", "dup: 21 (3%), mkt-report: 9 (1%) — minor noise"]},
        "story_quality":     {"score": 6, "evidence": ["Many summaries are informative (Borouge Q2 revenue $1.4B, Alpek EBITDA guidance)", "But numerous rows are boilerplate: 'Americas+1 212 318 2000 EMEA+44 20 7330 7500' repeated across Bloomberg entries", "CBS News entry '9/20: CBS Weekend News' is a video listing, not article substance"]},
        "trust":             {"score": 7, "evidence": ["errors: 0 in header", "No hallucinated URLs detected — links resolve to real domains", "But heavy reliance on investing.com regional mirrors (uk./za./ng./ca.) inflates apparent volume"]}
      },
      "verdict": "Maximal coverage and volume but seriously undermined by wrong-entity contamination on ambiguous names and universal missing-publisher metadata."
    },
    {
      "label": "C",
      "axes": {
        "precision":         {"score": 8, "evidence": ["Bloomberg: 20 articles, but several are about Clay (AI startup) and Smack Technologies — tangential name-drops rather than Bloomberg-focused", "Coles: 20 clean articles (krill oil removal, Flybuys change, Palantir contract ended)", "Constellium: 10 tightly on-topic articles (Q2 guidance raise, EOS partnership, Changchun JV exit)", "Linklaters: 20 articles all firm-specific (Verlinvest, Glencore, Wachtell dealmaker)"]},
        "coverage":          {"score": 5, "evidence": ["answered: 25/42 — 17 companies returned nothing (BERKSHIRE LABELS, CHARTER NEX FILMS, Dine Cartonnages, Fritz Foss, HPCL Mittal Energy, ICOF EUROPE, IMPACT RETAIL, Jindal Films, LUSHA SYSTEMS, Little Island Productions, NECTAR 360 SERVICES, NUBIZ PLASTIC, SEERTECH SOLUTIONS, Sigma Chemtrade, TRICON DRY CHEMICALS, Universal McCann, ZETA TECHNICAL SERVICES)", "Alpek: only 1 article; CHEP: only 1 article", "Spelling variants Klockner/Klöckner: 100% identical — spelling-insensitive"]},
        "metadata_integrity": {"score": 10, "evidence": ["Header: no-date 0, stale 0, no-publisher 0", "Every row shows named publisher (Reuters, Bloomberg, TheWrap, Yahoo Finance)", "Timestamps include precise datetime not just date"]},
        "story_quality":     {"score": 9, "evidence": ["Dominion-NextEra Reuters summary specifies $1B/year Virginia supplier program", "Coles Palantir story explains 3-year contract ending 2027", "ExxonMobil Venezuela story cites Petromonagas Orinoco Belt specifics", "Summaries consistently informative"]},
        "trust":             {"score": 10, "evidence": ["errors: 0", "URLs resolve to established publishers (reuters.com, bloomberg.com, cnbc.com, hollywoodreporter.com)", "No hallucinated content patterns detected"]}
      },
      "verdict": "High quality where it answers, with perfect metadata and spelling-insensitive matching, but leaves 40% of queried companies with no results at all."
    },
    {
      "label": "D",
      "axes": {
        "precision":         {"score": 4, "evidence": ["BERKSHIRE LABELS: 20 results but mostly label industry M&A tangentially mentioning Berkshire Labels (Asteria Group, Sopano) — broader-than-asked", "CHEP: Cheplapharm/Sanofi and CHS/OCP North America dominate — wrong entities", "Fritz Foss: 20 results are FOSS Group, Foss & Company tax equity, unrelated Foss/Fritz mentions — wrong entities", "NUBIZ PLASTIC: results are Medytox Nubiju, Nubo bio, InterTabac — wrong entities", "Sigma Chemtrade: results include Sigma Lithium, Sigma Healthcare, Trison Wells, ContextLogic gChem — wrong entities", "TRICON DRY CHEMICALS: results are EMCO, Tricon Energy, PetChem, StanChem — wrong entities"]},
        "coverage":          {"score": 9, "evidence": ["answered: 42/42", "Spelling variants Klockner/Klöckner: both answered, 38% overlap — largely different result sets ⚠", "Nominal coverage inflated by wrong-entity matches on ambiguous names"]},
        "metadata_integrity": {"score": 5, "evidence": ["Header: no-date 0 (0%), stale 0 (0%), no-publisher 840 (100%) — every article missing publisher", "Domain shown in URL parentheses (prnewswire.com, bloomberg.com, reuters.com) offers partial compensation", "dup: 34 (4%), mkt-report: 10 (1%)"]},
        "story_quality":     {"score": 6, "evidence": ["Deloitte summaries are substantive (Wavicle acquisition, ControlCatalyst.AI launch)", "Bloomberg entries reduced to headline+one-liner (e.g., Dangote refinery, Enbridge/Tallgrass)", "Some summaries are boilerplate page fragments rather than article substance"]},
        "trust":             {"score": 7, "evidence": ["errors: 0", "URLs resolve to real publisher/wire domains", "No hallucinated URLs detected but heavy volume of press-release aggregators (prnewswire, businesswire, globenewswire)"]}
      },
      "verdict": "Broad coverage at scale but riddled with wrong-entity matches on ambiguous names, universal missing-publisher metadata, and spelling-variant inconsistency."
    },
    {
      "label": "E",
      "axes": {
        "precision":         {"score": 8, "evidence": ["Constellium: both articles on-topic (Changchun JV exit, Q2 2026 results)", "Dominion Energy: 5 articles all specific (NextEra Virginia package, CVOW cost rise, Q2 AI demand)", "Linklaters: 4 articles all about FY26 record results and US expansion", "Gandhar Oil: 3 clean articles on AGM, Q1 FY27 results", "Impact Retail management buyout article is on-topic"]},
        "coverage":          {"score": 2, "evidence": ["answered: 18/42 — 24 companies returned zero results (ALPEK POLYESTER, Borouge, CHARTER NEX FILMS, CHEP, COLES, Deloitte, ExxonMobil, Fritz Foss, GREEN BAY PACKAGING, HAIER, HPCL Mittal Energy, ICOF EUROPE, International Paper, Klöckner Pentaplast, Little Island Productions, NECTAR 360, NUBIZ, RAINFOCUS, SEERTECH, SNOWFLAKE, Sigma Chemtrade, TRICON, Westrock, ZETA)", "Even answered companies get only 1-5 articles", "Spelling variants: answers 'Klockner Pentaplast' (1 article) but not 'Klöckner Pentaplast' (0) — spelling-fragile ⚠"]},
        "metadata_integrity": {"score": 10, "evidence": ["Header: no-date 0, stale 0, no-publisher 0", "Every row shows named publisher (Reuters, Fox News, City A.M., Benzinga)", "0 duplicates"]},
        "story_quality":     {"score": 8, "evidence": ["Constellium Q2 summary gives $2.7B revenue and $439M EBITDA specifics", "Linklaters summary details £2.48m PPEP and 11.6% pre-tax profit growth", "Dominion-NextEra summary quotes $2.25B bill credit pool and $100M workforce fund", "Summaries are analytical rather than boilerplate"]},
        "trust":             {"score": 8, "evidence": ["errors: 0", "URLs mostly resolve to legitimate sources", "One suspicious URL: reisingergooch.com regulatory docket review reads as niche/possibly synthesized", "Some URLs like industryanalysts.com and directorstalkinterviews.com are generic domains rather than article-specific"]}
      },
      "verdict": "Sparse but high-quality selective results with strong metadata; catastrophically low coverage answering fewer than half of queried companies."
    }
  ]
}
```

## Notes

The most striking pattern in this run is the trade-off between coverage and precision on ambiguous company names. Providers B and D achieved nominal 42/42 coverage but at heavy cost: queries like "BERKSHIRE LABELS", "CHEP", "Fritz Foss", "NUBIZ PLASTIC", "Sigma Chemtrade", and "TRICON DRY CHEMICALS" pulled back Berkshire Hathaway, Cheplapharm, unrelated Foss entities, Sigma Lithium/Healthcare, and Tricon Energy — wrong entities sharing only a name fragment. Providers A and C, by contrast, returned no results for many of these same queries, preserving precision but sacrificing coverage. Provider E takes this discipline furthest, answering only 18/42 but with tightly on-topic results.

Metadata integrity splits cleanly: A, C, and E have zero missing publishers; B and D have 100% missing publishers with domain shown only in the URL parenthesis — a real degradation even if the underlying domain is usually credible. On the Klockner/Klöckner spelling-variant test, C is perfectly spelling-insensitive (100% overlap), B is partial (74%), while A and D return substantially different result sets for the two spellings (38% each) and E answers only the unaccented form. No provider showed hallucinated URLs or errors, so trust separations are driven by URL-source quality and press-release aggregator reliance rather than fabrication.

---

## Recomputed scorecard (harness — authoritative)

Axis scores are the model's; `weighted`, `final`, caps and the ranking
are recomputed by the harness. If numbers in the raw output above
disagree, this table wins.

| Rank | Provider | precision | coverage | metadata_integrity | story_quality | trust | weighted | final | caps |
|---|---|---|---|---|---|---|---|---|---|
| 1 | A | 9 | 7 | 10 | 9 | 10 | 8.9 | 8.9 | — |
| 2 | C | 8 | 5 | 10 | 9 | 10 | 8.15 | 8.15 | — |
| 3 | E | 8 | 2 | 10 | 8 | 8 | 7.1 | 7.1 | — |
| 4 | B | 4 | 9 | 5 | 6 | 7 | 5.9 | 5.9 | metadata_soft |
| 5 | D | 4 | 9 | 5 | 6 | 7 | 5.9 | 5.9 | metadata_soft |

---

## Spelling-variant consistency (harness — authoritative)

Entities queried under two spellings that differ only by accent, case or
punctuation. Overlap is the share of returned URLs common to both.

**Klockner Pentaplast vs Klöckner Pentaplast**

| Provider | articles for “Klockner Pentaplast” | articles for “Klöckner Pentaplast” | shared URLs | overlap | read |
|---|---|---|---|---|---|
| Perplexity Agent | 4 | 7 | 3/8 | 38% | largely different results for the two spellings ⚠ |
| Perplexity Search | 20 | 20 | 17/23 | 74% | partially overlapping results |
| Syracuse | 10 | 10 | 10/10 | 100% | identical results — spelling-insensitive |
| Exa | 20 | 20 | 11/29 | 38% | largely different results for the two spellings ⚠ |
| Linkup | 1 | 0 | 0/1 | 0% | answers only "Klockner Pentaplast" ⚠ |
