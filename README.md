# AI News Provider Comparison

Benchmarking news search providers against each other on the same queries, then using an AI judge to score the results.

Providers currently in the comparison:

- [Exa](https://exa.ai)
- [Linkup](https://linkup.so)
- [Perplexity](https://perplexity.ai)
- [Syracuse](https://syracuse.1145.am) *(author's project)*
- [Tavily](https://tavily.com)

## How it works

Two types of query are benchmarked:

- **Company queries** — news about specific named companies (e.g. ExxonMobil, Commerzbank, Klöckner Pentaplast). The mix deliberately includes large well-known companies, mid-tier companies, and small/obscure companies with low digital footprint.
- **Industry/location queries** — news about an industry sector in a geography (e.g. PE Resins in the US, Road Freight in Europe).

For each query, every provider is called with the same parameters and its results are written to a shared CSV. An AI judge then scores the results.

## Running the benchmark

### 1. Setup

Copy `.env.sample` to `.env` and fill in your API keys:

```sh
cp .env.sample .env
```

Keys needed:

| Variable | Provider |
|---|---|
| `EXA_API_KEY` | Exa |
| `LINKUP_API_KEY` | Linkup |
| `PERPLEXITY_API_KEY` | Perplexity |
| `SYRACUSE_API_KEY` | Syracuse |
| `TAVILY_API_KEY` | Tavily |
| `ANTHROPIC_API_KEY` | Claude (for analysis step) |

### 2. Run the comparison

```sh
uv run python main.py 2026-03-08
```

This writes results to `results/2026-03-08/`:

```
results/2026-03-08/
  companies.csv     # all provider results for company queries
  industries.csv    # all provider results for industry/location queries
  errors/           # per-provider error logs
```

### 3. Run the AI analysis

```sh
uv run python analyse.py results/2026-03-08
```

This writes to `results/2026-03-08/AI-analysis/`:

```
  claude-companies-{timestamp}.md    # scored analysis for company queries
  claude-industries-{timestamp}.md   # scored analysis for industry queries
  decode-key-{timestamp}.json        # maps A/B/C/D/E back to real provider names
```

You can also analyse a previous run:

```sh
uv run python analyse.py results/2026-03-02
```

And use a cheaper model for quick iteration:

```sh
uv run python analyse.py results/2026-03-08 --model claude-sonnet-4-6
```

## Anti-bias design

The author of this benchmark is also the author of Syracuse. This creates an obvious risk: any AI with knowledge of Syracuse — and knowledge that it is being evaluated by its author — might soften its criticism or give it undeserved benefit of the doubt.

`analyse.py` addresses this with three measures:

**1. Provider name anonymisation.** Before any data is sent to the AI, the five provider names are randomly shuffled and replaced with letters (A, B, C, D, E). The mapping is stored locally in `decode-key-{timestamp}.json` but the AI never sees it. The AI cannot defer to "Syracuse" because it does not know which label it is.

**2. Unsparing system prompt.** The model is explicitly instructed that hedging is forbidden, that every negative claim must be backed by a specific article example, and that it must produce a strict rank order — not a "different providers suit different needs" conclusion. The instruction to describe what each lower-ranked provider would need to fix to reach first place forces the model to articulate concrete gaps rather than glossing over them.

**3. Consistent evaluation criteria.** The prompt specifies the same criteria for every provider: precision (false positive rate), coverage of obscure entities, date accuracy, summary usability (can you understand the story without clicking?), source quality, paywall accessibility, and hallucination risk.

## Interpreting the output

The analysis files use Provider A/B/C/D/E throughout. To decode:

1. Open the `decode-key-{timestamp}.json` file alongside the analysis:
   ```json
   { "label_to_provider": { "A": "Exa", "B": "Syracuse", ... } }
   ```

2. The analysis will have ranked providers 1st–5th and listed specific improvements needed for each. Cross-reference with the decode key to identify which provider is which.

3. Pay particular attention to the **"What each provider needs to fix"** section — this is where the most actionable competitive intelligence lives.

Note: the mapping is re-randomised on every run of `analyse.py`, so Provider A in one run is not necessarily the same as Provider A in another.

## What is evaluated

Queries ask each provider for news from the last 90 days. The AI judge scores
results against these criteria:

| Criterion | What counts as failure |
|---|---|
| Precision | Article is about a completely different company/industry that merely shares a name fragment (false positive) |
| Significance | Company/industry is mentioned but nothing useful is communicated — trivial name-drops in unrelated roundups |
| Coverage | No results at all for obscure or small companies |
| Date presence | Article has no publication date — the user cannot tell whether the news is current. Treated as a major failure. |
| Recency | Article is dated more than 90 days before the run date. The query window is 90 days; older results are off-scope by construction and equivalent to a wrong-topic result. |
| Summary usability | Raw scraped boilerplate (nav menus, cookie banners) instead of a distilled summary |
| Source quality | Aggregators that add no value, product pages, "About Us" content, market research landing pages. Press releases are fine. |
| Paywall | Source is subscriber-only with no usable preview |
| Hallucination | URLs that do not correspond to real published articles; invented facts in summaries |

A provider with a large share of no-date or stale (>90d) results cannot rank
1st regardless of other strengths: the data is non-actionable without a
trustworthy date.

## Results history

### 2026-05-28

No single winner across both query types — Syracuse leads companies, Exa leads industries.

- **Companies:** Syracuse 1st (8.6/10 — tight on-topic clusters like Borouge's BlueAlp/AD Ports coverage with zero no-dates), Perplexity 2nd (8.0/10 — analytical summaries on the Dominion–NextEra merger but only 98 total articles), Linkup 3rd (7.8/10 — clean Commerzbank/UniCredit cluster undermined by 11 errors and Husky Technologies returning zero results), Exa 4th (5.0/10 — precision cap engaged after the same wrong-entity articles like "Tata 1mg Achieves Profit Milestone" recycled across 25+ queries), Tavily last (2.0/10 — recency, trust, and precision caps all engaged with 4221/4221 no-date articles and Bloomberg queries returning "Apple iOS 27 Photos").
- **Industries:** Exa 1st (7.9/10 — broad dated coverage like Holmen containerboard and BP chairman removal despite Molasses Oceania drift into Westpac/Unitree), Syracuse 2nd (6.7/10 — perfect recency but thin sets like a single Marcus Theatres item for Film Distribution Midwest and BP-chairman drift into SOLVENTS Northern Europe), Perplexity 3rd (6.6/10 — clean metadata undermined by reliance on supplier "About" pages like AGT Food and Anton Paar instead of news), Linkup 4th (5.7/10 — 14 errors with Film CN returning zero and BOPET CN dominated by IndexBox/Towardspackaging forecast pages), Tavily last (3.8/10 — recency and precision caps engaged with 1876/1876 no-date and Film CN returning "China Original Pickle" IndexBox pages).

**Recommendation for autonomous use** (agent or human acting without manual filtering):

- **Companies:** **Use Syracuse** — final 8.6/10 with precision 9 and no caps engaged, delivering clean entity-targeted clusters (e.g., Borouge, Commerzbank) suitable for unfiltered agent consumption.
- **Industries:** **Use Exa + Perplexity** — neither clears the bar alone, but Exa (7.9/10, precision 6) supplies the dated breadth across topics like Construction Europe while Perplexity (6.6/10, precision 6) contributes higher-signal curated items, and neither has a trust cap.

### 2026-05-09

No single winner across both query types — Syracuse leads on companies, Exa leads on industries.

- **Companies:** Syracuse 1st (9.3/10 — clean dates and decision-ready summaries across 137 articles, e.g. Borouge Q1 "$1,175 million, down 17% YoY"), Exa 2nd (7.65/10 — full coverage but wrong-entity bleed on obscure firms like Braroll and Fritz Foss), Linkup 3rd (4.0/10 — trust cap engaged from 25 errors with HPCL Mittal Energy and Klöckner Pentaplast returning zero results), Perplexity 4th (4.0/10 — trust cap engaged from fabricated-looking Reuters/Bloomberg URLs like commerzbank-fintech-partnership-ai-procurement-2026-05-07), Tavily last (3.0/10 — recency and precision caps engaged from 1931 undated articles and scraped Bloomberg Terminal boilerplate).
- **Industries:** Exa 1st (8.2/10 — full coverage of all 25 topics with clean dates, e.g. FrieslandCampina €90M whey expansion), Perplexity 2nd (7.95/10 — zero errors and full coverage but About Us pages and "analogous to BOARD" stretches), Syracuse 3rd (4.55/10 — precision cap engaged from 18 empty topics and Bitget crypto spam in LATAM professional services), Linkup 4th (4.0/10 — trust cap engaged from 102 errors with 11 topics empty including Whey Ingredients|Northern Europe), Tavily last (2.8/10 — recency, trust, and precision caps engaged from 100% undated 2025 articles and homonym matches like "Board" as corporate governance).

**Recommendation for autonomous use** (agent or human acting without manual filtering):

- **Companies:** **Use Syracuse** (9.3/10) — clears the bar with high precision, full coverage, zero errors, and real resolvable URLs suitable for unfiltered agent consumption.
- **Industries:** **Use Exa + Perplexity** — Exa (8.2/10) contributes precision and complete topic coverage across all 25 queries, while Perplexity (7.95/10) contributes flawless date integrity and zero errors as a cross-check against Exa's recurring Nigeria CBN leakage.



### 2026-04-20

No single winner across both query types:

- **Companies:** Syracuse 1st (zero false positives across all covered companies — Borouge, Commerzbank, Husky Technologies results 100% on-target — with perfect date hygiene and concise summaries, though zero results for Braroll, Fritz Foss, Dine Cartonnages, KRC Custom Manufacturing, L M Goes Embalagens, Little Island Productions, Sigma Chemtrade, and Universal McCann), Linkup 2nd (best summary quality of all providers and good precision for covered companies like Linklaters and Klöckner Pentaplast, but 42% error rate with zero results for CBS News, HPCL Mittal Energy, and International Paper, plus entity disambiguation failures returning Dine Brands Global for Dine Cartonnages and Kilroy Realty for KRC Custom Manufacturing), Exa 3rd (excellent date hygiene with only 1 stale article across 1,170 results and strong coverage of household-name companies, but catastrophically poor precision for obscure firms — zero relevant results out of ~50 returned for each of Braroll, Fritz Foss, Dine Cartonnages, and KRC Custom Manufacturing — plus summaries consisting of scraped boilerplate like "Bloomberg - Are you a robot?" and cookie banners), Perplexity 4th (strong results for well-known companies like Linklaters and Commerzbank but likely hallucinated articles for obscure companies — Braroll results included fabricated stories about R$50M Banco do Brasil financing and IoT partnerships with "TechStart" via suspiciously well-formed valor.globo.com and industriahoje.com.br URLs, and Dine Cartonnages results included five fabricated articles about antimicrobial coatings and €50M financing with constructed foodpackagingforum.org and lesechos.fr URLs), Tavily last (best source mix for major companies drawing from Reuters, Bloomberg, and WSJ, but every single one of 1,977 articles lacked a publication date — a catastrophic infrastructure failure — combined with zero relevant results for obscure companies like Braroll, Fritz Foss, and Dine Cartonnages despite returning 88–100 articles each, padded with unusable TradingView feed entries containing only "Image 17 Image 18 Image 19").
- **Industries:** Exa 1st (highest volume of genuinely relevant dated articles across all topic combinations with zero errors — ALUMINIUM | Northern America returned tariff and Century Aluminum coverage, CONSTRUCTION | Central Asia returned Kazakhstan highway and Kyrgyzstan HPP projects — though polluted by generic IMF/OECD/Brookings Facebook filler appearing across 9+ topics, term-ambiguity false positives like BOARD | Eastern Asia returning ChiNext stock exchange reform instead of paperboard and LIQUIDS | Southern Africa returning Liquid Intelligent Technologies telecom instead of liquid packaging, and summaries consisting of raw HTML scrapes with navigation menus and language selectors), Linkup 2nd (best summary quality and strongest source selection with Reuters, Variety, Screen Daily, and Aviation Week, plus strong relevance where results existed such as NEON Korean film distribution and FrieslandCampina Borculo expansion for Whey Ingredients | Northern Europe, but an 80% error rate — 199 errors out of 249 rows — with complete failures returning zero articles for 15 of ~25 topics including ALUMINIUM | Northern America, CONSTRUCTION | Central Asia, Cheese/Milk Powders | Western Europe, and PAPER | Northern Europe), Perplexity 3rd (dated articles with clear procurement-oriented summaries across all topics, but critically low volume of 2–6 articles per topic, pervasive false positives from keyword matching without industry context — Film Distribution | Midwest returned Franchise FastLane consulting and NFP insurance broker acquisitions, HR SERVICES | Mid Atlantic returned CACI army modernization contracts — plus company homepages and directory listings like Roberts Camera, Clutch.co rankings, and Randstad office pages returned as news, and suspiciously uniform 2026-04-19 timestamps suggesting retrieval dates rather than publication dates), Syracuse 4th (clean dates and concise summaries with strong PE Resins | US coverage of LyondellBasell and Dow price hikes across 18 articles, but zero articles for 15+ topics including BOARD

### 2026-04-13

No single winner across both query types:

- **Companies:** Syracuse 1st (highest precision for covered companies with 20-article deep dives on CBS News, Commerzbank, ExxonMobil, and International Paper from quality sources like Reuters, AP, and Bloomberg, with accurate timestamps and no hallucinations, though it returned nothing for ~9 of 20 obscure companies including Braroll, Fritz Foss, and Sigma Chemtrade), Linkup 2nd (comparable precision and source quality with strong Borouge and ExxonMobil coverage but 28 errors/silent failures across obscure companies and entity confusion returning Sigma Lithium articles for Sigma Chemtrade), Perplexity 3rd (best summary quality with concise analyst-briefing-style writeups and honest "no results found" acknowledgments for Dine Cartonnages, but fabricated three Braroll articles with suspiciously neat URLs like "valor.globo.com/empresas/noticia/2026/03/15/braroll-acessorios-industriais-50-milhoes-financiamento.ghtml" and confused KRC Custom Manufacturing with Kilroy Realty Corp and Husky Technologies with the CC-330 Husky military aircraft), Exa 4th (returned 46–50 articles per company regardless of relevance, flooding Braroll with results like "Quinoa Better Living" and "Predict FIFA 2026 matches," returning Jindal Stainless articles for Jindal Films, and producing summaries full of scraped boilerplate including Facebook "Log In" prompts and cookie banners), Tavily last (1,974 total articles with zero dates on every single one, systematic inclusion of TradingView feed pages showing only "More news from Reuters Image 19 Image 20 Image 21," paywalled Bloomberg summaries returning only "Bloomberg Connecting decision makers to a dynamic network of information…," and zero relevant results across all obscure companies including 100 articles for Braroll with not one about Braroll).
- **Industries:** Exa 1st (only provider combining full 28-topic coverage, dated articles, and zero errors with meaningful relevant content across most topics, though it misinterpreted "Board" as corporate governance instead of paperboard/PCB and returned Iowa gubernatorial candidates and Wisconsin beaver articles for Film Distribution | Midwest), Tavily 2nd (highest volume and access to Reuters/Bloomberg/WSJ but every article across all topics lacked dates entirely, beauty packaging cosmetics spam from beautypackaging.com dominated Packaging | Oceania and Packaging Boxes | IN, and TradingView stubs added zero value), Linkup 3rd (cleanest and most precisely targeted results when functional, but 149 errors left 11 of 28 topics completely empty including Board | Eastern Asia, Construction | Central Asia, HR Services | Mid Atlantic, and Packaging Boxes | IN), Perplexity 4th (best precision and summary quality with analyst-briefing-style outputs like the Kazakhstan IFC infrastructure reform summary, but only 76 total articles across 28 topics with some topics getting just 1 result, and corporate "About" pages from ENGIE, Maersk, and Atos counted as articles), Syracuse last (fewest total articles at 85 with many topics receiving only 1 result, Board | Eastern Asia returning a single off-industry Seek/Zhaopin article, Distribution Services | Northern America dominated by 8 Universal Music Group takeover articles, and summaries often reduced to uninformative fragments like "Faces Energy Price Shock: European Paper Market Faces Energy Price Shock").

### 2026-03-31

Syracuse 1st in both query types:

- **Companies:** Syracuse 1st (highest reliability — precise, no hallucination, best coverage depth for well-known companies at 20 articles each), Linkup 2nd (best per-article summary quality and near-perfect precision, but only 85 articles total and 26 errors — zero results for 3 companies), Exa 3rd (dates present, real news for well-known companies, but systematic injection of identical irrelevant filler articles across 15+ company searches), Perplexity 4th (strong precision and summaries for known companies, but hallucinated entire articles for L M Goes Embalagens and Husky Technologies — fabricated Reuters/Bloomberg/FT URLs), Tavily last (zero dates on all 1,943 articles, summaries are paywall boilerplate or scraped navigation chrome, 8+ companies returned zero relevant articles). [Details](results/2026-03-31/AI-analysis/claude-companies-20260331-214203.md)
- **Industries:** Syracuse 1st (highest signal purity — virtually every article real, relevant, dated, and from authoritative sources; zero hallucination), Exa 2nd (broadest real coverage on several industrial topics but badly undermined by cross-topic pollution from the same ~10 irrelevant Nigerian/Ghanaian news articles injected across every topic, plus heavy syndication duplication), Linkup 3rd (best summary quality and high relevance precision, but 58% error rate and only 41 total articles — unreliable), Perplexity 4th (appears to deliver perfectly curated results but widespread hallucination — fake Reuters, Bloomberg, FT links with placeholder article IDs like "12345678" — making it actively dangerous), Tavily last (809 articles, zero dates, boilerplate summaries, catastrophic industry mismatching — cosmetics news for packaging boxes, cinema news for packaging film, US trucking for European road freight). [Details](results/2026-03-31/AI-analysis/claude-industries-20260331-214203.md)

### 2026-03-16

No single winner across both query types:

- **Companies:** Syracuse 1st (highest precision, no hallucinations, clean sources — but zero coverage for 7+ obscure companies), Linkup 2nd (best summaries, 21 errors causing complete failures for several companies), Perplexity 3rd (good coverage and summaries for known companies, but hallucinated articles for obscure Brazilian companies), Exa 4th (firehose of irrelevant syndicated content, scraped boilerplate summaries), Tavily last (no dates on any article, scraped navigation menus as summaries, >90% false-positive rate). [Details](results/2026-03-16/AI-analysis/claude-companies-20260316-201205.md)
- **Industries:** Exa 1st (only provider returning relevant dated content across all 12 topics, despite duplication and boilerplate), Tavily 2nd (deepest source network including ICIS/Aviation Week but zero dates on every article), Perplexity 3rd (clean results for some topics but fatally thin at 35 articles and India/Indiana confusion), Syracuse 4th (best summary quality but severe coverage gaps — zero results for Film/CN and MRO/South America, frequent industry mismatches), Linkup last (87% error rate — essentially non-functional). [Details](results/2026-03-16/AI-analysis/claude-industries-20260316-201205.md)

### 2026-03-08

Syracuse ranked 1st in both query types:

- **Companies:** Syracuse 1st (highest precision, zero hallucination), Linkup 2nd (best summaries, entity disambiguation gaps), Perplexity 3rd (hallucination risk on obscure companies), Tavily 4th (no dates on any article), Exa last (broken relevance — same irrelevant articles returned for every company).
- **Industries:** Syracuse 1st (precise, clean dates, no hallucination), Exa 2nd (covers all topics but 20% errors and syndication spam), Tavily 3rd (zero dates, topic mismatches), Perplexity 4th (ranked down from surface quality due to systematic hallucination), Linkup last (90.7% error rate — effectively non-functional). [Details](results/2026-03-08/AI-analysis/claude-companies-20260308-231709.md)

### 2026-03-02

No single winner across both query types:

- **Industries/Regions:** Syracuse favoured, Exa second.
- **Companies:** Perplexity/Linkup (ChatGPT) or Syracuse/Linkup (Claude).
- Tavily last in both. [Details](results/2026-03-02/README.md)

### 2026-02-10

Added Exa and Tavily. Syracuse remains preferred overall. [Details](results/2026-02-10/README.md)

### 2026-02-01

ChatGPT, Grok, Claude, and Gemini all prefer Syracuse. Copilot prefers Linkup. [Details](results/2026-02-01/README.md)

### 2026-01-06

Perplexity appeared to have improved but was found to be surfacing old articles with new dates — high false-positive rate. Syracuse holds up well for industry news. AI analysis results varied across models and accounts. [Details](results/2026-01-06/README.md)

### 2025-08-30

After changes to Syracuse, now a stronger contender for company-specific news. [Details](results/2025-08-30/README.md)

### 2025-05-27

None of the three original providers (Perplexity, Linkup, Syracuse) reliably handles industry/region queries. Linkup best for company news at this point. [Details](results/2025-05-27/README.md)
