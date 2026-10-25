# Companies Analysis — 20261025-174159

*Model: claude-opus-4-7 | Max articles per company per provider: 20*

*Provider labels were anonymised. See `decode-key-20261025-174159.json` to decode.*

---

```json
{
  "query_type": "companies",
  "providers": [
    {
      "label": "A",
      "axes": {
        "precision":         {"score": 7, "evidence": ["Bloomberg, Deloitte, Linklaters, Dominion Energy returned clean company-specific headlines (Deloitte: 'FRC fines Deloitte £6.05m over Go-Ahead Group audit lapses')", "Coles had 1 MKT-REPORT flag (gymnast Ali Coles unrelated to supermarket)", "ExxonMobil, Snowflake, CBS News sets had 5 dups total but very few wrong-entity", "Jindal Films: AssetBuilt real-estate asset-sale listing is thin name-drop"]},
        "coverage":          {"score": 7, "evidence": ["answered 26/42 companies; missed ALPEK POLYESTER, BERKSHIRE LABELS, CHARTER NEX FILMS, CHEP, Dine Cartonnages, Fritz Foss, HPCL Mittal Energy, ICOF EUROPE, IMPACT RETAIL, NUBIZ PLASTIC, SEERTECH SOLUTIONS, Sigma Chemtrade, TRICON DRY CHEMICALS, Universal McCann, ZETA TECHNICAL SERVICES", "Klockner/Klöckner Pentaplast spelling pair: identical 100% overlap (3 vs 3)", "Strong depth on returned entities (20 articles each for Bloomberg, Borouge, Coles, Deloitte, ExxonMobil, Snowflake, International Paper, Westrock, Linklaters, Mistral AI, Dominion, Haier)"]},
        "metadata_integrity": {"score": 10, "evidence": ["Header: no-date 0 (0%), stale 0 (0%), no-publisher 0 (0%)", "Every row names a publisher (e.g., 'The Irish Times (irishtimes.com)', 'Plastics News (plasticsnews.com)')", "dup 5 (2%) is minor"]},
        "story_quality":     {"score": 8, "evidence": ["Snippets informative and specific (Constellium: 'Q2 revenue rising 31% year over year to $2.75 billion and adjusted EBITDA reaching $439 million')", "Borouge dividend story quotes '$656 million, equivalent to 8.1 fils per share'", "Some rows truncate mid-sentence ('Borouge Opens $ 105M Polypropylene Facility in Austria.' repeated as title+body)"]},
        "trust":             {"score": 9, "evidence": ["errors: 0 header count", "URLs resolve to real outlets (prnewswire.com, businesswire.com, bloomberg.com, reuters sources)", "No sign of hallucinated URLs across Bloomberg/Deloitte/ExxonMobil samples"]}
      },
      "verdict": "Clean metadata and tight on-topic retrieval for the companies it answers, but it refuses the long tail — 16 of 42 entities returned nothing."
    },
    {
      "label": "B",
      "axes": {
        "precision":         {"score": 6, "evidence": ["Of 16 articles returned, most are on-topic (Constellium: 'Scrap Shortage Puts Constellium Recycling Plans at Risk'; Mistral: 'Mistral raises €3B as sovereign AI becomes big business')", "Jindal Films CEO interview is a vendor profile piece but names the queried company", "Regus set gave 4 clean IWG/Regus openings"]},
        "coverage":          {"score": 1, "evidence": ["answered 7/42 companies; 35 entities returned nothing including Bloomberg, Deloitte, ExxonMobil, Coles, Haier, Linklaters, Snowflake, Westrock, International Paper, CBS News", "Spelling pair: Klockner Pentaplast 0 vs Klöckner Pentaplast 2 — answered only one spelling", "errors: 201 header count indicates systemic retrieval failure"]},
        "metadata_integrity": {"score": 10, "evidence": ["Header: no-date 0, stale 0, no-publisher 0", "Each row cites a named publisher ('Utility Dive (utilitydive.com)', 'TechCrunch (techcrunch.com)')"]},
        "story_quality":     {"score": 8, "evidence": ["Summaries are concise and informative (Dominion: 'Dominion raised the estimated cost of its 2.6-GW Coastal Virginia Offshore Wind project by about $288 million')", "Snowflake breach writeup provides specifics ('used previously stolen credentials to access customer accounts without MFA')"]},
        "trust":             {"score": 3, "evidence": ["errors: 201 header count — ALPEK 8, Deloitte 11, HAIER 10, Universal McCann 10, Linklaters 10, Westrock 10 errors reported", "Zero articles for Bloomberg/Deloitte/ExxonMobil despite 6-11 errors each suggests infrastructure failure, not hallucination"]}
      },
      "verdict": "When it answers, metadata and summaries are clean, but 201 errors and only 7 of 42 entities answered make it unusable as a news tool."
    },
    {
      "label": "C",
      "axes": {
        "precision":         {"score": 4, "evidence": ["BERKSHIRE LABELS: all 20 rows are wrong entity — Berkshire Hathaway/Residential/Grey/Financial Services, Bershka clothing, Barron McCann; zero are about the UK label printer", "SEERTECH SOLUTIONS: 20 rows are SEERS Technology (medical wearables), SurvTech Solutions, Seer Inc proteomics — none match queried entity (3 dups too)", "LUSHA SYSTEMS: on-target with Italian Garante fine coverage", "ICOF EUROPE: returned CoFICAB (Tunisian cable), iCO Products fire nozzles, ICOF Dominican training institute — wrong entities, 2 dups"]},
        "coverage":          {"score": 8, "evidence": ["answered 42/42 companies — full coverage attempt", "Spelling pair: Klockner 20 vs Klöckner 20 but only 60% URL overlap — same entity returned different sets", "Coverage inflated: many 'answered' rows for obscure entities (Fritz Foss, NUBIZ PLASTIC, ZETA TECHNICAL SERVICES, SEERTECH) are wrong-entity filler"]},
        "metadata_integrity": {"score": 4, "evidence": ["Header: no-publisher 840 (100%) — every single row flagged NO PUBLISHER ⚠, publisher recoverable only from domain (einpresswire.com, linkedin.com, prnewswire.com)", "no-date 0, stale 0 — dates clean", "dup 14 (2%), not-news 2 — low"]},
        "story_quality":     {"score": 6, "evidence": ["Snippets often raw-scraped boilerplate (Bloomberg Technology row: 'As technology continues to reshape financial services, regulators and policy setters are embarking on a range of digital-finance initiatives')", "Many headlines include junk tails ('|CHEMOURS USD 450 mn package agreed in PFAS deal...')", "Some clean summaries (Deloitte Risk Clarity launch; Snowflake convertible notes)"]},
        "trust":             {"score": 5, "evidence": ["errors: 0", "No hallucinated URLs detected in spot checks", "But precision collapse on BERKSHIRE LABELS/SEERTECH/ICOF/Fritz Foss — provider returned wrong-entity content without warning, which is a trust failure"]}
      },
      "verdict": "Answers everything but stuffs the long tail with wrong-entity results, strips every publisher name, and leaves raw-scraped boilerplate in summaries."
    },
    {
      "label": "D",
      "axes": {
        "precision":         {"score": 3, "evidence": ["IMPACT RETAIL: 20 rows are supermarket/retail industry roundups and FMCG newsletters — zero are about the Leicester cosmetics marketing agency; 2 dups, 1 not-news", "Dine Cartonnages: 20 rows are Dine Brands IHOP/Applebee's, Duni AB napkins, FMCG retail roundups — zero about French carton manufacturer; 6 dups", "SEERTECH SOLUTIONS: 20 rows are M&A newsletters, Seer Inc proteomics, SEERS Technology Korea — none match the queried entity; 2 dups", "Fritz Foss, NUBIZ PLASTIC, Little Island Productions, TRICON DRY CHEMICALS similarly filled with aggregator/newsletter noise; Dine 6 dups, ICOF 2 dups + 1 not-news"]},
        "coverage":          {"score": 7, "evidence": ["answered 42/42 companies but much of the long tail is wrong-entity filler", "Spelling pair: Klockner 20 vs Klöckner 20 at 60% overlap", "Core blue-chips (Bloomberg, Deloitte, Linklaters, ExxonMobil, Dominion, Snowflake) got substantive 20-article results"]},
        "metadata_integrity": {"score": 4, "evidence": ["Header: no-publisher 840 (100%) — every row flagged NO PUBLISHER ⚠, recoverable only from domain (law360.com, cfotech.news, linkedin.com)", "no-date 0, stale 0 — dates clean", "dup 43 (5%) higher than peers, mkt-report 4, not-news 12"]},
        "story_quality":     {"score": 5, "evidence": ["Many rows are aggregator table-of-contents dumps (Impact Retail row: 'Debenhams posts its first profit in five years—but the £28.3 million includes a large non-cash effect' then 'Frasers takes control of HUGO BOSS')", "Linklaters row for 'Applied Intelligence' is a navigation menu scrape", "Mixed with clear quotes elsewhere (Haier: 'Carrier Global completed the sale of its Commercial Refrigeration business to Haier Group for a stated transaction value of $775 million')"]},
        "trust":             {"score": 5, "evidence": ["errors: 0", "No hallucinated URLs seen", "But self-attributed labels like 'Nubiz Plastic' tagged on InterTabac Dortmund trade-show stories, and SEERTECH tagged on Wire financial roundups, show the provider classifies loosely"]}
      },
      "verdict": "Attempts every company but drowns the long tail in wrong-entity aggregator pages, strips every publisher, and dups 5% of rows; the headline-brand coverage is competent."
    },
    {
      "label": "E",
      "axes": {
        "precision":         {"score": 9, "evidence": ["Alpek: all 4 rows on-topic Q3 earnings (Milenio, Investing.com, Rio Times, El Economista)", "ExxonMobil 11 Reuters-sourced rows all specific (Rovuma LNG, Joliet refinery, Guyana LNG, Papua LNG)", "Only 1 MKT-REPORT flag total (Coles Supermarkets Retail World)", "Little Island Productions returned a BBC trailer story about Onwards and Sideways — appears to be a different production entity (plausible miss)"]},
        "coverage":          {"score": 5, "evidence": ["answered 35/42 companies but with thin volume (188 total articles vs 316-840 for peers); missed BERKSHIRE LABELS, Dine Cartonnages, Fritz Foss, NUBIZ PLASTIC, SEERTECH SOLUTIONS, Sigma Chemtrade, TRICON DRY CHEMICALS entirely", "Spelling pair: Klockner 10 vs Klöckner 8 at only 29% overlap — largely different results flagged by harness", "Thin tails: RAINFOCUS 1 article, Universal McCann 1, ICOF EUROPE 1, Little Island Productions 1, IMPACT RETAIL 1"]},
        "metadata_integrity": {"score": 10, "evidence": ["Header: no-date 0, stale 0, no-publisher 0", "Every row names a reputable publisher (Reuters, Packaging Europe, Investing.com, The Irish Times, Milenio)", "dup 0 (0%) — cleanest of all five"]},
        "story_quality":     {"score": 9, "evidence": ["Summaries are editorially rewritten and informative (Snowflake: 'beat analysts' expectations for its fiscal second-quarter results and raised its fiscal 2027 product-revenue forecast to $6.07 billion from $5.84 billion')", "Dominion summary quotes 'operating earnings of 79 cents per share and revenue of $4.48 billion'", "Mistral Voxtral 3: 'transcription in more than 50 languages and speech synthesis in more than 35'"]},
        "trust":             {"score": 10, "evidence": ["errors: 0", "0 dups, 0 no-date, 0 no-publisher — ground truth clean", "URLs point to real primary sources (reuters.com, bbc.com, bloomberg not present but prnewswire/businesswire absent too — editorial sourcing only)"]}
      },
      "verdict": "Smallest volume but the cleanest and most editorially curated results; the price is weak coverage of obscure entities and inconsistency across spelling variants."
    }
  ]
}
```

## Notes

The run reveals a sharp quality/coverage tradeoff. Providers C and D both answer 42/42 companies but inflate coverage with wrong-entity filler — C's BERKSHIRE LABELS results are entirely Berkshire Hathaway and Bershka clothing, D's Dine Cartonnages results are Applebee's/IHOP earnings. Both also strip every publisher name (100% NO PUBLISHER flagged), forcing the consumer to judge sources by domain. Provider B is broken (201 errors, 7/42 answered). Provider A refuses the long tail cleanly rather than guessing (16 entities returned nothing) and delivers clean metadata when it does answer.

Provider E has the best per-article quality and metadata hygiene — zero dups, zero no-publisher, zero no-date, zero errors, and editorially rewritten summaries from reputable outlets — but its coverage is thin (188 articles total vs 316-840 for peers) and the spelling-variant test exposed a real weakness: Klockner vs Klöckner Pentaplast returned largely different URL sets (29% overlap), meaning the caller's accent choice meaningfully changes results. Provider A's identical 100% overlap on that pair is the only robust answer. No provider handles the obscure B2B tail (Fritz Foss, NUBIZ PLASTIC, ZETA TECHNICAL SERVICES) well — either they return nothing or they return noise.

---

## Recomputed scorecard (harness — authoritative)

Axis scores are the model's; `weighted`, `final`, caps and the ranking
are recomputed by the harness. If numbers in the raw output above
disagree, this table wins.

| Rank | Provider | precision | coverage | metadata_integrity | story_quality | trust | weighted | final | caps |
|---|---|---|---|---|---|---|---|---|---|
| 1 | E | 9 | 5 | 10 | 9 | 10 | 8.5 | 8.5 | — |
| 2 | A | 7 | 7 | 10 | 8 | 9 | 7.9 | 7.9 | — |
| 3 | C | 4 | 8 | 4 | 6 | 5 | 5.25 | 5.25 | metadata_soft |
| 4 | D | 3 | 7 | 4 | 5 | 5 | 4.55 | 4.55 | metadata_soft, precision |
| 5 | B | 6 | 1 | 10 | 8 | 3 | 5.45 | 4.0 | trust |

---

## Spelling-variant consistency (harness — authoritative)

Entities queried under two spellings that differ only by accent, case or
punctuation. Overlap is the share of returned URLs common to both.

**Klockner Pentaplast vs Klöckner Pentaplast**

| Provider | articles for “Klockner Pentaplast” | articles for “Klöckner Pentaplast” | shared URLs | overlap | read |
|---|---|---|---|---|---|
| Syracuse | 3 | 3 | 3/3 | 100% | identical results — spelling-insensitive |
| Linkup | 0 | 2 | 0/2 | 0% | answers only "Klöckner Pentaplast" ⚠ |
| Exa | 20 | 20 | 15/25 | 60% | partially overlapping results |
| Perplexity Search | 20 | 20 | 15/25 | 60% | partially overlapping results |
| Perplexity Agent | 10 | 8 | 4/14 | 29% | largely different results for the two spellings ⚠ |
