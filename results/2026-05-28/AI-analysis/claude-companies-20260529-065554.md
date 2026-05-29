# Companies Analysis — 20260529-065554

*Model: claude-opus-4-7 | Max articles per company per provider: 15*

*Provider labels were anonymised. See `decode-key-20260529-065554.json` to decode.*

---

```json
{
  "query_type": "companies",
  "providers": [
    {
      "label": "A",
      "axes": {
        "precision":         {"score": 9, "evidence": ["Borouge: 20 on-topic articles (Q1 2026 results, BlueAlp diaper recycling, AD Ports MoU)", "Commerzbank AG: clean cluster on UniCredit takeover battle, Q1 results, 3000 job cuts", "Dominion Energy: 20 results all on NextEra merger", "Minor noise — 'Cole's' LA restaurant + Infinite Coles entries under COLES query are FP-entity", "Husky Technologies: tight cluster of CEO/President appointments"]},
        "coverage":          {"score": 6, "evidence": ["27 of queried entities returned results, but Bloomberg (1 article), CHEP (1), Entertainment Partners (1), Linklaters (1), GREEN BAY PACKAGING (1), CVS PHARMACY (1 about Walgreens) are thinly covered", "Klockner Pentaplast and Klöckner Pentaplast both returned 5 identical articles — duplicate entity handling", "No results gaps not evident, but headline counts for several entities are low (1-3)"]},
        "recency_integrity": {"score": 10, "evidence": ["Header: no-date: 0, stale: 0 across 232 articles", "All Borouge, Commerzbank, Constellium dates within 90 days"]},
        "story_quality":     {"score": 8, "evidence": ["Borouge summaries informative: 'net profit nearly halved... logistics challenges hit revenues in March'", "Commerzbank: 'plans to cut 3,000 jobs to help it reach more ambitious profit targets'", "Some summaries truncated at field labels like 'Partnership:' or 'Step Down:' reducing readability"]},
        "trust":             {"score": 10, "evidence": ["Header: errors: 0, dup: 0", "URLs from Bloomberg, Reuters, Zawya, GlobeNewswire — no suspicious patterns", "CVS PHARMACY query returned a Walgreens article — minor FP-entity but URL legitimate"]}
      },
      "weighted": 8.55,
      "caps_applied": [],
      "final": 8.55,
      "verdict": "Tight, clean, on-topic, well-dated — the most reliable surface for an AI agent."
    },
    {
      "label": "B",
      "axes": {
        "precision":         {"score": 2, "evidence": ["ALPEK POLYESTER query returned 'Alpha Compute Completes GAMEE Acquisition', 'Alpex Solar TOPCon Cell Facility', 'SKG Pharma' — all wrong-entity", "BERKSHIRE LABELS query returned dozens of Berkshire Hathaway portfolio articles — wrong entity", "CHARTER NEX FILMS query returned 'SoFi Stablecoin', 'Tribeca AI film', 'NEX Mainnet on Coinbase' — wrong entity", "Bulk recurring noise across nearly every query: 'Tata 1mg Achieves Profit Milestone', 'Google Introduces Preferred Sources', 'RBI Drives Growth' appear in 25+ company sections"]},
        "coverage":          {"score": 7, "evidence": ["All queried entities returned ~45-50 articles each (high volume)", "Genuine Borouge, CBS News, Commerzbank, Dominion Energy clusters present beneath the noise", "Constellium query is dominated by SpaceX/Starlink/satellite articles — entity not actually covered"]},
        "recency_integrity": {"score": 10, "evidence": ["Header: no-date: 0, stale: 0 across 2512 articles", "Dates consistently May 2026"]},
        "story_quality":     {"score": 5, "evidence": ["Real articles have decent summaries (Borouge AD Ports MoU, Commerzbank AGM)", "Many summaries are raw scraped fragments: 'Image 25 Reuters Refinitiv' style boilerplate in noise articles", "Brazil-language entries for L M Goes Embalagens are full Portuguese summaries — usable"]},
        "trust":             {"score": 6, "evidence": ["Header: errors: 0, dup: 1", "URLs from real sources (Bloomberg, Reuters, Stocktitan) but also low-quality aggregators (headlinez.news, hollywoodrecord.com, briefglance.com, newser.com expert-time URLs look templated)", "Massive recurring articles across unrelated queries suggests bulk keyword-stuffed feed rather than entity-targeted search"]}
      },
      "weighted": 5.65,
      "caps_applied": ["precision"],
      "final": 5.0,
      "verdict": "High volume hides a precision disaster — same wrong-entity articles recycled across nearly every company query."
    },
    {
      "label": "C",
      "axes": {
        "precision":         {"score": 9, "evidence": ["Borouge: clean 4-article cluster on OMV/XRG combination and Patrick Jany CFO", "Commerzbank AG: UniCredit voluntary exchange offer and AGM dividend approval, on-topic", "Dominion Energy: 7 articles all on NextEra merger ($67B, McGuireWoods advisory, POWER Magazine)", "Sigma Chemtrade: provider explicitly notes no match and returns synthesis — transparent rather than fabricated"]},
        "coverage":          {"score": 4, "evidence": ["Only 98 total articles across all entities — many companies return 1-3 results", "Bloomberg returns 0 results, ExxonMobil 1, International Paper 1, Linklaters 2, Husky Technologies 0 visible", "L M Goes Embalagens entry admits 'No relevant recent news article found'", "ZETA TECHNICAL SERVICES entry admits no match and pivots to Zeta Global"]},
        "recency_integrity": {"score": 10, "evidence": ["Header: no-date: 0, stale: 0 across 98 articles", "All Dominion Energy NextEra dates clustered around May 18-20 2026"]},
        "story_quality":     {"score": 9, "evidence": ["Summaries are analytical and decision-useful: 'Dominion shareholders will receive a fixed exchange ratio... transaction expected to close in 12-18 months'", "Commerzbank: 'approved a dividend of €1.10 per share and authorisation for further share buybacks'", "Snowflake DEF 14A summary cites '29% product revenue growth'"]},
        "trust":             {"score": 8, "evidence": ["Header: errors: 0, dup: 0", "URLs from Reuters, Business Wire, GlobeNewswire, official company IR pages, McGuireWoods", "One example.com URL for Universal McCann entries ('https://example.com/universal-mccann-general-mills-...') is suspicious — possible hallucinated placeholder", "Sigma Chemtrade entry uses search synthesis URL pattern — transparent"]}
      },
      "weighted": 7.85,
      "caps_applied": [],
      "final": 7.85,
      "verdict": "Low volume but high quality — analytical summaries and transparent no-match handling, marred by occasional example.com placeholder URLs."
    },
    {
      "label": "D",
      "axes": {
        "precision":         {"score": 8, "evidence": ["Commerzbank AG: clean 5-article Bloomberg cluster on UniCredit bid rejection, AI cost cuts, 3000 job cuts", "Dominion Energy: 6 articles all on NextEra merger with company press releases", "Entertainment Partners query returns mostly off-topic FP-entity matches (Brillstein Promotes, SeatGeek + Beemok Sports, Seaport Entertainment + Public Records, Lucky Strike + Giants) — name-only matches", "Jindal Films cluster on Jindal Poly Films SEBI notice and NCLT class action is correct entity"]},
        "coverage":          {"score": 6, "evidence": ["140 articles across queried entities", "Husky Technologies returned 0 articles, 8 errors", "HPCL Mittal Energy only 2 articles with 1 error", "DOMINION ENERGY had 1 error; HAIER had 1 error"]},
        "recency_integrity": {"score": 10, "evidence": ["Header: no-date: 0, stale: 0", "Dates consistently within window"]},
        "story_quality":     {"score": 8, "evidence": ["Borouge: 'Q1 2026 performance with $1.2 billion revenue, $343 million adjusted EBITDA, and $156 million net profit despite logistics disruptions'", "International Paper: 'breaks ground on $225 million sustainable packaging facility in Brandon, Mississippi'", "Sodexo: 'Revenue fell 3.7% to €12.02 billion... shares fell 13-16%'"]},
        "trust":             {"score": 7, "evidence": ["Header: errors: 11, dup: 2 (Jindal Films, Linklaters)", "URLs legitimate (Reuters, CNBC, PRNewswire, GlobeNewswire, LinkedIn for Snowflake earnings)", "Husky Technologies 8 errors and 0 results is a significant failure mode", "Snowflake Q1 earnings sourced from LinkedIn posts rather than primary releases — lower-grade sourcing"]}
      },
      "weighted": 7.65,
      "caps_applied": [],
      "final": 7.65,
      "verdict": "Strong content where it works, but 11 errors and one entity with zero results expose reliability gaps."
    },
    {
      "label": "E",
      "axes": {
        "precision":         {"score": 1, "evidence": ["Bloomberg query returns articles like 'Iran War Truce', 'Apple iOS 27 Photos' — generic Bloomberg.com headlines not about the news outlet", "Borouge query returns 'Novo Nordisk Wegovy', 'Sumitomo Pharma shelf registration', 'Brazil finance minister' — wrong entity macro noise", "COLES query returns 'Sky News Business Editor Ross Greenwood reacts', 'Coca-Cola Profit Rises', H&M, Kroger — wrong entity and Facebook video summaries", "Summaries are raw scraped boilerplate: 'Image 18 Image 19 Image 20 Dec 22, 2025 Reuters Mergers and acquisitions' across hundreds of entries"]},
        "coverage":          {"score": 5, "evidence": ["4221 articles total but quality is unusable; nominally every entity has 50-100 results", "Entities are not actually covered substantively — e.g., Klöckner Pentaplast results are Kuehne+Nagel, Kimberly-Clark, Thyssenkrupp"]},
        "recency_integrity": {"score": 0, "evidence": ["Header: no-date: 4221 of 4221 articles", "Every single article flagged [NO DATE ⚠]"]},
        "story_quality":     {"score": 1, "evidence": ["Most summaries are nav menus and cookie-banner-style scrapes: 'Skip to main content', 'Image 1 Get started News /Reuters', 'Subscribe Sign In'", "Genuine article text rare; e.g., Berkshire entry: 'Berkshire took a $2.6 billion stake in Delta Airlines' is one of few usable lines"]},
        "trust":             {"score": 3, "evidence": ["Header: errors: 0, dup: 104", "URLs include real publications (WSJ, Reuters, CNBC) but also scraped TradingView wrapper pages that repeat the same boilerplate", "104 duplicates across the dataset"]}
      },
      "weighted": 1.85,
      "caps_applied": ["recency_hard", "trust", "precision"],
      "final": 1.85,
      "verdict": "Catastrophic: no dates at all, content is mostly cookie banners and navigation scrape, and queries return wrong entities at scale."
    }
  ],
  "ranking": ["A", "C", "D", "B", "E"],
  "ranking_rationale": {
    "1st": "A: highest precision with clean entity targeting, zero errors/dupes/no-dates, and informative summaries.",
    "2nd": "C: precision near A's level with strong analytical summaries, but low volume and one suspicious example.com URL pattern hold it below.",
    "3rd": "D: solid Bloomberg/Reuters sourcing for major entities, but 11 errors and Husky Technologies returning zero results signal real reliability gaps.",
    "4th": "B: high volume but precision is wrecked by the same handful of wrong-entity articles (Tata 1mg, Google Preferred Sources) recycled across nearly every company query.",
    "5th": "E: every article missing a date, summaries are scraped boilerplate, 104 duplicates, and queries routinely return wrong entities — triple-capped."
  }
}
```

## Notes

The most striking pattern across this run is the precision/volume inverse correlation: provider E returned the most articles (4221) and the worst content, while provider C returned the fewest (98) with the highest analytical quality. Provider B's failure mode is subtler than E's — its dates and URLs look legitimate, but a small set of generic articles ("Tata 1mg Achieves Profit Milestone", "Google Introduces Preferred Sources", "Spacex Starlink Nabs American Airlines") appears under 25+ unrelated company queries, suggesting weak entity matching rather than no matching. Provider A and D both rely heavily on Bloomberg/Reuters/company IR for the same big stories (NextEra-Dominion, UniCredit-Commerzbank, Borouge Q1), and they tend to agree on what matters.

Provider A's honest weaknesses: coverage is uneven (Bloomberg, CHEP, Entertainment Partners, Linklaters, Green Bay Packaging each got only one article, and CVS Pharmacy's lone result is actually a Walgreens story — a quiet FP-entity slip), and several summaries are truncated at field labels like "Partnership:" or "Step Down:" which reduces story_quality below where the underlying article would put it. It also returned duplicate entities for Klockner Pentaplast and Klöckner Pentaplast as separate queries with identical 5-article result sets, which the provider did not deduplicate.