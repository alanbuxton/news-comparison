# Companies Analysis — 20260706-073017

*Model: claude-opus-4-7 | Max articles per company per provider: 15*

*Provider labels were anonymised. See `decode-key-20260706-073017.json` to decode.*

---

```json
{
  "query_type": "companies",
  "providers": [
    {
      "label": "A",
      "axes": {
        "precision":         {"score": 8, "evidence": ["Borouge: 20 clean articles on Woosh recycling partnership, AD Ports Fujairah pact, Q1 2026 results — all on-topic", "Commerzbank AG: 20 highly relevant UniCredit takeover articles from Bloomberg, Reuters, Business Times", "COLES: 20 on-target results (ACCC Kalgoorlie block, price gouging laws, Ever.Ag partnership)", "5 mkt-report flags out of 305 (2%) — very low FP-not-news rate"]},
        "coverage":          {"score": 5, "evidence": ["answered: 27/52 — half the queried entities returned zero (ALPEK POLYESTER, AURIGA POLYMERS, BERKSHIRE LABELS, Braroll, CHARTER NEX FILMS, GREEN BAY PACKAGING, HPCL Mittal Energy, Sigma Chemtrade all empty)", "CHEP returned only 1 article (Splitero board addition); Entertainment Partners only 1 (UEG Ventures)", "Duplicate coverage for Klockner Pentaplast and Klöckner Pentaplast (same 10 articles both)"]},
        "recency_integrity": {"score": 10, "evidence": ["header: no-date: 0 (0%), stale: 0 (0%) — all 305 articles carry dates within window", "Borouge results all timestamped April–June 2026", "Commerzbank UniCredit coverage precisely dated June 2026"]},
        "story_quality":     {"score": 8, "evidence": ["Constellium article: 'Constellium Sells Automotive Structures Joint Venture in Changchun, China' — clear summary of Vision 2028 divestiture", "CBS News 'Scott Pelley Ousted From 60 Minutes' Adweek piece includes context on Nick Bilton dismissal", "International Paper Mississippi groundbreaking summary conveys $225M investment scope", "Some Constellium MarketBeat entries feel thin (analyst upgrade blurbs)"]},
        "trust":             {"score": 10, "evidence": ["header: errors: 0, dup: 0 (0%)", "URLs from established outlets: Bloomberg, Reuters (via Zawya), AP, Variety, GlobeNewswire — no hallucinated patterns", "Consistent PR Newswire / Cision URL structures verifiable"]}
      },
      "verdict": "Strong precision, dates and trust; content is genuinely relevant when it appears, but half the entity list returns nothing, hurting coverage."
    },
    {
      "label": "B",
      "axes": {
        "precision":         {"score": 7, "evidence": ["ExxonMobil: 9 articles all on-topic (Texas redomicile, Woodside acquisition talks, Q1 2026 results)", "Linklaters: 11 relevant deal-advisory items (OMIFCO IPO, Philippines bond, Wallbox restructuring)", "Sigma Chemtrade query: returned Chemtrade Logistics and Sigma Lithium — mixed entity match (FP-entity risk)", "Dine Cartonnages query returned 5 Dine Brands Global articles — wrong entity (FP-entity)"]},
        "coverage":          {"score": 6, "evidence": ["answered: 35/52 — better than A but still 17 entities empty (AURIGA, BERKSHIRE LABELS, CBS News, Deloitte, Entertainment Partners, Fritz Foss, etc.)", "CBS News returned 0 articles despite 1 error", "Green Bay Packaging: 0 articles, 2 errors"]},
        "recency_integrity": {"score": 10, "evidence": ["header: no-date: 0 (0%), stale: 0 (0%)", "Haier IFA 2026 article dated 2026-09-04 — future-dated but within scope; Husky HyCAP dated 2026-07-14 slightly future", "Overall dates cleanly presented"]},
        "story_quality":     {"score": 8, "evidence": ["Dominion Energy NextEra merger summary conveys $67B deal, 10M customers, AI data center context", "Commerzbank UniCredit takeover article gives 12.51% uptake figure and board rejection stance", "MISTRAL AI €3B raise summary includes valuation and infrastructure focus"]},
        "trust":             {"score": 4, "evidence": ["header: errors: 62 — extremely high error rate distributed across many entities (Deloitte 6 errors, LUSHA SYSTEMS 3, MISTRAL AI 3, ZHEJIANG KINGSAFE 2)", "Errors indicate systemic retrieval failures; ~34% of company queries hit at least one error", "No obvious hallucinated URLs but reliability concerns"]}
      },
      "verdict": "Decent story quality and dates, but 62 errors and entity confusion (Dine Brands returned for Dine Cartonnages) undermine trust and precision."
    },
    {
      "label": "C",
      "axes": {
        "precision":         {"score": 6, "evidence": ["Bloomberg: 10 articles that appear to be industry macro (Pfizer supply chain, Tesla-CATL batteries, EU due-diligence rules) with only tangential Bloomberg mentions — mostly FP-entity/broader-than-asked", "Charter NEX Films: 2 items pointing to Instagram profile and generic corporate overview — FP-not-news (social media, About Us)", "CHEP: single article on Brambles class action is on-topic", "Lusha Systems: 6 results — most are Lusha newsroom/docs/privacy pages (FP-not-news), one Demand Gen case study OK", "Regus: single Facebook post about La Vista office (FP-not-news social media)"]},
        "coverage":          {"score": 6, "evidence": ["answered: 31/52 — 21 entities empty", "Constellium: 4 articles (Yahoo Finance, Seeking Alpha, MarketBeat) — mostly stock aggregator pages, borderline", "SEERTECH SOLUTIONS: 2 LinkedIn posts referencing company (weak)"]},
        "recency_integrity": {"score": 10, "evidence": ["header: no-date: 0 (0%), stale: 0 (0%)", "Bloomberg articles dated 2026-06-10 through 2026-06-30", "Dominion Q1 press release properly dated 2026-05-07"]},
        "story_quality":     {"score": 7, "evidence": ["Sodexo Q3 FY2026 summary clearly conveys +2.0% organic growth and guidance revision", "International Paper dividend declaration article gives exact $0.4625 amount and dates", "Some entries thin — MarketBeat 'stock price and news' summaries lack specifics"]},
        "trust":             {"score": 8, "evidence": ["header: errors: 0, dup: 0", "URLs mostly from real outlets (Reuters, CNBC, Bloomberg, GlobeNewswire, Business Wire)", "Some social/directory URLs (Instagram, LinkedIn, Facebook) reduce trust slightly"]}
      },
      "verdict": "Clean dates and no errors, but frequent About Us / social media / macro industry articles inflate FP rate; low article volume overall."
    },
    {
      "label": "D",
      "axes": {
        "precision":         {"score": 1, "evidence": ["Alpek Polyester: 78 articles all NO DATE, mostly industry-wide polyester/petrochemical stories with no Alpek specifics", "Bloomberg query returned 83 items that are IRS Fast Track, AFL-CIO lawsuits, Supreme Court news — Bloomberg only as publisher name-drop", "Coles query returned Reuters/TradingView macro (China Vale profit, Volkswagen Brazil) that don't mention Coles substantively", "Dine Cartonnages returned Nestle, Berkeley homebuilder, Micron chip news — wrong entity entirely", "32 mkt-report flags in header"]},
        "coverage":          {"score": 8, "evidence": ["answered: 52/52 — every entity got results (only provider to do so)", "But 'coverage' is illusory since content is largely off-topic"]},
        "recency_integrity": {"score": 0, "evidence": ["header: no-date: 4406 (100%) — every single article lacks a date", "Cannot verify any article falls within 90-day window", "Rubric explicitly treats no-date as off-scope"]},
        "story_quality":     {"score": 3, "evidence": ["Summaries are largely scraped navigation/related-article boilerplate ('Image 25 Reuters Refinitiv...', 'More news from Reuters')", "Coles Sky News entries include Portuguese/Spanish sidebar text ('Empresário de 52 anos revela como aprendeu inglês')", "CBS News summaries: 'watch now watch now VIDEO...' cookie-navigation dump"]},
        "trust":             {"score": 2, "evidence": ["header: errors: 0 nominally, but content quality suggests scraper failures", "URLs point to real domains but content extraction is broken — summaries are page furniture, not article body", "59 dup flags", "Reader cannot decide relevance from these blobs"]}
      },
      "verdict": "Full entity coverage is a mirage; 100% no-date, boilerplate summaries, and rampant off-topic entity matches make output nearly unusable."
    },
    {
      "label": "E",
      "axes": {
        "precision":         {"score": 6, "evidence": ["Coles: 15 highly relevant articles (Christmas in July, ACCC Kalgoorlie block, Greencross talks) — all on-topic", "Dominion Energy: strong on-topic set (transmission line ruling, NextEra merger, heat wave tips)", "Commerzbank: solid UniCredit tender saga coverage", "But Braroll query returned Sky News Australia clickbait, Ventisol fans, Marvo gaming (FP-entity)", "Fritz Foss query returned Fhenix crypto, National Beverage FIZZ, Horizon Farms (FP-entity)", "L M Goes Embalagens returned Brazilian detergent factory, Anvisa fiscalização (FP-entity mostly)", "50 mkt-report flags"]},
        "coverage":          {"score": 9, "evidence": ["answered: 52/52 — every entity returned articles", "Even obscure entities (KRC Custom Manufacturing, ZHEJIANG KINGSAFE, TRICON DRY CHEMICALS) got results, though relevance varies"]},
        "recency_integrity": {"score": 10, "evidence": ["header: no-date: 0 (0%), stale: 0 (0%)", "Articles precisely timestamped e.g. Coles 2026-07-02 23:15:00+00:00", "CVS Caremark Zepbound coverage dated 2026-07-05"]},
        "story_quality":     {"score": 7, "evidence": ["CVS Restores Eli Lilly's Zepbound article gives clear GLP-1 formulary shift context", "Coles Kalgoorlie ACCC block summary conveys ruling detail and share impact", "Snowflake SoftBank SB Neo article provides FY27 launch timeline", "Some entries are aggregator/PR blurbs but generally decision-informative"]},
        "trust":             {"score": 7, "evidence": ["header: errors: 33 — non-trivial but manageable", "URLs from mix of tier-1 (Bloomberg, Reuters, WSJ) and lower-tier aggregators (aktiensensor.com, mondialnews.com, briefglance.com)", "Some URLs look suspicious (banehopper.com 'GE Vernova Accelerates India Expansion' with quality-score metadata) — possible AI-generated content farm", "14 duplicates"]}
      },
      "verdict": "Broadest coverage with clean dates and volume, but relies on aggregator/content-farm URLs and shows entity-confusion on obscure names, hurting precision and trust."
    }
  ]
}
```

## Notes

The starkest split is between date-integrity discipline and coverage breadth. Provider D achieved 52/52 answered but paid for it with 100% no-date articles and heavily boilerplate summaries — the harness will cap it hard. Provider E also hit 52/52 but with clean dates, though it leaned on lower-tier aggregators and content-farm-looking domains (banehopper.com, aktiensensor.com) that create latent trust concerns not caught by simple date/error counts. Providers A and C traded coverage for cleaner precision — A especially returned 20-article deep dives on marquee entities (Borouge, Commerzbank, Coles) but left 25 entities empty. Provider B's 62-error count is the run's biggest reliability red flag.

Among the providers scoring well on precision/dates, A's honest weakness is that its uniform 20-article cap for well-covered entities looks like a hard limit rather than editorial judgment, and its zero-return rate on obvious entities (CBS News for provider B returned 0 also, but A got 20 there) suggests inconsistent source coverage across industries. E's honest weakness is source quality: mixing Bloomberg/WSJ with what look like SEO content mills means an AI agent could easily be misled by plausibly-worded but low-provenance summaries.

---

## Recomputed scorecard (harness — authoritative)

Axis scores are the model's; `weighted`, `final`, caps and the ranking
are recomputed by the harness. If numbers in the raw output above
disagree, this table wins.

| Rank | Provider | precision | coverage | recency_integrity | story_quality | trust | weighted | final | caps |
|---|---|---|---|---|---|---|---|---|---|
| 1 | A | 8 | 5 | 10 | 8 | 10 | 8.0 | 8.0 | — |
| 2 | E | 6 | 9 | 10 | 7 | 7 | 7.5 | 7.5 | — |
| 3 | C | 6 | 6 | 10 | 7 | 8 | 7.05 | 7.05 | — |
| 4 | B | 7 | 6 | 10 | 8 | 4 | 6.95 | 4.0 | trust |
| 5 | D | 1 | 8 | 0 | 3 | 2 | 2.7 | 2.7 | recency_hard, trust, precision |
