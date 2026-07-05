# Companies Analysis — 20260705-124554

*Model: claude-opus-4-7 | Max articles per company per provider: 15*

*Provider labels were anonymised. See `decode-key-20260705-124554.json` to decode.*

---

```json
{
  "query_type": "companies",
  "providers": [
    {
      "label": "A",
      "axes": {
        "precision":         {"score": 1, "evidence": ["Alpek Polyester query returned Evonik polyester business news, PepsiCo, FAA Blue Origin, and Reuters cookie-banner scrapes rather than Alpek-specific news", "Berkshire Labels (a UK label converter) query returned Berkshire Hathaway/Buffett/Abel investing news exclusively — wrong-entity FP-entity", "Sigma Chemtrade query returned Sigma Lithium (Brazil), Sigma Healthcare (Australia/Boots), Sigma Advanced Systems — all wrong-entity", "Gandhar Oil Refinery includes stock-quote pages (Reuters GADH.M3, Investing.com, Bloomberg profile) which are FP-not-news"]},
        "coverage":          {"score": 8, "evidence": ["All ~40 queried entities returned results (78-100 articles per company header)", "Even obscure entities like 'Braroll Acessorios Industriais' and 'Jiangin Yonghe Packaging Products' got 82-88 articles"]},
        "recency_integrity": {"score": 0, "evidence": ["Header states no-date: 4406 out of 4406 total articles — 100% no-date across every company including ALPEK POLYESTER (78 no-date), Bloomberg (83 no-date), CVS PHARMACY (91 no-date)"]},
        "story_quality":     {"score": 2, "evidence": ["Bloomberg query summaries are almost entirely nav boilerplate: '### Products Bloomberg Terminal Data Trading Risk Compliance Indices'", "CBS News summaries show raw scraped video listings ('watch now watch now VIDEO02:53')", "Many TradingView entries are just image-list boilerplate: 'Image 16 Image 17 Image 18 Image 19 Reuters Refinitiv'"]},
        "trust":             {"score": 5, "evidence": ["Header errors: 0 — no fetch errors", "But URLs like tradingview.com/news/reuters.com,2026:newsml_L6N42O0WJ appear scraped rather than original, and summaries are frequently boilerplate suggesting scraper is grabbing chrome, not content"]}
      },
      "weighted": 2.20,
      "caps_applied": ["recency_hard", "precision"],
      "final": 2.20,
      "verdict": "Massive scale with zero date integrity and rampant wrong-entity contamination; the no-date flag on 100% of 4406 articles alone disqualifies this from serious use."
    },
    {
      "label": "B",
      "axes": {
        "precision":         {"score": 8, "evidence": ["Dominion Energy returns clean on-topic hits: 'NextEra Energy and Dominion Energy to Combine' and 'Dominion Energy Announces First-Quarter 2026 Results'", "ExxonMobil returned only one item — an SEC 8-K supplement — which is on-topic though thin", "Bloomberg returns clearly synthetic-looking generic supply-chain roundups (Pfizer, Tesla, Microsoft, Apple, Unilever) that read as plausibly hallucinated Bloomberg headlines with suspiciously uniform URL patterns bloomberg.com/news/articles/2026-06-XX/..."]},
        "coverage":          {"score": 3, "evidence": ["Only 69 total articles across ~30 companies; multiple companies (ALPEK POLYESTER, AURIGA POLYMERS, Braroll, CBS News, Gandhar and many others) returned zero results per provider header", "CHEP got 1 article, ExxonMobil got 1 article, Linklaters got 1 article"]},
        "recency_integrity": {"score": 10, "evidence": ["Header states no-date: 0 and stale: 0 across all 69 articles; every entry carries a clean date within window"]},
        "story_quality":     {"score": 9, "evidence": ["Dominion Energy summary explains NextEra $67B all-stock deal specifics with EPS growth guidance", "Berkshire Labels — despite being wrong-entity — gives crisp actionable summaries of Abel's investment moves", "Trane summary quantifies Q1 EPS ($2.66) and full-year guidance uplift"]},
        "trust":             {"score": 5, "evidence": ["Header errors: 0", "But Bloomberg cluster of 10 articles with uniform bloomberg.com/news/articles/2026-06-XX/... URLs and generic topics (EU due-diligence, Apple chip packaging, Unilever deforestation) looks like FP-halluc — no way to verify these exist", "Berkshire Labels query returned Berkshire Hathaway news which is wrong-entity — a trust concern about entity disambiguation"]}
      },
      "weighted": 6.35,
      "caps_applied": [],
      "final": 6.35,
      "verdict": "Highest per-article quality of any provider with perfect date integrity, but coverage is thin and the uniformly-shaped Bloomberg cluster smells of hallucination."
    },
    {
      "label": "C",
      "axes": {
        "precision":         {"score": 6, "evidence": ["Coles returns strong on-topic items: 'ACCC blocks Coles supermarket' and 'Coles in talks to acquire TPG's Greencross for $4 billion'", "CVS Pharmacy returns clean company-specific news: 'Florida Attorney General launches investigation into CVS Health' and Q1 2026 earnings press release", "Sigma Chemtrade query returned Chemtrade Logistics and Sigma Lithium articles — wrong-entity mix", "Klöckner Pentaplast and Klockner Pentaplast both returned zero articles (all errors) — the query-error case that produces no false positives but also no data"]},
        "coverage":          {"score": 4, "evidence": ["62 errors out of 122 attempted articles per header (errors: 62) — over half the queries errored", "CBS News: 0 articles, 1 error", "Deloitte: 0 articles, 6 errors", "Entertainment Partners: 0 articles, 5 errors", "GREEN BAY PACKAGING: 0 articles, 2 errors; LUSHA SYSTEMS: 0 articles, 3 errors"]},
        "recency_integrity": {"score": 10, "evidence": ["Header states no-date: 0, stale: 0 — every article that was returned has a valid recent date"]},
        "story_quality":     {"score": 9, "evidence": ["Dominion Energy summary quantifies '$67 billion all-stock deal' and '10 million customers'", "Linklaters entries name specific deals: 'OMIFCO $2.7bn IPO' and 'Genel Energy $360M Capricorn acquisition'", "CVS summary specifies '$2.9B in Q1 profit' and '$100.4 billion in first quarter total revenues'"]},
        "trust":             {"score": 4, "evidence": ["Header errors: 62 — an extremely high error rate indicating unreliable retrieval", "Deloitte errored on all 6 attempts producing no output for a major queried company"]}
      },
      "weighted": 6.05,
      "caps_applied": ["trust"],
      "final": 4.00,
      "verdict": "When it returns something, the articles are crisp and well-summarized, but a 62-error header count and multiple companies with zero results cap it under the trust rule."
    },
    {
      "label": "D",
      "axes": {
        "precision":         {"score": 7, "evidence": ["Commerzbank returns 20 clean, on-topic UniCredit-takeover-battle articles with headlines like 'Germany Rejects UniCredit's €39 Billion Takeover Bid for Commerzbank'", "Coles returns focused stories: 'Coles refunds $2,000 worth of faulty Apple gift cards' and 'Australia Court Says Coles Misled Shoppers'", "Dominion Energy: strong signal — 'NextEra to buy Dominion in $66.8 billion US power deal'", "Entertainment Partners returned only 1 article about UEG (United Entertainment Group) — wrong-entity FP", "CHEP returned 1 article about the 'Coalition for Home Equity Partnership' — wrong-entity FP"]},
        "coverage":          {"score": 7, "evidence": ["305 total articles across ~30 companies with most entities getting 3-20 hits (Bloomberg 3, Borouge 20, CBS News 20, Commerzbank 20, Coles 20, Dominion 20)", "Some entities like CHEP got just 1 article and Entertainment Partners got 1 article — undercoverage on niche entities"]},
        "recency_integrity": {"score": 10, "evidence": ["Header states no-date: 0, stale: 0, errors: 0 across 305 articles"]},
        "story_quality":     {"score": 9, "evidence": ["Commerzbank summaries name specific numbers: '€40 billion voluntary bid' and '12.51% of Commerzbank's stock' tendered", "Snowflake entries describe specific product releases and Anthropic partnership announcements with revenue detail", "Sodexo item quantifies 'first-quarter net income of $2.96 billion, or $2.30 a share'"]},
        "trust":             {"score": 9, "evidence": ["Header: errors 0, no-date 0, stale 0, dup 0 — cleanest header of the set", "URLs point to real, verifiable sources: bloomberg.com, wsj.com, reuters.com, businesswire.com, globenewswire.com"]}
      },
      "weighted": 8.10,
      "caps_applied": [],
      "final": 8.10,
      "verdict": "Best-in-class combination of clean dates, real URLs, sharp summaries, and adequate depth per company — the only clear caveat is a few wrong-entity slips on obscure niche names."
    },
    {
      "label": "E",
      "axes": {
        "precision":         {"score": 2, "evidence": ["Adidas 'ADIDAS PRO WORK' article about PPE footwear appears in nearly every company's result set (Alpek, Auriga, Berkshire Labels, Bloomberg, Borouge, Braroll, CBS News, CHEP, Coles, Constellium, CVS, etc.) — pure off-topic contamination on massive scale", "'Cloud.ru Aims for 2027 Data Center Launch in Moscow' by 'Science Editor Dr. Naomi Korr' at memesita.com surfaces across many company queries — same off-topic filler", "Berkshire Labels query returns unrelated Berkshire Hathaway/Buffett content plus 'BOBST Thalia UV Digital Inks' — mixed wrong-entity and generic industry", "CVS Pharmacy result includes an obviously fabricated-looking article 'Attorney General Bonta: CVS to Pay $36.5 Million' with einpresswire.com URLs — potential FP-halluc pattern"]},
        "coverage":          {"score": 9, "evidence": ["2334 total articles across every queried entity with 40+ articles per company", "Even niche entities like 'Braroll Acessorios Industriais' (47) and 'Jiangin Yonghe Packaging Products' (48) received dozens of results"]},
        "recency_integrity": {"score": 10, "evidence": ["Header states no-date: 0, stale: 0 across 2334 articles — every entry has a recent timestamp"]},
        "story_quality":     {"score": 5, "evidence": ["Some summaries are excellent (Coles ACCC blocking, Commerzbank UniCredit specifics)", "But many articles have autogenerated-sounding headlines and boilerplate summaries: 'ADIDAS PRO WORK' repeated verbatim across dozens of company queries", "Suspicious author bylines like 'News | 2026-06-10 | Quality Score: 90/100' at banehopper.com suggest AI-generated content farms"]},
        "trust":             {"score": 3, "evidence": ["Header errors: 33, dup: 14", "URLs from clearly low-trust domains: memesita.com, banehopper.com, kimsellssouthshore.com, licbdc.org, lalampepetrole.com — these read as content-farm/SEO-spam URLs unrelated to legitimate business news publishers", "Same 'Adidas Launches ADIDAS PRO WORK' aktiensensor.com article recycled as filler across dozens of unrelated companies is a strong FP-halluc/spam signal"]}
      },
      "weighted": 4.85,
      "caps_applied": ["trust", "precision"],
      "final": 4.00,
      "verdict": "Massive volume and perfect date coverage, but the same off-topic 'Adidas PRO WORK' and 'Cloud.ru' filler articles crossbleed across every entity from content-farm domains — trust is broken."
    }
  ],
  "ranking": ["D", "B", "C", "E", "A"],
  "ranking_rationale": {
    "1st": "D combines clean header counts (0 errors, 0 no-date, 0 stale, 0 dup), real-source URLs, sharp quantitative summaries, and consistent per-company depth — the only mainstream-quality result set here.",
    "2nd": "B has perfect recency and the crispest individual summaries but very thin coverage (69 articles total, many companies with 1 result) and a suspiciously uniform Bloomberg cluster; still edges C by avoiding the trust cap.",
    "3rd": "C would rank higher on summary quality but its 62-error count and total zero-returns for CBS News/Deloitte/Entertainment Partners/Green Bay Packaging/Lusha trigger the trust cap at 4.00.",
    "4th": "E has huge volume and perfect dates but is capped by trust (content-farm domains, repeated off-topic filler) and by precision (same Adidas/Cloud.ru article contaminating dozens of unrelated queries).",
    "5th": "A is disqualified by 100% no-date flags (4406/4406), boilerplate-only summaries, and wrong-entity contamination on virtually every query."
  }
}
```

## Notes

The most striking pattern across the run is the inverse relationship between volume and quality: A returned 4406 articles with zero usable dates and mostly boilerplate summaries, while B returned 69 articles that were nearly all clean and dated. E managed both scale and perfect dating but achieved this partly by recycling the same off-topic "Adidas PRO WORK" filler article across dozens of unrelated company queries, which is arguably worse than A's honest boilerplate because it looks legitimate at first glance. Only D and C achieved credible per-article quality, and C was undone by its high error rate leaving major companies (CBS News, Deloitte, Entertainment Partners) completely uncovered.

D's honest weaknesses: coverage still tails off for niche entities (CHEP got 1 article, Entertainment Partners got 1, Linklaters got 2, Fritz Foss got 1), and a handful of clear wrong-entity slips leaked through — the single Entertainment Partners hit is about UEG (United Entertainment Group), and the single CHEP hit is about a "Coalition for Home Equity Partnership" completely unrelated to the pallet-pooling company. So while D is unambiguously the best of the five, it should not be trusted blindly on obscure or acronym-heavy company names.