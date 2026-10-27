# Companies Analysis — 20261027-000250

*Model: claude-opus-4-7 | Max articles per company per provider: 20*

*Provider labels were anonymised. See `decode-key-20261027-000250.json` to decode.*

---

```json
{
  "query_type": "companies",
  "providers": [
    {
      "label": "A",
      "axes": {
        "precision": {"score": 3, "evidence": [
          "Berkshire Labels: 19 of 20 results flagged [WRONG ENTITY: Berkshire Hathaway/Residential/Bending Spoons] — essentially 0% on-target",
          "CHARTER NEX FILMS: nearly all 20 are [WRONG ENTITY: Charter Communications, Nex Playground, Henkel, etc.]",
          "Dine Cartonnages: 20/20 are generic food-industry index pages or Dine Brands, no on-target coverage",
          "SEERTECH SOLUTIONS: 20/20 wrong-entity (Schwab, Rentokil, QXO, Pistachio, Bolt.new) — zero on-target"
        ]},
        "coverage": {"score": 10, "evidence": [
          "answered: 42/42 companies with 20 articles each — perfect coverage on paper",
          "Even obscure Fritz Foss and NUBIZ PLASTIC answered (though content wrong-entity)"
        ]},
        "metadata_integrity": {"score": 2, "evidence": [
          "no-publisher: 840 (100%) — publisher never named; only domain visible",
          "dup: 43 (5%) across the run including Alpek #3 duplicated as #5, Borouge #13 as #14",
          "not-news: 12 (1%) including LinkedIn posts for Alpek and Zeta"
        ]},
        "story_quality": {"score": 6, "evidence": [
          "Alpek Q3 2026 summaries give concrete figures ($276M EBITDA, +101% YoY, $990M guidance)",
          "Borouge item #4 quotes '$1.4 billion revenue, $401 million adjusted EBITDA'",
          "Many wrong-entity rows still have readable summaries, but Bloomberg entry #16 is a cookie-wall-style page listing"
        ]},
        "trust": {"score": 4, "evidence": [
          "0 errors reported in header",
          "But rampant mislabelling: Berkshire Hathaway stories returned under 'Berkshire Labels' query, Charter Communications under 'Charter Nex Films' — provider treated name-match as entity-match",
          "Spelling-variant pair Klockner vs Klöckner only 60% overlap — same entity returns substantially different URL sets"
        ]}
      },
      "verdict": "Enormous volume with excellent nominal coverage, but a brittle name-matching layer makes small-company precision collapse to near-zero and 100% no-publisher metadata degrades every row."
    },
    {
      "label": "B",
      "axes": {
        "precision": {"score": 9, "evidence": [
          "Coles 10 results: all genuine Coles Group news (supplier awards, antitheft tags, FY26 results, Fair Work provision)",
          "Dominion Energy 8 results: all on-target (SCC staff recommendation, IRP filing, NextEra merger, Q2 earnings)",
          "ExxonMobil 11 results: all genuine Exxon news (Guyana LNG, refining margin boost, Joliet refinery, Rovuma LNG contracts)",
          "Only minor stumbles: Little Island Productions [WRONG ENTITY: BBC drama Onwards and Sideways] and 2 wrong-entity rows under NECTAR 360"
        ]},
        "coverage": {"score": 6, "evidence": [
          "answered: 35/42 — missed Berkshire Labels, Dine Cartonnages, Fritz Foss, NUBIZ PLASTIC, Sigma Chemtrade, Tricon Dry Chemicals, Seertech Solutions",
          "Small/obscure companies systematically absent",
          "ICOF Europe returns only 1 article, Impact Retail only 1, Rainfocus only 1, Universal McCann only 1"
        ]},
        "metadata_integrity": {"score": 10, "evidence": [
          "no-date: 0 (0%), stale: 0 (0%), no-publisher: 0 (0%), dup: 0 (0%)",
          "Every row has explicit publisher like 'Reuters', 'Packaging Europe', 'ScanX'",
          "Only 1 mkt-report flag in 188 rows"
        ]},
        "story_quality": {"score": 9, "evidence": [
          "ExxonMobil #2: 'stronger refining margins could lift third-quarter downstream earnings by about $4.5 billion'",
          "Dominion Energy #7: '$340 million, or 37 cents per share, and adjusted earnings of 79 cents per share. Revenue was $4.48 billion'",
          "Summaries consistently provide decision-ready specifics without boilerplate"
        ]},
        "trust": {"score": 9, "evidence": [
          "0 errors, no suspicious URLs — all canonical publisher domains",
          "Spelling-variant Klockner vs Klöckner: only 29% overlap — 'largely different results' flag, a notable consistency weakness",
          "Rare wrong-entity label (Little Island Productions returned Onwards and Sideways)"
        ]}
      },
      "verdict": "The cleanest, most trustworthy results in the run — publisher named every time and precision excellent — but it quietly skips seven companies and returns thin counts for small firms."
    },
    {
      "label": "C",
      "axes": {
        "precision": {"score": 6, "evidence": [
          "Bloomberg 5/5 on-target (Crypto Exposure Analytics, Canoe acquisition, Enterprise MCP)",
          "Dine Cartonnages #2 is [LABELLED NOT-NEWS] trade-exhibition profile, #1 only [NAME-DROP]",
          "Flint Group: 2 of 3 are [WRONG ENTITY: Flint Group US HVAC platform]",
          "Westrock: 3 of 7 are [WRONG ENTITY: Westrock Coffee Company]"
        ]},
        "coverage": {"score": 6, "evidence": [
          "answered: 36/42 — missed Fritz Foss, Gandhar Oil Refinery, Green Bay Packaging, International Paper, NUBIZ Plastic, Sigma Chemtrade",
          "Thin counts: HPCL Mittal 5 articles all no-date, ICOF Europe 1 article, Seertech Solutions 1 article"
        ]},
        "metadata_integrity": {"score": 3, "evidence": [
          "no-date: 91 (59%) — severe; HPCL Mittal Energy all 5 results undated, Haier all 7 undated, Linklaters 9 of 10 undated",
          "Consumer cannot tell if HMEL #1 ('HMEL to invest Rs 2,600 cr in Punjab') is current or years old",
          "no-publisher 0%, dup 0% — small mercy"
        ]},
        "story_quality": {"score": 8, "evidence": [
          "Deloitte #4: 'global FY2026 revenue of US$74.5 billion, up 3.8% in local currency and 5.7% in US dollars'",
          "Constellium #2: 'Q2 revenue of $2.7 billion and record Segment Adjusted EBITDA, while net income reached $148 million'",
          "Summaries written in cautious, hedged prose ('the supplied report does not give a precise date') — informative and honest"
        ]},
        "trust": {"score": 6, "evidence": [
          "0 errors, no hallucinated URLs",
          "But Haier 7/7 undated, Linklaters 9/10 undated, HPCL 5/5 undated — pattern suggests date extraction is broken, not that sources lack dates",
          "Spelling-variant Klockner vs Klöckner: 0% URL overlap — same entity returns completely different articles"
        ]}
      },
      "verdict": "Thoughtful, well-summarised results with named publishers, but a crippling 59% no-date rate and 0% overlap between accent-variant queries undermines the whole feed."
    },
    {
      "label": "D",
      "axes": {
        "precision": {"score": 7, "evidence": [
          "Bloomberg 20 results all on-target (Crypto Basel analytics, Dublin expansion, Canoe acquisition, FXGO)",
          "ExxonMobil 20 results all on-target (Shell/Exxon chemicals JV, Guyana licence, refining margin boost)",
          "Westrock: 7 of 20 are [WRONG ENTITY: Westrock Coffee Company] — significant pollution",
          "Little Island Productions: 20/20 wrong-entity (Banijay/Little Princess, Rock Island/Fresh Films, Great Island Productions)"
        ]},
        "coverage": {"score": 5, "evidence": [
          "answered: 26/42 — worst coverage of the five providers",
          "Missed: ALPEK POLYESTER, Berkshire Labels, Charter Nex Films, CHEP, Dine Cartonnages, Fritz Foss, HPCL Mittal, ICOF Europe, Impact Retail, Little Island, NUBIZ Plastic, Seertech, Sigma Chemtrade, Tricon Dry Chemicals, Universal McCann, Zeta Technical Services"
        ]},
        "metadata_integrity": {"score": 10, "evidence": [
          "no-date: 0 (0%), stale: 0 (0%), no-publisher: 0 (0%)",
          "Publisher named on every row; dup only 5 (2%)",
          "Timestamps include time-of-day precision (2026-10-22 13:58:30+00:00)"
        ]},
        "story_quality": {"score": 7, "evidence": [
          "Rich entity-role tags like '[ExxonMobil Holdings Corp.: vendor]' and '[Haier Smart Home Co. Ltd.: organization]' are useful",
          "But many summaries are truncated with ellipses like '...' and 'ExxonMobil Yet to Seek Guyana Licence Extension' — abrupt",
          "Deloitte summaries are substantive: 'global FY2026 revenue of US$74.5 billion'"
        ]},
        "trust": {"score": 7, "evidence": [
          "0 errors, dates look authentic with timezone precision",
          "Spelling-variant Klockner vs Klöckner: 100% overlap — the only provider that is truly spelling-insensitive",
          "Tag misfires: Little Island Productions tagged on completely unrelated Banijay/Little Princess story shows weak entity disambiguation"
        ]}
      },
      "verdict": "Metadata and spelling-insensitivity are best-in-class, but answering only 26/42 companies with substantial wrong-entity leakage on smaller firms limits usefulness."
    },
    {
      "label": "E",
      "axes": {
        "precision": {"score": 3, "evidence": [
          "Berkshire Labels: 19/20 wrong-entity (Berkshire Residential, Bershka, Berkshire Hathaway, Berkshire Grey)",
          "Fritz Foss: 20/20 wrong-entity (FRITZ! router brand, Foss & Company tax equity, Fossil Group, Fritz Hansen)",
          "Little Island Productions: 20/20 wrong-entity (Banijay Little Princess, Rock Island, Doreen Wilcox Little)",
          "LUSHA SYSTEMS: strong on-target set (Garante €2M fine coverage), showing precision is possible when name is unambiguous"
        ]},
        "coverage": {"score": 10, "evidence": [
          "answered: 42/42 companies with 20 articles each — perfect raw coverage",
          "Even NUBIZ Plastic answered (though 20/20 wrong-entity trade-fair content)"
        ]},
        "metadata_integrity": {"score": 2, "evidence": [
          "no-publisher: 840 (100%) — domain shown but publisher name never extracted, same severe issue as Provider A",
          "dup: 14 (2%) including Alpek #1 duplicated as #4 in Berkshire Labels, Nubiz Plastic #13 as #14 as #15",
          "not-news: 2 (0%) — minimal boilerplate"
        ]},
        "story_quality": {"score": 7, "evidence": [
          "Alpek #1: 'Q3 2026 comparable EBITDA doubled from a year earlier to $276 million' with analyst context",
          "Deloitte #4: 'The AI-powered, human-led solution combines agentic capabilities with Deloitte...'",
          "Many rows have truncated headlines like 'EOS and Constellium Strengthen Partnership on Additive Manufacturing Portfolio - toolingtales'"
        ]},
        "trust": {"score": 4, "evidence": [
          "0 errors, URLs look canonical",
          "But company-name string matching is the only entity gate — Zeta Technical Services returned 20 Zeta Global ad-tech stories, Sigma Chemtrade returned 20 Sigma Healthcare/Chemtrade Logistics stories",
          "Spelling-variant Klockner vs Klöckner only 60% overlap — same entity gets substantially different article sets"
        ]}
      },
      "verdict": "High-volume firehose with the best raw coverage, but the entity disambiguation is naive — small-company queries become namesake-roundups and 100% no-publisher strips every row of a credibility cue."
    }
  ]
}
```

## Notes

The run exposes a stark split: Providers A and E chase maximum recall and return 20 rows for every single company, but for small, ambiguous or obscure names (Berkshire Labels, Fritz Foss, NUBIZ Plastic, Little Island Productions, Zeta Technical Services, Sigma Chemtrade) they degenerate into wrong-entity namesake dumps where literally every row is flagged. Providers B, C and D silently skip 6–16 of the 42 companies — a different failure mode that at least avoids misleading the caller. Only Provider D achieves true spelling-insensitivity on the Klockner/Klöckner pair (100% URL overlap); the others return substantially different article sets for the same real entity, with Provider C hitting an alarming 0% overlap.

Provider B looks strongest on precision, metadata and story quality, but its honest weaknesses are real: it answered only 35/42 companies and gave single-article thin coverage to several (ICOF Europe, Impact Retail, Rainfocus, Universal McCann). It also mislabelled Little Island Productions, so its entity disambiguation is good but not perfect. Provider D's metadata is immaculate and it is the only spelling-robust provider, but its 26/42 answer rate is the worst in the run and Westrock, Little Island and several other queries drowned in wrong-entity Westrock Coffee / Banijay content. Provider C's 59% no-date rate is the single most damaging metadata finding across the run — HMEL, Haier, Linklaters and others are nearly all undated, which hard-caps its usefulness regardless of how well-written its summaries are.

---

## Recomputed scorecard (harness — authoritative)

Axis scores are the model's; `weighted`, `final`, caps and the ranking
are recomputed by the harness. If numbers in the raw output above
disagree, this table wins.

| Rank | Provider | precision | coverage | metadata_integrity | story_quality | trust | weighted | final | caps |
|---|---|---|---|---|---|---|---|---|---|
| 1 | B | 9.0 | 7.4 | 10 | 9 | 9 | 8.83 | 8.83 | — |
| 2 | D | 8.5 | 6.0 | 10 | 7 | 7 | 7.78 | 7.78 | — |
| 3 | C | 3.6 | 2.9 | 3 | 8 | 6 | 4.39 | 4.39 | metadata_hard |
| 4 | E | 5.0 | 4.0 | 2 | 7 | 4 | 4.5 | 4.0 | metadata_hard, trust |
| 5 | A | 4.1 | 4.5 | 2 | 6 | 4 | 4.13 | 4.0 | metadata_hard, trust |

---

## Row labels and controls (harness — authoritative)

Every shown row was labelled in a separate per-company pass; precision
and coverage are counted from those labels and replace the judge's
scores (shown in brackets). A row is clean if on-target and not flagged
as duplicate, stale, undated, market report or not-news. *Padded*
companies were answered only with false positives; padded companies and
answered control companies each cancel 1 answered company in coverage.

| Provider | precision | coverage | clean rows | wrong-entity | name-drop | not-news | flagged | answered | padded | controls hit | unlabelled |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Exa | 5.0 (3) | 4.0 (10) | 448/900 | 353 | 25 | 7 | 7 | 31/42 | 11 | 3 | 0 |
| Linkup | 3.6 (6) | 2.9 (6) | 56/154 | 13 | 3 | 2 | 80 | 24/42 | 12 | 0 | 0 |
| Perplexity Agent | 9.0 (9) | 7.4 (6) | 170/188 | 13 | 4 | 0 | 1 | 33/42 | 2 | 0 | 0 |
| Perplexity Search | 4.1 (3) | 4.5 (10) | 373/900 | 322 | 14 | 109 | 22 | 32/42 | 10 | 3 | 0 |
| Syracuse | 8.5 (7) | 6.0 (5) | 271/318 | 14 | 23 | 1 | 7 | 26/42 | 0 | 1 | 0 |

**Exa**

- BERKSHIRE LABELS: 20 rows, none clean — Baker Labels; Berkshire Financial Services; Berkshire Grey (robotics); Berkshire Hathaway
- Dine Cartonnages: 20 rows, none clean — Alma Pack / Le Carton Morocco deal; Cartonnage de Vaucanson; Cartonnages d'Auch; Dine Brands
- Fritz Foss: 20 rows, none clean — EU Cyber Resilience Act article; FERMAC & MOSS industrial decoration alliance; FOSS Group Indonesia (fire suppression); FRITZ! (AVM router brand)
- ICOF EUROPE: 20 rows, none clean — COFICAB (Tunisian cable group); ICOF Dominican Republic (Instituto de Capacitación Ocoa Futuro); ICOP (Italian engineering firm); ICOP/Trevi (Italian engineering)
- IMPACT RETAIL: 20 rows, none clean — Alta Group / Fortenova (Serbian retail); Empire / Sobeys / Safeway; Empire Company / Sobeys; FPG / Constantia Emporium
- Little Island Productions: 20 rows, none clean — Banijay / Little Princess; Banijay Kids & Family / Little Princess; Chinese short drama platforms in Korea; Chorokbaem Media / Reelshort
- NUBIZ PLASTIC: 20 rows, none clean — Bumi Baru Plastik (Indonesia recycling); CB Expo cannabis fair in Dortmund; Mutares/SABIC thermoplastics acquisition; NUBIZ trade fair in Dortmund
- SEERTECH SOLUTIONS: 20 rows, none clean — SEER TECH (06106.HK) Hong Kong firm; Seer, Inc. (Nasdaq: SEER) proteomics; Seer, Inc. (proteomics) buyout; Seer, Inc. (proteomics) earnings
- Sigma Chemtrade: 20 rows, none clean — Chemtrade Logistics; Chemtrade Logistics Income Fund; Sigma Healthcare; Sigma Healthcare/Chemist Warehouse
- TRICON DRY CHEMICALS: 20 rows, none clean — ALSOK / Nippon Dry-Chemical (Japan); Hovione (pharma); Intercon Chemical (St. Louis); Monument Chemical / Minasolve
- ZETA TECHNICAL SERVICES: 20 rows, none clean — FST Technical Services / Z2; Zeta (Indian banking-tech); Zeta Global (ad-tech)
- CONTROL Mariel Labels (made-up): 20 rows — LabelVie breaks 10bn dirhams in half-year sales - 7news Morocco; Pavilion and GovSpend Are Partnering to Bring Suppliers Earlier, Warme; EXCLUSIVE: How firms linked to sanctioned Chinese cotton giant sell cl
- CONTROL Ostumbra Corrugated (made-up): 20 rows — Ostrea : après une année de rodage industriel, le spécialiste des coqu; Cirkla, Belmark and Ossid launch resealable fibre trays for food — Pac; Orora expects lower Group EBIT as Saverglass pressures persist
- CONTROL Veliel Packaging (made-up): 20 rows — Weil Advises OTPP and Trivium Packaging in $3.4B Acquisition by Silgan; Silgan, private equity acquiring Trivium to create $7.3B packaging gia; Sidley Represents Strategic Partnership Between Silgan and AIP in US$7

**Linkup**

- BERKSHIRE LABELS: 2 rows, none clean — Asteria Group / GT Etiketten (Dutch, different group)
- Borouge: 5 rows, none clean
- Dine Cartonnages: 2 rows, none clean
- Entertainment Partners: 2 rows, none clean
- HAIER: 7 rows, none clean
- HPCL Mittal Energy: 5 rows, none clean
- ICOF EUROPE: 1 rows, none clean
- IMPACT RETAIL: 2 rows, none clean — IMPACT Commerce (Danish e-commerce); Impact International (Netherlands retail marketing)
- Little Island Productions: 2 rows, none clean
- SEERTECH SOLUTIONS: 1 rows, none clean
- TRICON DRY CHEMICALS: 3 rows, none clean
- ZETA TECHNICAL SERVICES: 6 rows, none clean — ZETA Group (pharma engineering); Zeta Global (ad-tech)

**Perplexity Agent**

- Little Island Productions: 1 rows, none clean — BBC drama Onwards and Sideways
- ZETA TECHNICAL SERVICES: 6 rows, none clean — Zeta Global (ad-tech)

**Perplexity Search**

- BERKSHIRE LABELS: 20 rows, none clean — Berkshire Hathaway; Berkshire Hathaway / Bending Spoons; Berkshire Hathaway / Brooks Running; Berkshire Residential Investments
- Dine Cartonnages: 20 rows, none clean — C-Store finance news roundup; C-Store finance roundup; CPG Latest stories index; CPG business news roundup
- Fritz Foss: 20 rows, none clean — Baker Hughes / Chart Industries; Boehringer Ingelheim / Evax; China tech newsflash (Nvidia etc.); DRESSi dressing brand launch
- ICOF EUROPE: 20 rows, none clean — Aeon / Aware Health; Black Kite (cyber risk); Cleversoft / FS Assist; Copla (GRC platform)
- IMPACT RETAIL: 20 rows, none clean — Acne Studios; Beauty industry roundup; Carrefour / Codifrance; Couche-Tard
- Little Island Productions: 20 rows, none clean — All3 robotics; Ardagh Metal Packaging; Bell Canada ahlo 2; Discovery/WBD antitrust
- NUBIZ PLASTIC: 20 rows, none clean — Arburg acquiring Stork IMM; Coca-Cola Europacific Partners plant upgrade; InterTabac 2026 trade fair; InterTabac press event
- SEERTECH SOLUTIONS: 20 rows, none clean — Arclin / Nomex manufacturing; Bolt.new / Dokai acquisition; Cribl / CardinalOps; Factor supply chain platform
- Sigma Chemtrade: 20 rows, none clean — Chemtrade Logistics Income Fund; NAFDAC Nigeria medicines; Sigma Healthcare; Sigma Healthcare (Australian pharmacy)
- ZETA TECHNICAL SERVICES: 20 rows, none clean — Zeta Global (ad-tech)
- CONTROL Mariel Labels (made-up): 20 rows — Category: Magazine Production and Print; The Packaging Week; Le fabriquant d'étiquettes Sopano passe à l'offensive avec trois acqui
- CONTROL Ostumbra Corrugated (made-up): 20 rows — Regulatory & Legal; The Packaging Week; Capital & Financial Markets - Packaging News Daily
- CONTROL Veliel Packaging (made-up): 20 rows — The Packaging Week; Operations & Footprint - Packaging News Daily; Latest Non-Food Packaging Industry News Insights & Updates - Part 28

**Syracuse**

- CONTROL Mariel Labels (made-up): 2 rows — LEADERSHIP EXPERTS WHO STUDIED AI AT OXFORD AND MIT: HUMANITY FIRST, L; From the Front Lines of Catastrophes to the Future of Technology: EFFE

---

## How sure is the ranking? (harness)

The queried companies were resampled 2000 times and
precision, coverage, final score and rank recounted each time. Ranges are
95%. This covers only which companies were queried — the judge's axes and
the row labels are held fixed — so the real uncertainty is wider.
Providers ahead of the next in under 90% of
resamples are not clearly separated from it.

| Rank | Provider | final | precision | coverage | held rank | ahead of next |
|---|---|---|---|---|---|---|
| 1 | Perplexity Agent | 8.83 (8.2–9.3) | 8.1–9.7 | 5.7–8.8 | 100% | 100% |
| 2 | Syracuse | 7.78 (7.4–8.1) | 8.1–8.9 | 4.5–7.4 | 100% | 100% |
| 3 | Linkup | 4.39 (3.6–5.0) | 2.6–4.8 | 0.0–5.5 | 85% | 85% (not separated) |
| 4 | Exa | 4.0 (3.6–4.0) | 3.8–6.1 | 1.2–6.4 | 85% | 99% |
| 5 | Perplexity Search | 4.0 (3.4–4.0) | 3.1–5.2 | 2.1–6.9 | 89% | — |

---

## Spelling-variant consistency (harness — authoritative)

Entities queried under two spellings that differ only by accent, case or
punctuation. Overlap is the share of returned URLs common to both.

**Klockner Pentaplast vs Klöckner Pentaplast**

| Provider | articles for “Klockner Pentaplast” | articles for “Klöckner Pentaplast” | shared URLs | overlap | read |
|---|---|---|---|---|---|
| Perplexity Search | 20 | 20 | 15/25 | 60% | partially overlapping results |
| Perplexity Agent | 10 | 8 | 4/14 | 29% | largely different results for the two spellings ⚠ |
| Linkup | 5 | 3 | 0/8 | 0% | largely different results for the two spellings ⚠ |
| Syracuse | 3 | 3 | 3/3 | 100% | identical results — spelling-insensitive |
| Exa | 20 | 20 | 15/25 | 60% | partially overlapping results |
