# Industries Analysis — 20260513-203319

*Model: claude-opus-4-7 | Max articles per topic per provider: 15*

*Provider labels were anonymised. See `decode-key-20260513-203319.json` to decode.*

---

```json
{
  "query_type": "industries",
  "providers": [
    {
      "label": "A",
      "axes": {
        "precision": {"score": 6, "evidence": [
          "CONSTRUCTION|Europe: on-topic UK construction PMI Reuters article 2026-03-05 is solid TP",
          "Cocoa|Asia Pacific: 'Olam Group announces management changes' URL is just olamgroup.com homepage — FP-not-news",
          "LABORATORY|Africa: results are about polymer thermal analysis (TA Instruments, MDPI Polymers) not African laboratory industry — FP-entity",
          "Film|CN: heavy reliance on Grand View / Persistence / 24 Chemical Research market-report landing pages (≥4 of 5) — surplus FP-not-news"
        ]},
        "coverage": {"score": 3, "evidence": [
          "9 of 25 queried topics returned zero articles: BOARD|Eastern Asia, CLEANING SUPPLIES|New England, CONVERTING AND FINISHING MACHINES|Southern Asia, Converter Foil|Northern America, Film Distribution|Midwest, Flexible Packaging|CN, LIQUIDS|Southern Africa, PACKAGING|Oceania, PE Resins|US, Packaging Boxes|IN, Whey Ingredients|Northern Europe",
          "Road Freight|Europe returned only 1 article (londonsecrets.icu blog-style)",
          "Strong coverage where it works: LOGISTICS|Western Africa 7 articles, OIL/FUEL|SE Asia 7 articles"
        ]},
        "recency_integrity": {"score": 10, "evidence": [
          "Header: no-date 0, stale>90d 0 across all 68 articles",
          "All dated articles fall in Feb–May 2026 window"
        ]},
        "story_quality": {"score": 7, "evidence": [
          "OIL/FUEL|SE Asia: Reuters/Bloomberg/Guardian summaries cite specific figures (B40 mandate, 50% palm biodiesel, fuel reserves days)",
          "PAPER|Northern Europe: summaries name EUDR, Finland/Sweden kraft, 5.16% specialty CAGR",
          "LABORATORY|Africa Yahoo Finance summary is generic 'advanced materials market to double' boilerplate"
        ]},
        "trust": {"score": 2, "evidence": [
          "Header: errors 102 — by far the highest error count of any provider",
          "BOARD|Eastern Asia: 7 errors, 0 articles; CLEANING SUPPLIES|New England: 8 errors, 0 articles; Converter Foil|Northern America: 9 errors, 0 articles; Whey Ingredients|Northern Europe: 9 errors, 0 articles",
          "Olam Group 'announcement' cites olamgroup.com root URL — suspicious sourcing"
        ]}
      },
      "weighted": 5.45,
      "caps_applied": ["trust"],
      "final": 4.0,
      "verdict": "Decent precision and clean dates on the topics that worked, but 102 errors and 11 empty topics gut its usefulness."
    },
    {
      "label": "B",
      "axes": {
        "precision": {"score": 6, "evidence": [
          "PAPER|Northern Europe: International Paper acquiring NORPAC for $360M, Sappi Europe price increase — strong TPs",
          "PE Resins|US: ExxonMobil corporate sustainability page and ICIS PET resin insight are on-topic",
          "BOARD|Eastern Asia: 3 of 4 articles are tangential analogies ('analogous to BOARD industry', 'For BOARD procurement') — FP-entity stretching",
          "CONSTRUCTION|Europe: returns 'Top Electrical Engineering Companies in Germany' (f6s.com directory) and Excel Electric About Us page — FP-not-news",
          "Cocoa|Asia Pacific: CocoaSupply Australasia is a company homepage (cocoasupply.au) — FP-not-news"
        ]},
        "coverage": {"score": 9, "evidence": [
          "All 25 topics returned at least 1 article — every queried entity covered",
          "Whey Ingredients|Northern Europe: 3 articles naming Arla, FrieslandCampina, EU tariffs",
          "Road Freight|Europe: 2 IRU/Upply/Ti Q1 2026 reports — on-topic"
        ]},
        "recency_integrity": {"score": 10, "evidence": [
          "Header: no-date 0, stale 0 across all 80 articles",
          "Dates span Feb–May 2026 cleanly"
        ]},
        "story_quality": {"score": 7, "evidence": [
          "PAPER|Northern Europe Sappi/Burgo/Lecta price-hike summary gives specific percentages and effective dates",
          "PE Resins|US Milliken LeneX UGN-52 summary specifies HDPE/LLDPE film application",
          "Some entries are thin directory/About Us blurbs (Mayer Brown LatAm capabilities, Flex HR benefits page)"
        ]},
        "trust": {"score": 10, "evidence": [
          "Header: errors 0, dup 0",
          "URLs resolve to identifiable publications (Reuters, PRNewswire, ICIS, Mordor Intelligence)",
          "No hallucinated-looking URLs detected"
        ]}
      },
      "weighted": 7.65,
      "caps_applied": [],
      "final": 7.65,
      "verdict": "Best balance — full coverage, clean dates, zero errors, but precision suffers from About Us pages and analogy-stretched matches."
    },
    {
      "label": "C",
      "axes": {
        "precision": {"score": 2, "evidence": [
          "Distribution Services|Northern America: both results (Pocketalk translation, Christian Lingua) are language-translation services — FP-entity",
          "PROFESSIONAL SERVICES|LATAM: 6 of 7 articles are Bitget Wallet / CZR Exchange crypto press releases — FP-entity",
          "LOGISTICS|Western Africa: only article is Geekplus/Mindugar warehouse automation in Latin America — wrong region, FP-entity",
          "Whey Ingredients|Northern Europe section is legitimately strong (Arla, FrieslandCampina, Carbery)"
        ]},
        "coverage": {"score": 2, "evidence": [
          "Only 7 of 25 topics returned any results — 18 topics entirely missing (no BOARD, Construction, Film, Packaging, Paper, PE Resins, etc.)",
          "Whey Ingredients|Northern Europe got 16 articles while most topics got 0"
        ]},
        "recency_integrity": {"score": 10, "evidence": [
          "Header: no-date 0, stale 0",
          "Dates clean Feb–May 2026"
        ]},
        "story_quality": {"score": 5, "evidence": [
          "Whey Ingredients summaries quote specific figures (Arla 35.83ppl, Lakeland €25.2m profit, NSIA $496m deal)",
          "PROFESSIONAL SERVICES|LATAM Bitget entries are press-release boilerplate ('introducing a limited-edition International Women...')",
          "Headline fragments like 'Expands Global Footprint' shown as full title"
        ]},
        "trust": {"score": 8, "evidence": [
          "Header: errors 0, dup 0",
          "URLs map to recognizable outlets (Reuters, S&P Global, Irish Times, GlobeNewswire)",
          "No hallucinated URLs spotted"
        ]}
      },
      "weighted": 3.65,
      "caps_applied": ["precision"],
      "final": 3.65,
      "verdict": "Crippled by 18 empty topics and crypto-spam contamination of LATAM professional services; only the whey topic is genuinely useful."
    },
    {
      "label": "D",
      "axes": {
        "precision": {"score": 1, "evidence": [
          "CLEANING SUPPLIES|New England: returns FT 'cleaning products with skincare credentials', Ebay layoffs, ITC ENDS vape probe — overwhelmingly FP-entity",
          "BOARD|Eastern Asia: 'Japan’s government taps academics for BOJ board', 'Fox Factory Announces Strategic Board Refresh' — wrong sense of 'board', FP-entity",
          "Film|CN: results about Steinberg Law Firm scholarship, McCready Law firm partner — completely off-topic FP-entity",
          "LIQUIDS|Southern Africa: returns Sika acquiring Turkish Akkim, Brazil Lula chemical tax, Mexico Alpek polyester — wrong region/entity"
        ]},
        "coverage": {"score": 7, "evidence": [
          "All 25 topics returned articles (volume-wise complete)",
          "But coverage of right entities is illusory — e.g., CONSTRUCTION|Europe returns mostly UK/US construction (Construction Dive, Skanska US uncertainty)"
        ]},
        "recency_integrity": {"score": 0, "evidence": [
          "Header: no-date 2025 — every single one of 2025 articles is undated (100%)",
          "Cannot verify recency for any item"
        ]},
        "story_quality": {"score": 4, "evidence": [
          "Many summaries are scraped nav/footer fragments ('More news from Reuters Image 21 Image 22 Image 23 Dec 22, 2025 Reuters Mergers...')",
          "TradingView entries repeat identical boilerplate cookie/nav content as 'summary'",
          "Some genuine summaries present (Construction News Glenigan analysis)"
        ]},
        "trust": {"score": 3, "evidence": [
          "Header: dup 46 — substantial duplication (e.g., Daily Manufacturing News Digest appears as DUP of #4 multiple times in CONVERTING topic)",
          "Header: errors 0 but recency is structurally broken (0 dates on 2025 articles)",
          "Scraped boilerplate suggests low-quality extraction pipeline"
        ]}
      },
      "weighted": 2.95,
      "caps_applied": ["recency_hard", "precision"],
      "final": 2.95,
      "verdict": "Massive volume hides total recency failure (zero dates on 2025 results) plus rampant wrong-sense matches and duplicates."
    },
    {
      "label": "E",
      "axes": {
        "precision": {"score": 7, "evidence": [
          "OIL/FUEL|SE Asia: Malaysia B15 biodiesel rollout, Vietnam PVOIL E10 nationwide, Indonesia premium diesel hike — strong on-topic TPs",
          "Whey Ingredients|Northern Europe: FrieslandCampina €90M whey expansion across multiple credible sources (NutraIngredients, ESM Magazine, Just-Food)",
          "Film|CN: BOPP/BOPET film coverage on-topic (Jindal, Mitsubishi Polyester, Chinaplas BOBST)",
          "CONVERTING AND FINISHING MACHINES|Southern Asia: Pacific Group ordering Webtech Aeroflex S4, Khyati JB-106C — directly on-topic; but also includes generic Pascal Lamy WTO commentary as FP-entity",
          "HR SERVICES|Mid Atlantic: Marsh McLennan/TriBridge, Horizon HealthEZ NJ — solid TPs"
        ]},
        "coverage": {"score": 10, "evidence": [
          "All 25 topics returned 40+ articles each; e.g., LOGISTICS|Western Africa 45, OIL/FUEL|SE Asia 50, Whey Ingredients|N Europe 49",
          "Even niche queries like Molasses|Oceania get 48 articles (Fiji FSC, Australia sugarcane)"
        ]},
        "recency_integrity": {"score": 10, "evidence": [
          "Header: no-date 0, stale 0 across all 1297 articles",
          "Dates span Apr–May 2026 with timestamps"
        ]},
        "story_quality": {"score": 8, "evidence": [
          "PE Resins|US: 'Dow Chemical Announces 100% Cumulative Polyethylene Price Hike' summary with specific 30-cent April nominations",
          "FrieslandCampina entries cite €90M figure, 2028 capacity timeline, Netherlands location",
          "Some entries have garbled OCR-style fragments ('How CBN reforms are building shock absorbers' appears across many topics as off-topic filler)"
        ]},
        "trust": {"score": 7, "evidence": [
          "Header: errors 6 (all in CLEANING SUPPLIES|New England), dup 20 of 1297 = 1.5%",
          "Same 'How CBN reforms' Nigeria article surfaces repeatedly across unrelated topics (PROFESSIONAL SERVICES|LATAM, Packaging Boxes|IN, LIQUIDS, Converter Foil) — indicates weak topic filtering",
          "Recognized publishers dominate (Reuters, Bloomberg, PRNewswire, ICIS, FoodNavigator)"
        ]}
      },
      "weighted": 8.05,
      "caps_applied": [],
      "final": 8.05,
      "verdict": "Highest precision and volume with clean dates and minimal errors, marred only by a recurring off-topic Nigeria CBN article leaking across queries."
    }
  ],
  "ranking": ["E", "B", "A", "C", "D"],
  "ranking_rationale": {
    "1st": "E — strong precision, complete coverage across all 25 topics, zero no-date, only 6 errors and 1.5% dups; the cross-topic leakage of one Nigeria article is the main blemish.",
    "2nd": "B — flawless date integrity and zero errors, full topic coverage, but precision held back by About Us pages, market-report landing pages, and 'analogous to BOARD' stretching.",
    "3rd": "A — clean dates and reasonable precision where it returns results, but 102 errors and 11 empty topics make it unreliable; trust cap pulls it to 4.0.",
    "4th": "C — only 7 of 25 topics populated; LATAM professional services is contaminated by Bitget crypto press releases; precision cap applies.",
    "5th": "D — every 2025 article is undated (recency hard cap) plus wrong-sense matches ('Board' as governance, 'Film' as law firms) and 46 dups; the worst combination of structural failures."
  }
}
```

## Notes

The run reveals a sharp split between providers that index broadly versus those that filter strictly. D returned the largest article count but with zero usable dates and rampant homonym matches ('board' = corporate governance, 'film' = unrelated companies whose name contains the word) — quantity without integrity. C is the opposite failure mode: tight pipeline but only 7 topics populated, and its LATAM professional-services slot is overrun by Bitget Wallet crypto press releases, suggesting weak topic-anchoring. A's 102-error count is striking — it failed to return anything for 11 of 25 topics, indicating a fragile retrieval layer rather than a recency or precision problem.

E, the top-ranked provider, is not without weaknesses: the same Nigerian CBN reform article appears as filler across Packaging Boxes|IN, LIQUIDS|Southern Africa, Converter Foil|Northern America, and PROFESSIONAL SERVICES|LATAM, which indicates a fallback mechanism that injects loosely-relevant macro stories when topic-specific signal is thin. Its 1297-article volume also means a human consumer must sift; precision is good but not laser. B is the safer choice if the consumer wants compact, reliably-dated results across every topic, accepting that some entries will be market-report landing pages or supplier About Us pages rather than hard news.