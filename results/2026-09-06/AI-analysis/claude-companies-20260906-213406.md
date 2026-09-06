# Companies Analysis — 20260906-213406

*Model: claude-opus-4-7 | Max articles per company per provider: 15*

*Provider labels were anonymised. See `decode-key-20260906-213406.json` to decode.*

---

```json
{
  "query_type": "companies",
  "providers": [
    {
      "label": "A",
      "axes": {
        "precision":         {"score": 8, "evidence": ["Alpek results are on-topic (Rio Times Argentina plant closure, Plastics News lawsuit)", "Coles coverage is substantive (7NEWS Palantir contract, Reuters annual profit)", "Bloomberg query returned some off-topic name-drops like Simple Flying 'Airbus Resumes A330neo' where Bloomberg is merely cited as source", "Only 3 mkt-report (2%) and 2 dup (1%) — minimal noise"]},
        "coverage":          {"score": 4, "evidence": ["answered: 25/42 — 17 entities returned no results including BERKSHIRE LABELS, CHARTER NEX FILMS, HPCL Mittal Energy, Jindal Films, Sigma Chemtrade, Universal McCann, ICOF EUROPE, IMPACT RETAIL", "Both Klockner spellings answered with same single article (100% overlap)"]},
        "metadata_integrity": {"score": 10, "evidence": ["no-date: 0 (0%), stale: 0 (0%), no-publisher: 0 (0%) per header", "Publishers named cleanly e.g. 'Rio Times Online', 'Bloomberg', 'Reuters'"]},
        "story_quality":     {"score": 8, "evidence": ["Summaries informative: Borouge 'declares $656mln interim dividend for 2026' with specifics", "ExxonMobil Q2 summary quotes '$14.5 billion' profit and per-share detail", "Some summaries brief (e.g. Constellium Q2 headline-only)"]},
        "trust":             {"score": 9, "evidence": ["errors: 0, no suspicious URLs", "URLs resolve to established outlets (reuters.com, bloomberg.com, prnewswire.com)"]}
      },
      "verdict": "Clean metadata and disciplined precision, but nearly 40% of queried entities return nothing — a serious coverage gap."
    },
    {
      "label": "B",
      "axes": {
        "precision":         {"score": 3, "evidence": ["BERKSHIRE LABELS query returned entirely wrong entity — Berkshire Hathaway insurance/PE coverage instead of the UK label maker", "CHARTER NEX FILMS returned Charter Communications/Cox and unrelated 'nexTC' items", "Fritz Foss returned FOSS analytical instruments, Foss & Company tax equity, and Federal Signal — no queried entity match", "NECTAR 360 SERVICES returned Nektar Therapeutics and unrelated 'Nectar One'; ZETA TECHNICAL SERVICES returned Zeta Global marketing"]},
        "coverage":          {"score": 9, "evidence": ["answered: 42/42 — every entity got 20 articles", "Klockner spelling variants: 20 vs 20 but only 38% URL overlap ⚠"]},
        "metadata_integrity": {"score": 5, "evidence": ["no-publisher: 840 (100%) — every row shows domain only e.g. '| NO PUBLISHER ⚠ (theglobeandmail.com)'", "no-date: 0, stale: 0 — dates intact"]},
        "story_quality":     {"score": 6, "evidence": ["Some summaries substantive (Alpek Q2 '$407 million EBITDA')", "Many rows show boilerplate/nav text: 'Bij Yahoo gebruiken we Cookies...' on ExxonMobil Q2, 'Dacă doriți să personalizați' on Dominion", "LinkedIn post fragments used as summaries"]},
        "trust":             {"score": 7, "evidence": ["errors: 0", "URLs generally valid but many aggregator/syndicated sources (finanznachrichten.de, tradingview.com syndications)"]}
      },
      "verdict": "Perfect coverage headline is undermined by wrong-entity results for less-famous names and heavy publisher-name loss."
    },
    {
      "label": "C",
      "axes": {
        "precision":         {"score": 9, "evidence": ["Coles: 14/14 on-topic (ABC News profit, AFR Accenture deal, Guardian facial recognition)", "Linklaters: 11 articles all on-topic (Law.com Abu Dhabi hire, Reuters US gains)", "Dine Cartonnages returned exactly one legal notice about the actual French company", "0 mkt-report, only 2 dup"]},
        "coverage":          {"score": 6, "evidence": ["answered: 33/42 — misses BERKSHIRE LABELS, CHARTER NEX FILMS, Fritz Foss, ICOF EUROPE, IMPACT RETAIL, NUBIZ PLASTIC, SEERTECH SOLUTIONS, Sigma Chemtrade, ZETA TECHNICAL SERVICES", "Klockner spelling variants: only 18% overlap between the two ⚠"]},
        "metadata_integrity": {"score": 10, "evidence": ["no-date: 0, stale: 0, no-publisher: 0", "Publishers cleanly named e.g. 'Reuters', 'CNBC', 'Packaging Dive'"]},
        "story_quality":     {"score": 9, "evidence": ["Rich narrative summaries: Dominion 'reported adjusted second-quarter earnings of $0.79 per share, above the $0.68 analyst consensus'", "Snowflake summary details '$300 million' Saudi investment with regional specifics"]},
        "trust":             {"score": 10, "evidence": ["errors: 0, no suspicious URLs", "Sources are mainstream outlets (Reuters, CNBC, ABC News, WealthBriefing)"]}
      },
      "verdict": "Highest-quality summaries and cleanest metadata, but declines to answer ~20% of queried entities."
    },
    {
      "label": "D",
      "axes": {
        "precision":         {"score": 4, "evidence": ["BERKSHIRE LABELS returned Berkshire Hathaway insurance/investment content — wrong entity", "FLINT GROUP returned FLINT Corp (Canadian energy services) not the printing ink company, and 'FLIN' product launch item", "Deloitte returned only one PR item and its duplicate — thin", "Klockner spelling coverage: answers only 'Klockner Pentaplast' not 'Klöckner Pentaplast' (0% overlap)"]},
        "coverage":          {"score": 2, "evidence": ["answered: 15/42 — 27 entities returned no results (Alpek, CBS News, Constellium, Deloitte partial, Little Island Productions, Linklaters, Mistral, Snowflake, Westrock, etc all zero)", "errors: 18 including 10 errors on SNOWFLAKE query alone"]},
        "metadata_integrity": {"score": 9, "evidence": ["no-date: 0, stale: 0, no-publisher: 0 per header", "One suspicious future date on ExxonMobil (2026-10-31) but publishers named"]},
        "story_quality":     {"score": 7, "evidence": ["Summaries include specifics: Borouge 'net profit dips; eyes better H2 plant utilisation'", "Some analytical summaries with pros/cons framing (HPCL)"]},
        "trust":             {"score": 3, "evidence": ["errors: 18 (33% of answered set) — 10 errors on SNOWFLAKE alone, 4 on Deloitte, 2 on NECTAR 360, 2 on Bloomberg", "One future-dated article on ExxonMobil (2026-10-31)"]}
      },
      "verdict": "Half the queries returned nothing and error rate is extreme, especially for major names like Snowflake."
    },
    {
      "label": "E",
      "axes": {
        "precision":         {"score": 4, "evidence": ["Fritz Foss returned Foss & Company tax equity, FOSS acquisition of Wasatch Photonics, Federal Signal, Sygnum bank — none the queried entity", "NUBIZ PLASTIC returned Nubz dog treats, NUBURU laser company, nübo baby brand — no target match", "SEERTECH SOLUTIONS returned SEER Robotics, Serstech, SEERS (Korean pharma), SeeTrue — wrong entities", "Charter Nex Films query returned Charter Communications Cox deal, Boliden/Nexa Resources, NexPoint Materials — off-target"]},
        "coverage":          {"score": 9, "evidence": ["answered: 42/42 with 20 articles each", "Klockner spelling variants both answered but only 29% URL overlap ⚠"]},
        "metadata_integrity": {"score": 5, "evidence": ["no-publisher: 840 (100%) — publisher shown only as domain e.g. '(bloomberg.com)', '(reuters.com)'", "no-date: 0, stale: 0", "46 dup (5%) — highest dup rate of all providers"]},
        "story_quality":     {"score": 5, "evidence": ["Many summaries include ellipsis truncation and stray navigation: 'Regus opens HQ office, coworking space near downtown Allen | Allen | Community Impact ...'", "Some summaries carry raw parsing artifacts (ticker ellipsis '... :ALPKF)')", "Substantive content still present (Snowflake Q2 revenue $1.55bn, EPS 62c)"]},
        "trust":             {"score": 6, "evidence": ["errors: 0", "Heavy syndication and low-authority aggregators: 'lifestyle.thepointnews.com', 'lifestyle.massnews.com', 'lifestyle.lincolnlabs.com' repeated across RainFocus results", "5% dup rate suggests weak de-duplication"]}
      },
      "verdict": "Full coverage and no errors, but many results are wrong-entity, aggregator-syndicated, and publisher names are lost across the board."
    }
  ]
}
```

## Notes

The run exposes a sharp split between providers that answer everything (B, E) and providers that decline unfamiliar names (A, C, D). B and E both hit 42/42 but pay for it heavily in precision: obscure queries like BERKSHIRE LABELS, CHARTER NEX FILMS, Fritz Foss, NUBIZ PLASTIC, SEERTECH SOLUTIONS, ZETA TECHNICAL SERVICES consistently return wrong-entity content (Berkshire Hathaway, Charter Communications, Foss & Company, Zeta Global). Both also strip publisher names universally, keeping only domains. Provider D is particularly weak — half the queries return nothing and it produced 18 errors including 10 on Snowflake alone.

Provider C stands out on precision, story quality, and metadata integrity, but declines about 20% of queries. Provider A is similarly clean but with an even larger coverage gap (25/42). On the spelling-variant test, only A returns identical results for Klockner/Klöckner Pentaplast; B, C, and E show 18–38% overlap indicating accent-sensitive retrieval, and D answers only the ASCII spelling. No provider is uniformly strong: the choice is between clean-but-incomplete (A/C) and comprehensive-but-noisy (B/E).

---

## Recomputed scorecard (harness — authoritative)

Axis scores are the model's; `weighted`, `final`, caps and the ranking
are recomputed by the harness. If numbers in the raw output above
disagree, this table wins.

| Rank | Provider | precision | coverage | metadata_integrity | story_quality | trust | weighted | final | caps |
|---|---|---|---|---|---|---|---|---|---|
| 1 | C | 9 | 6 | 10 | 9 | 10 | 8.7 | 8.7 | — |
| 2 | A | 8 | 4 | 10 | 8 | 9 | 7.65 | 7.65 | — |
| 3 | E | 4 | 9 | 5 | 5 | 6 | 5.6 | 5.6 | metadata_soft |
| 4 | B | 3 | 9 | 5 | 6 | 7 | 5.55 | 5.0 | metadata_soft, precision |
| 5 | D | 4 | 2 | 9 | 7 | 3 | 4.65 | 4.0 | trust |

---

## Spelling-variant consistency (harness — authoritative)

Entities queried under two spellings that differ only by accent, case or
punctuation. Overlap is the share of returned URLs common to both.

**Klockner Pentaplast vs Klöckner Pentaplast**

| Provider | articles for “Klockner Pentaplast” | articles for “Klöckner Pentaplast” | shared URLs | overlap | read |
|---|---|---|---|---|---|
| Syracuse | 1 | 1 | 1/1 | 100% | identical results — spelling-insensitive |
| Perplexity Search | 20 | 20 | 11/29 | 38% | largely different results for the two spellings ⚠ |
| Perplexity Agent | 4 | 9 | 2/11 | 18% | largely different results for the two spellings ⚠ |
| Linkup | 1 | 0 | 0/1 | 0% | answers only "Klockner Pentaplast" ⚠ |
| Exa | 20 | 20 | 9/31 | 29% | largely different results for the two spellings ⚠ |
