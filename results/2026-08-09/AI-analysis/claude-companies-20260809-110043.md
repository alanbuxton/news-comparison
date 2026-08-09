# Companies Analysis — 20260809-110043

*Model: claude-opus-4-7 | Max articles per company per provider: 15*

*Provider labels were anonymised. See `decode-key-20260809-110043.json` to decode.*

---

```json
{
  "query_type": "companies",
  "providers": [
    {
      "label": "A",
      "axes": {
        "precision":         {"score": 8, "evidence": ["Coles: strong on-topic cluster (Greencross, ACCC ruling, Elizabeth St closure)", "Commerzbank AG: 20 articles all directly on UniCredit takeover and buyback", "CVS PHARMACY: 3/7 flagged [MKT-REPORT ⚠] (Attorney General settlements) - state AG announcements slightly off-topic", "FLINT GROUP: article #5 'affordable housing to come to East Lawrence' is Flint Holdings Group (wrong entity)"]},
        "coverage":          {"score": 5, "evidence": ["answered: 28/52 - misses AURIGA POLYMERS, BERKSHIRE LABELS, CHARTER NEX FILMS, Dine Cartonnages, Entertainment Partners, HPCL Mittal Energy, ICOF EUROPE, IMPACT RETAIL, and many others", "Sigma Chemtrade: [NO RESULTS RETURNED ⚠]", "Strong depth for large names (Coles=20, Commerzbank=20, Dominion=20, International Paper=20)"]},
        "recency_integrity": {"score": 10, "evidence": ["header: no-date: 0 (0%), stale: 0 (0%)", "All Borouge and ExxonMobil articles carry precise timestamps within 90 days"]},
        "story_quality":     {"score": 9, "evidence": ["Commerzbank #1: 'CBK Says Teaming Up With UniCredit Could Create Value' - clear substantive Bloomberg summary", "Coles Greencross coverage: informative snippets like 'Coles Ends Talks For Takeover of Petbarn Chain; Shares Gain'", "ExxonMobil #5: 'Exxon made $160 million per day last quarter as oil prices surged' - decision-ready summary"]},
        "trust":             {"score": 10, "evidence": ["header: errors: 0", "URLs resolve to legitimate publishers (Bloomberg, Reuters, AP, Straits Times)", "No hallucinated URL patterns detected"]}
      },
      "verdict": "High-precision provider with pristine date integrity and clean sources, but leaves nearly half the queried entities unanswered."
    },
    {
      "label": "B",
      "axes": {
        "precision":         {"score": 7, "evidence": ["Bloomberg: only 1 article and it's Bloomberg Philanthropies climate cash - wrong entity subset (Michael Bloomberg's charity, not Bloomberg L.P.)", "LUSHA SYSTEMS: 5 clean on-topic Italian GDPR fine articles", "Commerzbank AG: solid Q2/UniCredit coverage", "FLINT GROUP: 0 articles + 4 errors"]},
        "coverage":          {"score": 6, "evidence": ["answered: 31/52 - better than A", "Missed AURIGA POLYMERS, Braroll, CBS News (0 results), CHEP, CHARTER NEX, Dine Cartonnages, Fritz Foss, Jindal Films, KRC, and more", "CBS News returned 0 articles despite being a major entity"]},
        "recency_integrity": {"score": 10, "evidence": ["header: no-date: 0 (0%), stale: 0 (0%)"]},
        "story_quality":     {"score": 8, "evidence": ["Coles: informative summaries like 'Coles shares dropped 4.8% as markets reassessed valuation in light of Australia's new anti-price-gouging laws'", "CVS PHARMACY #4: substantive GLP-1 program description with concrete numbers", "Some summaries generic but generally decision-ready"]},
        "trust":             {"score": 6, "evidence": ["header: errors: 6 (FLINT GROUP 4 errors, Bloomberg 2 errors)", "Errors concentrated on specific entities suggests fetching instability", "No hallucinated URLs detected in returned results"]}
      },
      "verdict": "Clean dates and reasonable precision but hobbled by errors on multiple entities and low article counts per company."
    },
    {
      "label": "C",
      "axes": {
        "precision":         {"score": 6, "evidence": ["BERKSHIRE LABELS: all 9 articles about Berkshire Hathaway (Buffett/Abel) - wrong entity, name-share FP", "AURIGA POLYMERS: articles about Aura Minerals, Auriga Space, Aurrigo International - wrong entities", "CHARTER NEX FILMS: article about Charter Communications - wrong entity", "CHEP: mix of Chemed Corp, Cheniere, CHPE LLC - wrong entities alongside real CHEP items", "Fritz Foss: FUCHS Lubricants, Fosun, FRITZ! router - all wrong entities"]},
        "coverage":          {"score": 9, "evidence": ["answered: 51/52 - highest single-entity match rate", "Only NUBIZ PLASTIC returned no results", "Answered obscure entities like Braroll, Jiangin Yonghe, Little Island Productions"]},
        "recency_integrity": {"score": 9, "evidence": ["header: no-date: 0 (0%), stale: 0 (0%)", "Two dates suspiciously formatted: Linklaters items dated '2656-05-26' and '2175-07-21' (typos in year field)"]},
        "story_quality":     {"score": 9, "evidence": ["Sodexo: rich summaries with specific Meta contract details across 130+ locations", "Commerzbank #1: detailed Q2 net income figures and buyback specifics", "International Paper: substantive Q2 numbers including $6.0B revenue and $587M adj EBITDA"]},
        "trust":             {"score": 8, "evidence": ["header: errors: 0", "Two anomalous year values (2656, 2175) in Linklaters entries suggest date parsing bugs but not URL hallucination", "URLs appear legitimate to real publishers"]}
      },
      "verdict": "Best coverage of the pack but frequently substitutes similarly-named entities when the real one is obscure, dragging precision down."
    },
    {
      "label": "D",
      "axes": {
        "precision":         {"score": 5, "evidence": ["Braroll Acessorios: articles about OMR, Assintecal, Norac, Riffel - none about Braroll", "Bloomberg: mix of Bloomberg Law/Philanthropies and unrelated M&A stories (Pimco/Allianz, Datavant merger, Nielsen/DoubleVerify)", "CHEP: many wrong entities (Chemed, Cheniere, CJ CheilJedang, DXP, Chesapeake Utilities)", "Fritz Foss: Moss unicorn, Cover Genius/Friendsurance, DLC/Filogix - all wrong entities", "Sigma Chemtrade: 50 articles mostly about Sigma Healthcare, Sigma Lithium, Sigma Advanced Systems - wrong entities", "ZHEJIANG KINGSAFE: unrelated Yonghe, Xiaomi, Philips, MAPFRE stories"]},
        "coverage":          {"score": 10, "evidence": ["answered: 52/52 - full coverage", "50 articles per entity uniformly, even for obscure names"]},
        "recency_integrity": {"score": 10, "evidence": ["header: no-date: 0 (0%), stale: 0 (0%)"]},
        "story_quality":     {"score": 8, "evidence": ["Coles #2: detailed Yahoo Finance summary of Accenture India outsourcing deal", "Commerzbank items: dense operational detail on UniCredit buyback and merger talks", "Some snippets show mid-article truncation with '...' patterns but generally informative"]},
        "trust":             {"score": 8, "evidence": ["header: errors: 0", "URLs point to real publishers (Reuters, Bloomberg, WSJ, MarketScreener)", "No hallucinated URLs but heavy volume includes 32 mkt-reports and many wrong-entity matches"]}
      },
      "verdict": "Maximum coverage and volume, but the padding-to-50 approach floods results with wrong-entity and adjacent-topic articles that undermine precision."
    },
    {
      "label": "E",
      "axes": {
        "precision":         {"score": 1, "evidence": ["Bloomberg: results are Facebook/Instagram posts, Play Store app listing, and generic FT pages - all FP-not-news social/directory", "CBS News: only 2 results, both Reuters homepage/commentary unrelated to CBS", "COLES: results include YouTube video, Forbes council personal pages, Facebook posts", "Sigma Chemtrade: 74 articles almost entirely about Sigma Healthcare/Lithium/Advanced Systems - wrong entities", "Multiple entities filled with LinkedIn posts, Instagram reels, Facebook pages counted as FP-not-news"]},
        "coverage":          {"score": 4, "evidence": ["answered: 52/52 nominally but many returns are non-news garbage", "Sigma Chemtrade padded with 74 items about other Sigmas", "ZHEJIANG KINGSAFE: 88 items mostly China macro/unrelated"]},
        "recency_integrity": {"score": 0, "evidence": ["header: no-date: 729 (100%)", "Every single article carries [NO DATE ⚠] flag - cannot verify 90-day window"]},
        "story_quality":     {"score": 2, "evidence": ["Bloomberg summaries are cookie/JS boilerplate: 'Skip to content Bloomberg the Company & Its Products'", "Many summaries are scraped navigation menus and SVG code fragments", "Instagram/Facebook post transcripts as 'summaries' with garbled character codes"]},
        "trust":             {"score": 3, "evidence": ["header: errors: 0 but 32 dup (4%) and 34 mkt-report (5%)", "URLs include google.com/goto redirects, facebook.com/posts, instagram.com/reels - not primary news sources", "No hallucinated URLs but heavy reliance on social media and directory pages"]}
      },
      "verdict": "Catastrophic date integrity (100% missing) plus heavy social-media noise and wrong-entity padding; the results are effectively unusable as a news feed."
    }
  ]
}
```

## Notes

The most striking pattern is how providers handle obscure entities. C and D both push to answer nearly every query, but they do so by returning similarly-named companies (Berkshire Hathaway for BERKSHIRE LABELS, Sigma Healthcare for Sigma Chemtrade, FUCHS Lubricants for Fritz Foss). D's fixed 50-articles-per-entity quota amplifies this problem into hundreds of wrong-entity results. A takes the opposite approach — refusing to answer 24 of 52 entities — which yields much cleaner precision but leaves large coverage gaps. B sits in the middle with 6 errors and modest article counts. Provider E is a category apart: 100% missing dates makes recency unverifiable, and results skew heavily toward Facebook/Instagram/LinkedIn/YouTube pages rather than news articles.

Provider A looks strongest on precision and story quality but its coverage gap is severe — an AI agent querying HPCL Mittal Energy, ExxonMobil suppliers, or half the packaging sector would get nothing. Provider C's date-parsing produced two Linklaters items with years 2656 and 2175 that suggest fragility in the pipeline even though the overall header claims 0 no-date. No provider is genuinely great; the choice depends on whether the consumer prefers silence to noise (A) or noise to silence (C/D).

---

## Recomputed scorecard (harness — authoritative)

Axis scores are the model's; `weighted`, `final`, caps and the ranking
are recomputed by the harness. If numbers in the raw output above
disagree, this table wins.

| Rank | Provider | precision | coverage | recency_integrity | story_quality | trust | weighted | final | caps |
|---|---|---|---|---|---|---|---|---|---|
| 1 | A | 8 | 5 | 10 | 9 | 10 | 8.15 | 8.15 | — |
| 2 | C | 6 | 9 | 9 | 9 | 8 | 7.8 | 7.8 | — |
| 3 | D | 5 | 10 | 10 | 8 | 8 | 7.65 | 7.65 | — |
| 4 | B | 7 | 6 | 10 | 8 | 6 | 7.25 | 7.25 | — |
| 5 | E | 1 | 4 | 0 | 2 | 3 | 1.9 | 1.9 | recency_hard, trust, precision |
