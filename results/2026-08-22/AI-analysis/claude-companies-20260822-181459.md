# Companies Analysis — 20260822-181459

*Model: claude-opus-4-7 | Max articles per company per provider: 15*

*Provider labels were anonymised. See `decode-key-20260822-181459.json` to decode.*

---

```json
{
  "query_type": "companies",
  "providers": [
    {
      "label": "A",
      "axes": {
        "precision":         {"score": 7, "evidence": ["CBS News: 20 on-topic articles about CBS News/60 Minutes staffing, Bari Weiss, Scott Pelley firing", "Dominion Energy: strong M&A coverage of NextEra merger, Spanberger intervention", "ExxonMobil: 19 relevant articles on Q2 earnings, Guyana, Rovuma LNG", "Some noise: Bloomberg 'Ariel Levy to join 60 Minutes' filed under CBS News is fine, but ExxonMobil Petrobras profit article is peripheral name-drop"]},
        "coverage":          {"score": 4, "evidence": ["answered: 24/42 companies — 18 entities returned NO RESULTS including BERKSHIRE LABELS, CHARTER NEX FILMS, Dine Cartonnages, HPCL Mittal Energy, ICOF EUROPE, Jindal Films, Klockner Pentaplast (unaccented), LUSHA SYSTEMS, Sigma Chemtrade, TRICON DRY CHEMICALS, Universal McCann, ZETA TECHNICAL SERVICES", "Spelling-variant failure: answered 'Klöckner Pentaplast' with 3 articles but 0 for 'Klockner Pentaplast'"]},
        "metadata_integrity": {"score": 9, "evidence": ["no-date: 0 (0%), stale: 0 (0%), no-publisher: 0 (0%)", "Named publishers throughout: 'Rio Times Online', 'Plastics News', 'Bloomberg', 'Reuters'"]},
        "story_quality":     {"score": 8, "evidence": ["Coles: substantive summaries e.g. 'Coles Ends Talks For Takeover of Petbarn Chain; Shares Gain' with context", "Constellium Q2 earnings summary explains record profitability and cash flow", "Some short/truncated summaries e.g. Borouge Q2 'Borouge reports 23% rise in Q2 net profit as Ruwais operations recover.' is just the headline repeated"]},
        "trust":             {"score": 9, "evidence": ["errors: 0", "URLs from reputable domains: reuters.com, bloomberg.com, cnn.com, spglobal.com", "1 mkt-report flag on Constellium (alcircle.com), 3 total mkt-report across run"]}
      },
      "verdict": "Clean, well-formatted results with strong metadata and no errors, but leaves 18 of 42 queried entities completely unanswered including obscure but real companies."
    },
    {
      "label": "B",
      "axes": {
        "precision":         {"score": 9, "evidence": ["Alpek Polyester: 3 tightly on-topic articles about Argentina plant closure, Q2 EBITDA guidance, war-related opportunity", "Linklaters: 11 relevant articles on Webber Wentzel alliance end, US expansion, FY26 results", "Lusha Systems: 6 focused articles on Italian €2m GDPR fine", "Mistral AI: 8 articles all specifically about the French AI company, no wrong-entity noise"]},
        "coverage":          {"score": 8, "evidence": ["answered: 35/42 companies — highest of any provider except C/D/F", "Only 7 no-results: BERKSHIRE LABELS, Fritz Foss, ICOF EUROPE, IMPACT RETAIL, NUBIZ PLASTIC, SEERTECH SOLUTIONS, ZETA TECHNICAL SERVICES", "Answered obscure entities: Dine Cartonnages (1 article legal notice), HPCL Mittal Energy (1 ICRA rating article), Sigma Chemtrade (1 CARE Ratings), TRICON DRY CHEMICALS (2 articles including Colombian Supreme Court case)"]},
        "metadata_integrity": {"score": 10, "evidence": ["no-date: 0 (0%), stale: 0 (0%), no-publisher: 0 (0%)", "Consistent publisher naming: 'Reuters', 'Bloomberg', 'MLex', 'The Wall Street Journal', 'Financial Times'"]},
        "story_quality":     {"score": 9, "evidence": ["CBS News Paramount coverage includes substantive M&A context: 'Paramount Skydance said all options, including a possible sale of CNN, were being considered'", "Coles: 'ACCC probes Aldi, Coles after Four Corners tomato-sourcing claims' with detailed context on Chinese tomato allegations", "Sigma Chemtrade: single article gives credit downgrade rationale ('CARE Ratings downgraded... to CARE B+')"]},
        "trust":             {"score": 10, "evidence": ["errors: 0", "Consistently reputable sources: Reuters, Bloomberg, WSJ, MLex, ICIS", "0 mkt-report flags"]}
      },
      "verdict": "Best-balanced provider: broad coverage combined with clean metadata, informative summaries, and no obvious noise."
    },
    {
      "label": "C",
      "axes": {
        "precision":         {"score": 4, "evidence": ["Bloomberg query: returns generic Bloomberg news wire content like 'Nvidia Will Back First Phase of OpenAI Ohio Project' and 'Alibaba to Sell Gaming Arm' rather than news ABOUT Bloomberg", "IMPACT RETAIL: returns wrong-entity 'Ayala launches ACX Retail', 'Angel & Rocket Plans Major Expansion in India', 'Impact.com's $340M Secondary Raise' — none about a company called Impact Retail", "Fritz Foss: 20 articles on Danfoss, F&F Korean brand, Foss & Company tax equity — wrong entities", "TRICON DRY CHEMICALS: mostly generic chemical M&A (Tronox, Tinicum, GracoRoberts) not the queried entity"]},
        "coverage":          {"score": 9, "evidence": ["answered: 42/42 companies — always returns 20 articles per company", "But 'answers' for Fritz Foss, IMPACT RETAIL, SEERTECH SOLUTIONS, ZETA TECHNICAL SERVICES are mostly wrong-entity padding"]},
        "metadata_integrity": {"score": 3, "evidence": ["no-publisher: 840 (100%) — every single row has NO PUBLISHER ⚠", "Domains still visible (e.g. finance.yahoo.com, bloomberg.com, prnewswire.com) so information is degraded rather than absent", "0 no-date, 0 stale is a positive"]},
        "story_quality":     {"score": 6, "evidence": ["Alpek Polyester Q2 earnings summary provides detail: 'Operating Free Cash Flow: $127 million'", "Some summaries are raw scraped fragments: Bloomberg entry has 'Alibaba Group Holding Ltd. is selling its gaming arm in a deal worth at least $1.5 billion' followed by menu artifacts", "LinkedIn posts appear as sources for Alpek ('Rildo Magalhães | linkedin.com') — social media FP-not-news"]},
        "trust":             {"score": 6, "evidence": ["errors: 0", "dup: 24 (3%) higher than peers", "mkt-report: 8 flags", "LinkedIn and social sources for company research reduce trust: Alpek entry #4 is a LinkedIn profile page"]}
      },
      "verdict": "Answers every company but pads obscure queries with wrong-entity results, strips publisher names entirely, and includes LinkedIn/social sources."
    },
    {
      "label": "D",
      "axes": {
        "precision":         {"score": 3, "evidence": ["BERKSHIRE LABELS: 20 articles almost entirely about Berkshire Hathaway (Buffett, Alphabet stake), not label manufacturer — wrong-entity failure", "CBS News: articles about CSPi Q3, Cirrus Logic, Paramount-Warner, Castle Biosciences, Essilorluxottica — many unrelated to CBS News specifically", "Fritz Foss: 20 articles on Danfoss, DEUTZ acquiring FFG, JFB/XTEND, FinanceFeeds — all wrong entities", "CHEP: articles on StoneX AMG, Osapiens/Nasdaq, Xylem/Cornell Pump, Chevron/Hess — mostly unrelated M&A", "NUBIZ PLASTIC returns Nuo Therapeutics, Nu Holdings, Nocopi — name-similarity errors", "SEERTECH SOLUTIONS returns Ambiq, Serve Robotics, Semtech — wrong entities"]},
        "coverage":          {"score": 9, "evidence": ["answered: 42/42 — full coverage", "But many answers are wrong-entity padding; genuine coverage for e.g. HPCL Mittal Energy is 20 HPCL-related articles (correct); Dine Cartonnages answered with UNFI, News Corp, Hilton Food — none about the queried entity"]},
        "metadata_integrity": {"score": 3, "evidence": ["no-publisher: 840 (100%) — same total-strip as C", "0 no-date, 0 stale", "Domains present in parens so recoverable"]},
        "story_quality":     {"score": 7, "evidence": ["Dominion Energy summary quotes specific figures: 'Q2 2026 operating earnings of $0.79 a share, ahead of Wall Street's $0.75 estimate'", "Constellium: 'record segment adjusted EBITDA of $439 million' with context", "Some summaries are broken markdown fragments: Berkshire Hathaway 'Stay Informed Download the App...' includes navigation cruft"]},
        "trust":             {"score": 6, "evidence": ["errors: 0", "Wrong-entity results systematically returned for obscure companies reduce trust: querying 'BERKSHIRE LABELS' should not return Warren Buffett news", "dup: 3 (0%) low"]}
      },
      "verdict": "Nominal 100% answer rate hides systematic wrong-entity padding for obscure queries, plus universal stripping of publisher names."
    },
    {
      "label": "E",
      "axes": {
        "precision":         {"score": 7, "evidence": ["Where it answers, results are tightly on-topic: Borouge 8 articles all about the UAE petrochemicals company, RainFocus 9 articles all about the event platform", "Linklaters 10 articles all about the law firm's transactions and expansions", "Gandhar Oil 6 articles all about Q1 profit surge and refinery operations", "Bloomberg returns only 2 articles due to *** ERROR *** — but they are relevant"]},
        "coverage":          {"score": 2, "evidence": ["answered: 17/42 companies — worst coverage of any provider except by design", "25 no-results including major public companies: ALPEK POLYESTER, BERKSHIRE LABELS, CBS News, CHARTER NEX FILMS, CHEP, Dine Cartonnages, Entertainment Partners, ExxonMobil, GREEN BAY PACKAGING, HAIER, ICOF EUROPE, IMPACT RETAIL, Jindal Films, Klockner Pentaplast, Klöckner Pentaplast, LUSHA SYSTEMS, Little Island Productions, NUBIZ PLASTIC, REGUS BUSINESS CENTERS, SEERTECH SOLUTIONS, Sigma Chemtrade, TRICON DRY CHEMICALS, Universal McCann, ZETA TECHNICAL SERVICES"]},
        "metadata_integrity": {"score": 10, "evidence": ["no-date: 0, stale: 0, no-publisher: 0", "Publishers named clearly: 'Rio Times Online', 'AGBI', 'Reuters', 'Bloomberg'"]},
        "story_quality":     {"score": 8, "evidence": ["RainFocus Sales Module summary: 'The module integrates with CRMs like Salesforce, providing sales leadership with visibility...' - substantive", "Constellium Q2 summary quotes revenue and buyback specifics", "Coles Greencross article summarizes both the abandonment and the ACCC opposition context"]},
        "trust":             {"score": 5, "evidence": ["errors: 2 (Bloomberg entity failure)", "Where it answers, sources are reputable (Reuters, Bloomberg, ad-hoc-news.de, Investing.com)", "Error rate 2/42 = ~5% is material for a company query"]}
      },
      "verdict": "High-quality but low-yield: when it answers, results are relevant and well-formatted, but it fails to answer well over half of the queried companies."
    },
    {
      "label": "F",
      "axes": {
        "precision":         {"score": 1, "evidence": ["Self-reported relevance: 74% of results scored below 0.2 by the provider itself — 12 items answered with 154 articles it scored entirely below 0.2", "Fritz Foss best-score 0.044: returns TradingView reprints and unrelated finance news", "Klöckner Pentaplast best-score 0.093 — returns Bayer/Perfuse Therapeutics, Iran war coverage, Smurfit Westrock France investment — none about kp", "ALPEK POLYESTER best-score 0.145 — returns P2 Science, Reuters Iran war coverage, Fedrigoni Self-Adhesives", "Dine Cartonnages: 9 articles including Facebook posts about mummy sacrifice, National Girlfriends Day, and Etsy risk assessment templates — utter noise", "Bloomberg query returns Wikipedia article and Facebook posts"]},
        "coverage":          {"score": 4, "evidence": ["answered: 42/42 nominally but 12 items are pure noise per self-reported scoring", "Genuine coverage for e.g. Coles is only 6 articles; NECTAR 360 SERVICES gets 1 result with NO DATE"]},
        "metadata_integrity": {"score": 2, "evidence": ["no-publisher: 476 (100%) — every row missing publisher", "no-date: 74 (16%) — severe, most severe metadata failure of any provider — buyer cannot tell if article is recent", "Numerous NO DATE ⚠ flags across Bloomberg, CBS News, Dine Cartonnages, Little Island Productions, MISTRAL AI SAS"]},
        "story_quality":     {"score": 3, "evidence": ["Many summaries are raw scraped navigation cruft: multiple entries contain fragments like 'Home page Seeking Alpha - Power to Investors Search for Symbols'", "Dine Cartonnages entries include SVG path data and Facebook UI HTML in summary text", "Some summaries are single line marketing snippets from Instagram/Facebook posts"]},
        "trust":             {"score": 2, "evidence": ["errors: 0 (nominal) but 74% of results self-scored below 0.2 relevance — provider knows results are poor", "Sources include Facebook.com, Instagram.com, Etsy.com, Eventbrite.com, xn----ymcba6ad7a3a9iez.net (junk domain) for company research", "12 items answered with 154 articles all scored below 0.2 — precision failure the article list itself does not reveal"]}
      },
      "verdict": "Answers every query but the results are largely noise — the provider's own relevance scores show it knew 74% of its output was weak, metadata is degraded by 16% no-date rate, and sources include social media and junk domains."
    }
  ]
}
```

## Notes

The most striking pattern is the coverage/precision tradeoff. Provider B is the only one to combine broad coverage (35/42) with clean, on-topic results and clear publisher attribution — it declines to answer 7 obscure queries rather than fabricate results, and its answers for tiny entities like Dine Cartonnages (a single legal notice) or Sigma Chemtrade (a single CARE Ratings note) are exactly what an AI agent needs. Providers C, D, and F all claim 42/42 coverage but achieve it by returning wrong-entity padding: BERKSHIRE LABELS becomes Berkshire Hathaway news, Fritz Foss becomes Danfoss/DEUTZ news, NUBIZ PLASTIC becomes Nuo Therapeutics/Nu Holdings news. F additionally admits — through its own relevance scores — that 74% of what it returned it considered weak, and 12 entire queries were answered exclusively with sub-0.2 scored results.

Provider B's honest weaknesses: it misses 7 entities entirely (including Fritz Foss and IMPACT RETAIL, which no provider handled well), and its dup count is 1 which is functionally zero but suggests no duplicate-collapsing beyond that. Provider A is close behind on quality but answers only 24/42 — its refusal to attempt "Klockner Pentaplast" while returning results for "Klöckner Pentaplast" is a coverage failure the caller cannot anticipate. Provider E is the harshest tradeoff: excellent per-result quality but 17/42 coverage and 2 outright errors including the Bloomberg query.

---

## Recomputed scorecard (harness — authoritative)

Axis scores are the model's; `weighted`, `final`, caps and the ranking
are recomputed by the harness. If numbers in the raw output above
disagree, this table wins.

| Rank | Provider | precision | coverage | metadata_integrity | story_quality | trust | weighted | final | caps |
|---|---|---|---|---|---|---|---|---|---|
| 1 | B | 9 | 8 | 10 | 9 | 10 | 9.1 | 9.1 | — |
| 2 | A | 7 | 4 | 9 | 8 | 9 | 7.15 | 7.15 | — |
| 3 | E | 7 | 2 | 10 | 8 | 5 | 6.3 | 6.3 | — |
| 4 | C | 4 | 9 | 3 | 6 | 6 | 5.45 | 5.0 | metadata_hard |
| 5 | D | 3 | 9 | 3 | 7 | 6 | 5.25 | 5.0 | metadata_hard, precision |
| 6 | F | 1 | 4 | 2 | 3 | 2 | 2.2 | 2.2 | metadata_hard, trust, precision |

---

## Spelling-variant consistency (harness — authoritative)

Entities queried under two spellings that differ only by accent, case or
punctuation. Overlap is the share of returned URLs common to both.

**Klockner Pentaplast vs Klöckner Pentaplast**

| Provider | articles for “Klockner Pentaplast” | articles for “Klöckner Pentaplast” | shared URLs | overlap | read |
|---|---|---|---|---|---|
| Syracuse | 0 | 3 | 0/3 | 0% | answers only "Klöckner Pentaplast" ⚠ |
| Perplexity Agent | 6 | 3 | 3/6 | 50% | partially overlapping results |
| Exa | 20 | 20 | 11/29 | 38% | largely different results for the two spellings ⚠ |
| Perplexity Search | 20 | 20 | 16/24 | 67% | partially overlapping results |
| Linkup | 0 | 0 | 0/0 | — | no results for either spelling |
| Tavily | 2 | 20 | 0/22 | 0% | largely different results for the two spellings ⚠ |

---

## Provider self-reported relevance (harness — authoritative)

What each provider said about its own results. Never used to filter them. "Weak items" are queries the provider answered while scoring every article it returned below 0.2.

| Provider | scored | median | weak items | read |
|---|---|---|---|---|
| Syracuse | 0/205 | — | 0 | returns no relevance score — caller cannot triage its results |
| Perplexity Agent | 0/216 | — | 0 | returns no relevance score — caller cannot triage its results |
| Exa | 0/840 | — | 0 | returns no relevance score — caller cannot triage its results |
| Perplexity Search | 0/840 | — | 0 | returns no relevance score — caller cannot triage its results |
| Linkup | 0/63 | — | 0 | returns no relevance score — caller cannot triage its results |
| Tavily | 476/476 | 0.056 | 12 | 74% of its results scored below 0.2; 12 items answered with 154 articles it scored entirely below 0.2 ⚠ |
