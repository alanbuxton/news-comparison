# Companies Analysis — 20260513-203319

*Model: claude-opus-4-7 | Max articles per company per provider: 15*

*Provider labels were anonymised. See `decode-key-20260513-203319.json` to decode.*

---

```json
{
  "query_type": "companies",
  "providers": [
    {
      "label": "A",
      "axes": {
        "precision":         {"score": 7, "evidence": ["ExxonMobil: 9 clean Reuters/Bloomberg articles on Trump/Venezuela meeting, Q1 earnings, Hong Kong fuel station sale", "Commerzbank AG: 6 on-topic articles incl. Reuters '3,000 job cuts, raises targets as it fends off UniCredit'", "KRC Custom Manufacturing returns wrong-entity hits: KKR Solid Surface partnership and Kilroy Realty (KRC ticker) earnings", "Universal McCann: returned 'Universal Orlando Resort announces major changes' — wrong entity"]},
        "coverage":          {"score": 5, "evidence": ["Entertainment Partners: 0 articles, 1 error", "HPCL Mittal Energy: 0 articles, 5 errors", "Klockner Pentaplast and Klöckner Pentaplast: 0 articles, 5 errors each", "Strong coverage on Borouge (6), ExxonMobil (9), Westrock (8), Commerzbank (6)"]},
        "recency_integrity": {"score": 10, "evidence": ["Header: no-date: 0, stale: 0 across all 60 articles", "All Borouge articles dated within Mar-May 2026", "All Commerzbank articles dated May 2026"]},
        "story_quality":     {"score": 8, "evidence": ["Commerzbank Reuters summary: 'plans to cut 3,000 jobs to achieve more ambitious profit targets and defend against a hostile takeover'", "ExxonMobil: 'reported a 6% reduction in global production in Q1 due to the Iran conflict'", "International Paper: '$5.97 billion and earnings from continuing operations of $76 million' — decision-ready"]},
        "trust":             {"score": 4, "evidence": ["Header: errors: 25 — very high error rate", "HPCL Mittal Energy: 5 errors / 0 articles", "Klockner Pentaplast: 5 errors / 0 articles", "Klöckner Pentaplast: 5 errors / 0 articles, Jindal Films: 3 errors"]}
      },
      "weighted": 6.85,
      "caps_applied": ["trust"],
      "final": 4.0,
      "verdict": "Clean dates and strong story quality, but 25 errors and four queried companies returning zero results crater trust."
    },
    {
      "label": "B",
      "axes": {
        "precision":         {"score": 5, "evidence": ["Bloomberg: 4 articles read like hallucinated content — 'Bloomberg Launches AI-Powered Corporate Finance Analytics Tool' with suspiciously neat URL bloomberg.com/news/articles/2026-05-07/bloomberg-launches-ai-corporate-finance-tool", "Commerzbank AG: all 4 URLs (reuters.com/.../commerzbank-fintech-partnership-ai-procurement-2026-05-07, ft.com/content/bafin-commerzbank-supplier-risk-regulations-2026) follow suspicious neat patterns not matching real published content", "Jiangin Yonghe Packaging Products: 3 articles with implausibly tidy URLs (chinadaily.com.cn/business/2026-04-15/yonghe-financing-deal.htm)", "CBS News: includes YouTube video link and AeroVironment article that is about AV, not CBS"]},
        "coverage":          {"score": 7, "evidence": ["Returns articles for all 15 queried entities including Jiangin Yonghe Packaging Products (3 articles)", "Entertainment Partners: 3 articles where Provider A returned 0", "Sigma Chemtrade: 3 results but one is staffing list 'Top 15 Manufacturing Employers in Baltimore'"]},
        "recency_integrity": {"score": 10, "evidence": ["Header: no-date: 0, stale: 0", "All 52 articles dated Feb-May 2026"]},
        "story_quality":     {"score": 7, "evidence": ["Commerzbank: 'unveiled a new product innovation: the SupplyChain Finance Hub, a blockchain-based platform' — decision-ready if true", "ExxonMobil Q1 2026: '$4.2 billion ($8.8 billion excluding timing effects)'", "Universal McCann: returned Universal Corp and Universal Music Group articles — wrong-entity name-drops"]},
        "trust":             {"score": 3, "evidence": ["Header: errors: 0 but content quality suggests synthesized articles", "Bloomberg URLs like bloomberg.com/news/commerzbank-supplychain-finance-hub-launch-2026 don't follow Bloomberg's real URL conventions", "Jiangin Yonghe articles cite 'Sina Finance' and 'Yicai Global' with date-slug URL patterns inconsistent with those sites", "Multiple sources show identical formulaic 'partnership/regulatory/innovation' framing across unrelated entities — hallucination signature"]}
      },
      "weighted": 6.25,
      "caps_applied": ["trust"],
      "final": 4.0,
      "verdict": "Suspiciously neat URL patterns and formulaic content across providers strongly suggest hallucination; high trust risk."
    },
    {
      "label": "C",
      "axes": {
        "precision":         {"score": 9, "evidence": ["Borouge: 20 articles, all clearly on-topic (Zawya, AGBI, Hydrocarbon Processing covering logistics deals, Q1 results, China JV)", "Commerzbank AG: 20 articles all about UniCredit takeover battle, job cuts, EIB grid deal", "International Paper: 20 articles all covering NORPAC acquisition, Q1 results, Mississippi plant", "Minor wrong-entity slip: CBS News list includes WCBI TV (CBS affiliate) Tim Cook story which is name-drop, not CBS-specific"]},
        "coverage":          {"score": 9, "evidence": ["Returns articles for all 16 queried entities including HPCL Mittal Energy (6), Husky Technologies (10), Klockner Pentaplast (5)", "Entertainment Partners: 2 articles — light but present", "Linklaters: only 1 article (lease expansion)"]},
        "recency_integrity": {"score": 10, "evidence": ["Header: no-date: 0, stale: 0 across 137 articles", "All Borouge articles between Apr-May 2026", "All Klöckner Pentaplast articles April 2026"]},
        "story_quality":     {"score": 9, "evidence": ["Borouge Q1: 'revenue of $1,175 million, down 17% YoY and 30% QoQ, impacted by logistics disruptions'", "International Paper: 'net sales of $5.97bn, up 13.4% compared with $5.2bn a year earlier'", "HPCL Mittal Energy: 'HMEL has increased LPG output at its Guru Gobind Singh Refinery from 1,000 tonnes to 3,000 tonnes per day'"]},
        "trust":             {"score": 10, "evidence": ["Header: errors: 0, dup: 0", "Real-looking source URLs (zawya.com, reuters.com, investing.com, packaging-gateway.com)", "No hallucination signatures"]}
      },
      "weighted": 9.20,
      "caps_applied": [],
      "final": 9.20,
      "verdict": "Highest-volume clean result set with strong precision, full coverage, real URLs, and decision-ready summaries."
    },
    {
      "label": "D",
      "axes": {
        "precision":         {"score": 1, "evidence": ["Header: no-date: 1931 of 1931 — every article is undated, classified as off-scope per rubric", "Borouge bucket dominated by unrelated TradingView aggregator pages: 'Brookfield, Gic Seek $2 Billion Loan For National Storage Deal', 'China's NetEase Q4 revenue rises'", "Commerzbank: many on-topic stories but all undated; e.g. CNBC 'Commerzbank boss pledges to defend shareholders'", "Bloomberg bucket: bloomberglaw.com pages returned as raw boilerplate ('### Products Bloomberg Terminal Data Trading Risk Compliance Indices')"]},
        "coverage":          {"score": 8, "evidence": ["Returns articles for all 18 queried entities including Braroll Acessorios Industriais (82), Fritz Foss (98), Dine Cartonnages (84)", "However: Braroll, Fritz Foss, Dine, L M Goes results are nearly all macro/unrelated Reuters wire stories not about the queried entity"]},
        "recency_integrity": {"score": 0, "evidence": ["Header: no-date: 1931 — 100% undated", "Every single article flagged [NO DATE ⚠]", "Per rubric, NO_DATE counts as FP-no-date / off-scope"]},
        "story_quality":     {"score": 2, "evidence": ["Bloomberg articles are raw scraped boilerplate: 'Products Bloomberg Terminal Data Trading Risk Compliance Indices'", "Borouge TradingView snippets show navigation menus: 'More news from Reuters... Dec 22, 2025 Reuters Mergers and acquisitions'", "Few articles like CBS News AP story have real summaries"]},
        "trust":             {"score": 5, "evidence": ["Header: errors: 0, dup: 27", "URLs appear real but content scraping captured boilerplate/menu chrome instead of article body", "Header dup: 27 confirms duplicate retrieval problem"]}
      },
      "weighted": 2.30,
      "caps_applied": ["recency_hard", "precision"],
      "final": 2.30,
      "verdict": "Catastrophic: 100% of 1931 articles undated and most summaries are scraped boilerplate; fails the recency and not-news tests across the board."
    },
    {
      "label": "E",
      "axes": {
        "precision":         {"score": 6, "evidence": ["Borouge: 47 clean on-topic articles (Zawya, Hydrocarbon Processing on XLPE plant, Q1 results)", "Westrock: 47 articles all covering Westrock Coffee Q1 and Smurfit Westrock — on-topic", "But Braroll Acessorios Industriais: 50 Portuguese-language articles like 'Indústria paulista de troféus amplia seu controle com ERP' and 'Carlos Roberto Barbery é novo diretor-presidente no Brasil da Whirlpool' — none about Braroll itself (FP-entity, wrong-region per rubric: non-English for non-local entity is FP)", "L M Goes Embalagens, Dine Cartonnages, Jiangin Yonghe: 50 articles each but mostly industry roundups and unrelated companies (e.g. Stora Enso, Duni Group for Dine Cartonnages)", "Fritz Foss: 50 articles mostly unrelated (Fritz Farms in North Platte, Fazeshift fintech, Panavision Fritz Heinzle)"]},
        "coverage":          {"score": 9, "evidence": ["Returns results for all 21 queried entities", "Strong on Commerzbank AG (46), CBS News (46), ExxonMobil (47), Borouge (47), Westrock (47), Husky Technologies (48)"]},
        "recency_integrity": {"score": 10, "evidence": ["Header: no-date: 0, stale: 0 across 1158 articles", "All Commerzbank articles dated May 2026", "All Westrock articles dated April-May 2026"]},
        "story_quality":     {"score": 8, "evidence": ["Commerzbank: 'plans to cut 3,000 jobs to help it reach more ambitious profit targets' (RTE) — decision-ready", "Westrock Coffee Q1: 'net sales rising 44% to $308.8 million and adjusted EBITDA more than tripling to $26 million'", "Borouge Q1: 'net profit nearly halved in the first quarter of 2026, as logistics challenges hit revenues'", "Some entries are Facebook/Instagram social posts (e.g. 'BCG's Global Asset Management Report' Instagram link) — FP-not-news per rubric"]},
        "trust":             {"score": 7, "evidence": ["Header: errors: 0, dup: 29", "URLs appear real and resolvable", "Some social-media URLs (facebook.com, instagram.com) violate rubric's not-news rule but at low rate", "Several entity buckets clearly contain wrong-entity articles indicating weak query disambiguation"]}
      },
      "weighted": 7.30,
      "caps_applied": [],
      "final": 7.30,
      "verdict": "Massive coverage with clean dates, but wrong-entity bleed for obscure companies (Braroll, Fritz Foss, Dine Cartonnages) drags precision down."
    }
  ],
  "ranking": ["C", "E", "A", "B", "D"],
  "ranking_rationale": {
    "1st": "C: clean dates, real sources, full coverage, decision-ready summaries, zero errors or duplicates.",
    "2nd": "E: huge volume and full coverage with clean dates, but precision suffers from wrong-entity bleed on obscure companies and some social-media noise.",
    "3rd": "A: clean dates and good summaries when present, but 25 errors and four companies returning zero results cap trust and final score.",
    "4th": "B: looks polished but the suspiciously neat URLs and formulaic content across unrelated companies point to likely hallucination — high trust risk.",
    "5th": "D: 100% no-date results and raw boilerplate summaries make virtually all 1931 articles unusable despite broad entity coverage."
  }
}
```

## Notes

The run exposes a sharp split between providers that retrieve real, dated articles (C, E, and A) and those that either hallucinate (B) or scrape boilerplate without dates (D). Provider D's 1931-article haul with zero dates is the most striking failure mode — sheer volume cannot rescue a feed where every result is flagged off-scope. Provider B's risk is subtler but more dangerous for an AI agent: the content reads plausibly but the URL patterns (bloomberg.com/news/commerzbank-supplychain-finance-hub-launch-2026, reuters.com/business/finance/commerzbank-fintech-partnership-ai-procurement-2026-05-07) are too clean and too thematically consistent across providers to be genuine.

The top-ranked Provider C is not flawless: Linklaters returned only 1 article, Entertainment Partners only 2, and the CBS News bucket includes a WCBI affiliate piece about Tim Cook that is really an Apple story. But across 137 articles it has no errors, no duplicates, no stale or no-date hits, and the summaries actually let a user decide whether to click. That combination beats Provider E's much larger but noisier haul, where obscure Portuguese-named companies (Braroll, L M Goes, Dine Cartonnages) returned 50-article buckets that are almost entirely wrong-entity industry filler.