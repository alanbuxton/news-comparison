# Companies Analysis — 20260308-231709

*Model: claude-opus-4-6 | Max articles per company per provider: 15*

*Provider labels were anonymised. See `decode-key-20260308-231709.json` to decode.*

---



## 1. Provider-by-Provider Assessment

### Provider A

- **Precision**: Exceptionally high. Virtually every article returned is directly and substantively about the queried company. I found zero clear false positives across 135 articles. Even for Bloomberg, where two of three results are about Beko (a different company), the articles mention Bloomberg only tangentially — but Provider A returned only 3 articles for Bloomberg, suggesting conservative retrieval. The Beko articles (#2 and #3) are false positives for a Bloomberg search. For Jindal Films, articles reference "Jindal Poly Films," which is a related entity but not identical to "Jindal Films" — borderline but reasonable. For Commerzbank, article #8 (Dutch startups fundraising) has no clear connection — a false positive.

- **Coverage**: Good for well-known companies (ExxonMobil: 20 articles, International Paper: 20, CBS News: 20, Westrock: 20). Weaker for obscure companies: HPCL Mittal Energy got only 2 articles, Linklaters only 1, Jindal Films only 2. No results at all for several companies in the user's list that other providers attempted (Braroll Acessorios Industriais, Dine Cartonnages, Entertainment Partners, KRC Custom Manufacturing, Fritz Foss, Little Island Productions, Sigma Chemtrade, Universal McCann, L M Goes Embalagens, Jiangin Yonghe Packaging Products). Provider A appears to have only returned results for a subset of companies queried.

- **Date quality**: 100% of articles have dates. Dates appear accurate and include precise timestamps with timezone information.

- **Summary usability**: Summaries are generally informative but often truncated. For example, Borouge article #4: "Abu Dhabi Polymers Co Borouge LLC (ADX: BOROUGE) presented its Q4 and full-year 2025 results on February 4, 2026, highlighting record operational performance despite challenging market conditions in t…" — the truncation is frustrating but the reader gets the gist. Good example: Husky Technologies article #7 ("Machinery sales power M&A activity in second half of 2025") gives dollar amounts and context. Bad example: Bloomberg article #3 — summary is just the PR Newswire boilerplate: "ISTANBUL, Feb. 14, 2026 /PRNewswire/ - Beko (Arçelik A.Ş. )" — tells the user nothing.

- **Source quality**: Excellent. Sources are credible industry publications (Packaging Insights, Hydrocarbon Processing, Investing.com, Reuters, Plastics News, GlobeNewswire). No "About Us" pages, no product catalogs. Press releases from PR Newswire and GlobeNewswire are legitimate.

- **Hallucination risk**: Zero evidence of hallucination. All URLs follow real publication patterns. No suspiciously uniform URL structures.

- **Overall verdict**: Provider A delivers the highest precision and cleanest results but only covers a subset of the queried companies, leaving significant gaps for obscure and small entities.

---

### Provider B

- **Precision**: Terrible. The signal-to-noise ratio is catastrophic. For nearly every company, the majority of results are completely irrelevant. Examples:
  - **Braroll Acessorios Industriais**: 49 articles, almost none about Braroll. Results include "Collagen-Rich Bone Broth Powder Market Forecast," "Branco Motores lança linha de compressores," and Portuguese-language articles about local events in Barrocas, Bahia that have zero connection.
  - **Dine Cartonnages**: 38 articles, none visibly about Dine Cartonnages. Results include "Colbert Packaging Continues Strategic Capital Investment," generic market reports on food packaging, and "Restaurant Engagement Startup Grub Lab."
  - **Sigma Chemtrade**: 39 articles — returns Sigma Healthcare, Chemtrade Logistics (a different company), and Sigma Lithium results. This is the exact "Sigma Lithium for Sigma Chemtrade" false positive called out in the evaluation criteria.
  - **KRC Custom Manufacturing**: 40 articles — not a single one about KRC Custom Manufacturing. Results include "China's Rare Earth Dominance" syndicated across dozens of outlets, "Jack and Sage Acquires Sustainable Apparel Brand," and "Go Industries Expands OEM Custom Manufacturing."
  - **Fritz Foss**: 34 articles, zero about Fritz Foss. Random press releases from fosters.com, Delaware Online, etc.
  - The same irrelevant articles appear across multiple company searches (e.g., "Winn Resources Partners with Collide" appears in Bloomberg, Borouge, CBS News, Commerzbank, Deloitte, ExxonMobil, Husky Technologies, International Paper, Jindal Films, Klöckner Pentaplast, Linklaters, Westrock, and more).

- **Coverage**: Appears high (40 articles per company) but is illusory — volume is achieved by returning irrelevant content. For well-covered companies like CBS News or ExxonMobil, there are genuine hits buried in the noise, but the user would spend significant time filtering.

- **Date quality**: All dates appear to be present (formatted as YYYY-MM-DD). However, dates lack precision (all show 00:00:00+00:00). Dates seem broadly accurate for the genuine articles.

- **Summary usability**: Summaries are often raw scraped page boilerplate. Example: Braroll article #7 ("JORNAL @ NOSSA VOZ - BARROCAS - BA: Primeira Expo Barrocas movimenta economia e valoriza produção local") — the "summary" is website navigation text. Multiple summaries contain cookie banners, navigation menus, and CSS/HTML fragments. Example: Klöckner Pentaplast article #7 — "ProcellaRX Launches Ascend: Decision Quality. Trusted Partners. One Ecosystem - The Clarion-Ledger | This page contains press release content distributed by XPR Media."

- **Source quality**: Dominated by XPR Media syndicated press releases on local newspaper sites (fosters.com, courierpress.com, cantondailyledger.com, etc.), openpr.com market reports, and FinancialContent aggregator pages. These are not journalism. Many are the same press release duplicated across 5-10 local newspaper sites. Bloomberg results include bloomberg.com articles behind paywalls with no usable content.

- **Hallucination risk**: No evidence of fabricated URLs, but the 187 errors indicate systemic retrieval failures. The same "Winn Resources Partners with Collide" article appearing for every company searched suggests a broken relevance model rather than hallucination.

- **Overall verdict**: Provider B is unusable. It returns massive volumes of completely irrelevant content, wastes the user's time, and fails fundamentally at the core task of matching articles to companies.

---

### Provider C

- **Precision**: High overall but with notable gaps. For companies it covers, results are almost always genuinely about the target company. However, there are some problems:
  - **Fritz Foss**: All 4 results are about "FRITZ!" (AVM's router brand), not a company called Fritz Foss. This is a clear entity disambiguation failure.
  - **Sigma Chemtrade**: 6 results — returns Chemtrade Logistics (different company) and Sigma Lithium (different company). The exact false positive pattern warned about in the evaluation criteria.
  - **KRC Custom Manufacturing**: 3 results — one is about Kilroy Realty Corporation (KRC), one is about SendCutSend (a different custom manufacturer), and one is KRC® cabinet handles (possibly the right company or a different KRC). Disambiguation failure.
  - **Entertainment Partners**: 0 articles returned (5 errors). Complete miss.

- **Coverage**: Moderate. Returns fewer articles per company (typically 2-10) but with high relevance. For well-covered companies: ExxonMobil (10), Linklaters (9), Jindal Films (10), Westrock (9), Borouge (7). For obscure companies: Entertainment Partners (0), Fritz Foss (4, all wrong entity), Dine Cartonnages (not present in dataset). Missing entirely: Braroll Acessorios Industriais, Dine Cartonnages, Entertainment Partners, Jiangin Yonghe Packaging Products, KRC Custom Manufacturing (wrong entity), L M Goes Embalagens, Little Island Productions. 16 errors total.

- **Date quality**: 100% of articles have dates, but all are formatted as YYYY-MM-DD 00:00:00+00:00 without precise timestamps. Dates appear accurate.

- **Summary usability**: Excellent. This is Provider C's standout feature. Every summary is a human-readable, informative paragraph that explains the story. Example: Borouge article #6 — "Borouge completed a proof of concept for AI-powered autonomous operations at its Ruwais facility with Honeywell, demonstrating potential efficiency gains of up to 20%, reduced downtime by 20%, and operational cost savings of up to 10%." The user can understand the story without clicking. Another strong example: International Paper article #5 — "International Paper announced plans to split into two independent, publicly traded companies, separating its North American operations from its Europe, Middle East, and Africa (EMEA) packaging business…"

- **Source quality**: Very strong. Reuters, Bloomberg, The Guardian, Investing.com, Packaging Dive, GlobeNewswire, Federal Register. Credible sources throughout. No scraped boilerplate or aggregator noise.

- **Hallucination risk**: Low but not zero. Some Bloomberg URLs may be paywalled. No evidence of fabricated URLs or invented facts.

- **Overall verdict**: Provider C delivers the best summaries and high precision for the companies it covers, but has significant coverage gaps for obscure companies and entity disambiguation failures for ambiguous names.

---

### Provider D

- **Precision**: Poor to moderate. For well-known companies, there are genuine results, but they are buried in massive noise. Key problems:
  - **No dates on any article**. Every single article across 1,872 results shows "[NO DATE]." This is a fundamental data quality failure.
  - Massive volumes of TradingView news feed snippets that mention the company name in a sidebar or related-articles widget but contain no substantive information about the target company. Example: For Borouge, articles like "Australia's Ampol beats profit estimates" and "Carlsberg's annual profits beat forecasts" and "China Vanke Seeks A One-Year Extension" — these have zero relevance to Borouge.
  - **Braroll Acessorios Industriais**: 87 articles — includes "Manufacturing.co Launches Acquisition Platform," "Carrefour Aims to Boost Tech," "Grammy-Nominated Singer Fatally Stabbed," and "'Everywhere You Look ... There Are Dinosaur Tracks'" from Newser. This is absurd noise.
  - **Fritz Foss**: 94 articles — includes "Grammy-Nominated Singer Fatally Stabbed," "Most People Lack Sufficient Omega-3" from Newser, "Cattle futures higher on tightening cattle supply," and "Japan demands swift release of national detained in Iran." Zero results about any company called Fritz Foss.
  - **Little Island Productions**: 83 articles — includes "Fragile geopolitics and robust supply chains spur PE defense deals," "Rio Tinto and Glencore revive $200 billion mega-merger talks," and "Bain Capital's Christina Dix: An optimist on the IPO market." Almost none about Little Island Productions.
  - **Klöckner Pentaplast** vs **Kloeckner & Co**: Multiple results about Kloeckner & Co (a steel distributor) are returned for Klöckner Pentaplast (a plastics packaging company). WSJ articles about "Kloeckner & Co Confirms Takeover Talks With Worthington Steel" have nothing to do with Klöckner Pentaplast.

- **Coverage**: Appears massive (60-100 articles per company) but is overwhelmingly noise. For companies like CBS News, there are genuine articles (Gayle King contract, Bari Weiss coverage, layoffs) mixed with irrelevant video transcripts from socialnews.xyz. For ExxonMobil, there are real results (WSJ, Forbes, Reuters) alongside TradingView sidebar scrapes.

- **Date quality**: Zero percent of articles have dates. This alone makes Provider D unfit for the stated use case. A business professional preparing for meetings needs to know when events happened.

- **Summary usability**: Varies wildly. Some summaries are raw webpage scrapes with navigation menus, image placeholders ("Image 17 Image 18 Image 19"), cookie banners, and login prompts. Example: Bloomberg article #2 — "Bloomberg Connecting decision makers to a dynamic network of information, people and ideas, Bloomberg quickly and accurately delivers business and financial information, news and insight around th…" — this is website boilerplate, not a summary. Many TradingView articles have summaries that are just lists of unrelated sidebar headlines.

- **Source quality**: Mixed. There are legitimate high-quality sources (WSJ, Reuters, CNBC, Bloomberg Law, Forbes) but they are drowned out by TradingView sidebar scrapes, Newser aggregator content, socialnews.xyz video transcripts, PressReader clippings, and local newspaper syndicated press releases.

- **Hallucination risk**: Low for fabrication, but the systematic inclusion of irrelevant TradingView sidebar content suggests the retrieval system is treating "mentioned anywhere on the page" as relevance, even when the company name appears only in an unrelated sidebar widget.

- **Overall verdict**: Provider D returns the most articles but is fundamentally broken: no dates, terrible precision, and summaries full of scraped webpage chrome. It would waste enormous amounts of the user's time.

---

### Provider E

- **Precision**: Mixed, with a peculiar pattern. For some companies, results are genuinely relevant: HPCL Mittal Energy (6 articles, all relevant), International Paper (4 articles, all relevant), Klockner Pentaplast (6 articles, all relevant), Westrock (6 articles, all relevant), Linklaters (5 articles, all relevant). But for others:
  - **Bloomberg**: All 6 results are about "supply chain risk management" generically, not about Bloomberg the company. Articles like "5 Critical Trends for Supply Chains to Stay Ready to Work in 2026" and "Top 7 Supply Chain Risk Management Software Tools for 2026" have nothing to do with Bloomberg L.P. This suggests Provider E searched for "Bloomberg" in the context of supply chain risk, not as a company name.
  - **CBS News**: Article #1 is from cbsnews.com but about the Pentagon/Anthropic, not about CBS News as a company. Article #2 is CBS News Brand Studio (sponsored content about procurement). Article #3 is about "cbs-CONSULTING," a completely different company.
  - **Deloitte**: Article #2 is a comparison article "Deloitte vs EY: 2026 Top Supply Chain Management Frameworks" which is a product-page/SEO content piece, not news. Article #4 is an event page.
  - **Commerzbank**: Article #1 is a research report PDF, not news about the company. Article #3 is another research PDF.
  - **Braroll Acessorios Industriais**: 3 articles, all with suspiciously specific Portuguese-language URLs. The first article references a "parceria estratégica com a montadora brasileira AutoForte" at "jornaleconomico.com.br" — this URL and the specificity of the content raise hallucination concerns.
  - **L M Goes Embalagens**: 3 articles, again with suspiciously specific Portuguese-language content. "valor.globo.com/empresas/noticia/2026/02/15/lm-goes-embalagens-parceria-bioplast.ghtml" and "exame.com/negocios/lm-goes-embalagens-inovacao-barreiras-inteligentes/" — these are very specific URLs for an extremely obscure company. The summaries contain oddly precise details (R$200 milhões, R$50 milhões, "reduzir custos em 15%").
  - **Klöckner Pentaplast** (with umlaut): 3 articles, one of which is a Reuters URL "https://www.reuters.com/business/kloeckner-pentaplast-secures-200m-financing-2026-02-15" — I cannot verify this URL exists, and the specificity of the financing details combined with the clean URL pattern raises concerns. Similarly, "https://www.packagingeurope.com/article/kp-berry-global-rpet-partnership/2026-01-28" follows a suspiciously neat pattern.
  - **KRC Custom Manufacturing**: 4 articles — one about KRC Aluminum Profiles (different company), one about KRC Yachting (different company), and two blog posts from krcaluprofiles.com (product marketing content, not news).
  - **Dine Cartonnages**: 2 articles, neither about Dine Cartonnages. One is about Tetra Recart, the other is a listicle.
  - **Little Island Productions**: 2 articles — one is a job posting (not news), the other is about "Sad Little Productions" (a different entity).
  - **Universal McCann**: 2 articles — one is a McCann New Zealand appointment (relevant to McCann network but not specifically Universal McCann), the other is SEO content from mediaplusdigital.com.my.
  - **Entertainment Partners**: 1 article about California film tax credits — mentions Entertainment Partners as a service provider, not substantive company news.
  - **Husky Technologies**: Only 1 article returned, despite this being a company with significant recent news (CEO change, business combination, short seller report).

- **Coverage**: Very thin. 73 total articles across all companies. Well-covered companies get 4-6 articles; many get 1-3. Entertainment Partners, Husky Technologies, and several others are barely covered. However, Provider E is the only provider that attempted to return results for Braroll Acessorios Industriais and L M Goes Embalagens with content that appears specifically about those companies — though the hallucination risk on those results is high.

- **Date quality**: 100% of articles have dates. Some are precise timestamps (e.g., "2026-02-15 09:00:00+00:00"), others are date-only. Dates appear plausible but cannot be verified for potentially hallucinated articles.

- **Summary usability**: Summaries are well-written and informative when the articles are real. Example: HPCL Mittal Energy article #1 — "HPCL Mittal Energy Limited (HMEL) announces ₹2,600 crore investment to expand Guru Gobind Singh Refinery in Bathinda with polypropylene downstream units and fine chemical projects, boosting industrial growth." Clear, actionable information. However, the suspiciously precise summaries for Braroll and L M Goes articles undermine trust.

- **Source quality**: Legitimate sources appear (Reuters, Packaging Dive, Business Standard, PR Newswire, Campaign Asia) alongside SEO content pieces, blog posts, product pages (KRC Aluminum Profiles), and job postings. The mix is inconsistent.

- **Hallucination risk**: **High for obscure companies.** The Braroll Acessorios Industriais articles cite "Jornal Econômico Brasil" (jornaleconomico.com.br), "Valor Econômico" (valor.globo.com), and "Indústria Hoje" (industriahoje.com.br) with URLs that are suspiciously well-formed and content that is suspiciously detailed for a company with virtually no digital footprint elsewhere. The L M Goes Embalagens articles follow the same pattern — citing major Brazilian publications with perfect URLs and very specific financial details. The Klöckner Pentaplast (umlaut) articles cite Reuters and Packaging Europe with URL patterns that look fabricated. These may be hallucinated articles designed to fill coverage gaps.

- **Overall verdict**: Provider E delivers a mix of genuine results for well-known companies and likely hallucinated content for obscure ones, making it fundamentally untrustworthy for the user's purpose.

---

## 2. Ranking (1st to 5th)

1. **Provider A** — Highest precision and cleanest results with zero hallucination risk, though it covers fewer companies and fewer articles per company.

2. **Provider C** — Excellent summaries and high precision for covered companies, but fails on entity disambiguation (Fritz Foss, Sigma Chemtrade, KRC) and has coverage gaps for obscure companies.

3. **Provider E** — Returns relevant results for well-known companies with good summaries, but the likely hallucination of articles for obscure companies is a serious trust problem.

4. **Provider D** — Contains genuine articles for major companies buried under massive noise, but the complete absence of dates and terrible precision make it practically unusable.

5. **Provider B** — Catastrophically poor precision, returns the same irrelevant articles across every company search, and summaries are often raw webpage scrapes.

---

## 3. What Each Provider Needs to Fix

### Provider C (2nd → 1st)
**Fixable:**
- Fix entity disambiguation: "Fritz Foss" should not return AVM FRITZ! router articles. "Sigma Chemtrade" should not return Sigma Lithium or Sigma Healthcare. "KRC Custom Manufacturing" should not return Kilroy Realty Corporation. This requires a named entity resolution layer that distinguishes companies sharing partial names.
- Expand coverage for obscure companies. Provider C returned zero results for Braroll Acessorios Industriais, Dine Cartonnages, Entertainment Partners, Jiangin Yonghe Packaging Products, L M Goes Embalagens, and Little Island Productions. Even returning 0 results honestly is better than returning wrong results, but the user expects coverage.
- Reduce the 16 errors to zero — error-free retrieval for all companies.

**Harder to fix:**
- Add more article volume per company. Provider C's 2-10 articles per company is lean for meeting preparation. Aim for 10-15 high-quality articles per company.

### Provider E (3rd → 1st)
**Fundamental problem:**
- Eliminate hallucinated articles. The Braroll, L M Goes, and Klöckner Pentaplast (umlaut variant) results appear fabricated. If the system cannot find real articles for an obscure company, it must return nothing rather than invent content. This is a trust-destroying failure. Every result from Provider E is now suspect.

**Fixable:**
- Fix the Bloomberg search to return articles about Bloomberg L.P., not generic supply chain articles that happen to mention Bloomberg data or terminals.
- Stop returning job postings (Little Island Productions), event pages (Deloitte Supply Chain Summit), product pages (KRC Aluminum Profiles), and SEO listicles (Universal McCann Malaysia) as "news."
- Increase article volume — 73 total articles is too thin.
- Fix entity disambiguation: CBS News should not return "cbs-CONSULTING" results.

### Provider D (4th → 1st)
**Fundamental problems:**
- Add dates to every article. Zero dates across 1,872 articles is a dealbreaker. This is likely a systematic extraction failure.
- Implement a relevance threshold. The current system appears to return any page where the company name appears anywhere, including in unrelated sidebars, navigation widgets, and "More news from Reuters" sections. A TradingView page about cattle futures should never be returned for a Commerzbank search.

**Fixable:**
- Strip raw webpage scraping artifacts from summaries: "Image 17 Image 18 Image 19" placeholders, navigation text, login prompts, CSS fragments.
- Deduplicate: the same TradingView and FinancialContent articles appear across multiple company searches.
- Reduce volume per company from 60-100 to 10-20 high-relevance articles.
- Fix entity disambiguation: Kloeckner & Co (steel) should not be returned for Klöckner Pentaplast (plastics packaging).

### Provider B (5th → 1st)
**Fundamental problems:**
- The relevance model is broken at its core. Returning "Jack and Sage Acquires Sustainable Apparel Brand Kastlfel" for Klöckner Pentaplast, Jindal Films, Westrock, KRC Custom Manufacturing, Little Island Productions, Fritz Foss, and L M Goes Embalagens simultaneously is not a tuning issue — the system is not performing entity-specific retrieval at all. It appears to be returning a general feed of press releases regardless of the company searched.
- Stop returning the same article for every company. "Winn Resources Partners with Collide" appeared in results for at least 15 different company searches.
- Strip boilerplate from summaries. Summaries contain "This page contains press release content distributed by XPR Media. Members of the editorial and news staff of the USA TODAY Network were not involved…" — this is not a summary.
- Eliminate the 187 errors.
- Reduce from 40 articles per company to 10-15 genuinely relevant ones.
- For obscure companies (Braroll, KRC Custom Manufacturing, Fritz Foss, Dine Cartonnages), return zero results rather than unrelated press releases.

---

## 4. Top Provider's Weaknesses

**Provider A's weaknesses:**

1. **Incomplete company coverage**: Provider A returned results for only ~13 of the queried companies. It completely missed Braroll Acessorios Industriais, Dine Cartonnages, Entertainment Partners, Fritz Foss, Jiangin Yonghe Packaging Products, KRC Custom Manufacturing, L M Goes Embalagens, Little Island Productions, Sigma Chemtrade, and Universal McCann. For a user preparing for meetings about these companies, Provider A provides nothing.

2. **Bloomberg false positives**: Two of three Bloomberg results are actually about Beko's CEO transition, not about Bloomberg L.P. The connection is apparently that the press release was distributed via PR Newswire and mentions Bloomberg-related distribution, but the articles are about Beko/Arçelik.

3. **Commerzbank false positive**: Article #8 ("These 5 Dutch startups raised money in December") has no visible connection to Commerzbank AG.

4. **Truncated summaries**: Many summaries cut off mid-sentence (e.g., "…highlighting record operational performance despite challenging market conditions in t…"). The user cannot fully understand the story without clicking through.

5. **Duplicate articles for Klöckner Pentaplast**: The same 5 articles appear under both "Klockner Pentaplast" and "Klöckner Pentaplast" — the system should normalize these queries and deduplicate.

6. **Limited article depth for some companies**: HPCL Mittal Energy (2 articles), Linklaters (1 article), Jindal Films (2 articles) are thin for meeting preparation. Other providers (C, for example) found more genuine articles for Linklaters (9) and Jindal Films (10).

7. **Source diversity**: For some companies, Provider A leans heavily on Investing.com and Recycling Today/Packaging Insights. While these are legitimate, a broader source mix would provide more perspectives.

8. **Plasticstoday article for Husky Technologies (#4)**: "Huntsman Earnings Drop Amid Polyurethanes Challenges" — the summary says "Related: Husky Technologies Announces Leadership Changes." This is a sidebar mention, not a substantive article about Husky Technologies.