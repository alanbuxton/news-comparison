# Companies Analysis — 20260413-230959

*Model: claude-opus-4-6 | Max articles per company per provider: 15*

*Provider labels were anonymised. See `decode-key-20260413-230959.json` to decode.*

---



## 1. Provider-by-Provider Assessment

### Provider A

**Precision**: Poor for obscure companies, mediocre for well-known ones. For well-known companies like Bloomberg, Commerzbank, ExxonMobil, and CBS News, a significant share of results are genuinely relevant. However, for obscure companies, the majority of results are completely unrelated. For "Braroll Acessorios Industriais," not a single article in the top 15 is actually about Braroll — results include "Luxury Bazaar & Courtyard.io," "Correia Brothers Moving & Storage," "Quinoa Better Living," and "STAAR Surgical." For "Fritz Foss," results include "Tim Mossing joins Federato," "BullFrog AI Shares Surge," "Netflix Raises Prices," and "Coreboot 26.03 Open-Source Firmware" — zero results about Fritz Foss. For "Husky Technologies," results include "Predict FIFA 2026 matches," "LatentView Analytics," "Claw Wallet," and "ONEOK's $2.5 Billion Construction" — none about Husky Technologies. For "KRC Custom Manufacturing," results include "Montana Knife Company," "Kilroy Realty Corp," and random rare earth mining articles — zero relevant results. For "Sigma Chemtrade," multiple results are about "Sigma Lithium," a completely different company (e.g., "Sigma Lithium Signs with a Major Brazilian Bank," "Sigma Lithium Defies Market Volatility"). For "Jindal Films," almost all results are about "Jindal Stainless" or "Jindal Steel" — different companies. For "Jiangin Yonghe Packaging Products," results include "Zhejiang Yonghe Refrigerant" (wrong company) and generic packaging market reports. For "L M Goes Embalagens," results are entirely unrelated Brazilian news and generic packaging market reports. For "Little Island Productions," results are dominated by VisionWave/defense AI articles and random financial content with no connection. For "Universal McCann," results include Omnicom Media and advertising industry articles that mention McCann tangentially but are primarily about other firms. For "Entertainment Partners," most results are about the broader entertainment industry, not the specific company Entertainment Partners (the payroll/production services company).

**Coverage**: Returns 46-50 articles per company regardless of whether any exist. This volume-at-all-costs approach means obscure companies get flooded with noise. Companies like Braroll, Fritz Foss, KRC Custom Manufacturing, Dine Cartonnages, L M Goes Embalagens, and Little Island Productions have essentially zero genuine coverage.

**Date quality**: Most articles have dates, which is good. Some entries have dates in 2026 that appear accurate. Facebook posts and some aggregator content carry dates.

**Summary usability**: Summaries are raw scraped page content — navigation menus, cookie banners, boilerplate. Example: Bloomberg article #1 is "Facebook Log In ## Quartz's Post ### **Quartz** Verified account 11h ·…" — this is unusable boilerplate from a Facebook embed. Better examples exist for well-known companies, like the Commerzbank/UniCredit articles where the headline is informative.

**Source quality**: Heavy reliance on Facebook posts (multiple per company), obscure EIN Presswire distributions, OpenPR market reports, MarketMinute syndications, and ad-hoc-news.de SEO-spam articles (e.g., repeated "Commerzbank Girokonto" product marketing pieces). The Honeywell proxy statement appears for multiple unrelated companies (Borouge, International Paper, Universal McCann), suggesting a broken relevance filter.

**Hallucination risk**: No obvious fabricated URLs, but the systematic return of completely irrelevant content for obscure companies suggests the system is filling slots with whatever it can find rather than returning nothing, which is a form of manufactured relevance.

**Overall verdict**: Provider A returns a firehose of noise for obscure companies, padding results with completely unrelated articles, Facebook posts, and scraped boilerplate, while delivering acceptable but not exceptional coverage for well-known companies.

---

### Provider B

**Precision**: Terrible for obscure companies, mixed for well-known ones. The fundamental problem is that Provider B returns results that are topically adjacent but rarely about the specific queried company. For "Braroll Acessorios Industriais" (100 articles!), not a single one is about Braroll. Results include "BRIEF-Thryv Q4 Net Income," "Flash flooding eases in Australia," "Euro zone faces inflation hurdle," "US jobless claims data," and dozens of TradingView news feed items that have zero connection to Braroll. For "Fritz Foss" (92 articles), again zero relevant results — "Deere raises full-year net income forecast," "Drop in wind power boosts spot prices," "Trump Asks Congress For $1.5 Trillion Defense Budget." For "KRC Custom Manufacturing" (85 articles), zero relevant results. For "Husky Technologies" (78 articles), zero relevant results — articles about "Sasquatch Resources," "Giant Mining," and random TradingView market updates. For "Sigma Chemtrade" (77 articles), multiple Sigma Lithium articles are returned (a different company), plus generic chemical industry articles. For "Jindal Films" (79 articles), results are overwhelmingly about Jindal Steel/Stainless, not Jindal Films. For "Dine Cartonnages" (84 articles), results include "Sweet innovations debut for Valentine's Day," "Dine Brands Global" earnings (wrong company), and generic convenience store news. For "L M Goes Embalagens" (82 articles), results are generic beauty packaging and market reports with no mention of L M Goes.

For well-known companies, results are better but still diluted: CBS News gets 100 articles and many are relevant (layoffs, Bari Weiss, radio closure, Colbert replacement). Commerzbank coverage of the UniCredit saga is genuinely strong. ExxonMobil coverage is solid. But even here, TradingView scrapes that show only image placeholders contaminate the feed.

**Coverage**: Returns the most articles (1,974 total, 78-100 per company), but volume is inversely correlated with quality. Obscure companies get the most articles and the worst precision.

**Date quality**: All dates are missing — every single article shows "[NO DATE]." This is a critical failure for a business user who needs to know recency.

**Summary usability**: Many summaries are truncated paywall messages or navigation boilerplate. Bloomberg articles frequently show: "Bloomberg Connecting decision makers to a dynamic network of information, people and ideas, Bloomberg quickly and accurately delivers business and financial information..." — this is the standard paywall gate, not a summary. TradingView articles show "More news from Reuters Image 19 Image 20 Image 21" — completely useless. WSJ articles are paywalled with no usable content.

**Source quality**: Extremely heavy reliance on TradingView market feed pages that contain no substantive content — just lists of image placeholders and other article titles. These are aggregator index pages, not articles. Also heavy on paywalled WSJ and Bloomberg articles where no content is extractable.

**Hallucination risk**: No fabricated URLs visible, but the systematic inclusion of TradingView feed pages as "articles" about specific companies is effectively hallucinated relevance — these pages happen to list the company name somewhere in a sidebar or adjacent headline.

**Overall verdict**: Provider B maximizes volume at catastrophic cost to precision, returns no dates on any article, and fills results with TradingView feed pages and paywalled content that provides zero usable information, making it the worst provider for the stated use case.

---

### Provider C

**Precision**: Generally high for companies where it returns results. Borouge articles are all genuinely about Borouge (FY 2025 results, ADNOC expansion, Austria cooperation, M&A). Commerzbank articles are all relevant (UniCredit FAQ, growth targets, AI strategy). ExxonMobil results are on-target (proxy filing, Texas move, Venezuela, earnings). Klöckner Pentaplast results are all genuine company news. Linklaters results are all relevant (FCA priorities, CIP financing, Munich Security Conference, ESG newsletter). Westrock results are genuine (medium-term update, Q4 results, SWOT analysis, honeycomb mailers). However, there are notable failures: For "Braroll Acessorios Industriais," the 3 articles returned appear to be hallucinated — URLs like "valor.globo.com/empresas/noticia/2026/03/15/braroll-acessorios-industriais-50-milhoes-financiamento.ghtml" and "industriahoje.com.br/parcerias/braroll-technova-sensores-iot" follow suspiciously neat patterns and describe events (R$50 million financing, TechNova IoT partnership, ANP regulations) that cannot be verified. The summaries read like AI-generated corporate news rather than actual journalism. For "Fritz Foss," the 3 articles are completely unrelated (City of Tacoma contracts, government relations list, Des Moines "Best of" magazine). For "CBS News," 2 of 3 results are completely off-topic (pharmaceutical supply chains, ViClarity credit union software). For "Sigma Chemtrade," 1 of 2 results is Interactive Brokers' shortable stocks page and the other is Alberta Securities Commission's issuer list — neither contains substantive information about the company. For "Universal McCann," all 4 results are about banking/fintech/geopolitical risk with no connection to the advertising agency. For "KRC Custom Manufacturing," the sole result is about Kilroy Realty Corporation (KRC) — a REIT, not a custom manufacturer. For "Dine Cartonnages," the sole result acknowledges "No recent news articles found" which is honest but not useful. For "Husky Technologies," one result is about the Canadian military CC-330 Husky aircraft fleet and the other is about mining company Itafos and its "Husky 1" mine — neither is about the injection molding equipment company.

**Coverage**: Returns far fewer articles (56 total, 1-4 per company), but this restraint is mostly a virtue — except when it returns zero useful results for a company and fills the slot with tangentially related or hallucinated content.

**Date quality**: All articles have dates. Dates appear accurate and properly formatted.

**Summary usability**: Best of all providers. Summaries are concise, informative, and clearly written. Example: Borouge article — "Borouge reported FY 2025 revenue of USD 5.9 billion, down 3% year-over-year due to softer polyolefin prices, despite record sales volumes. Adjusted EBITDA was USD 2.2 billion with a 37% margin." This is immediately useful. Even the "no results found" acknowledgment for Dine Cartonnages is more honest than flooding with noise.

**Source quality**: Draws from legitimate sources — company websites, major news outlets (Reuters, The National, Economic Times), regulatory filings, and industry publications. No Facebook posts, no TradingView scrapes, no EIN Presswire spam.

**Hallucination risk**: The Braroll articles are the most suspicious content across all providers. Three articles about an obscure Brazilian industrial accessories company, each describing specific financial events (R$50M loan, IoT partnership, ANP regulations), with URLs that look plausible but may not resolve to real published content. This is a serious red flag. The summaries read as if generated by an AI to fill a gap in coverage.

**Overall verdict**: Provider C delivers the best summaries and highest precision for companies it genuinely covers, but returns hallucinated content for obscure companies (Braroll) and fails badly on entity disambiguation for others (KRC, Husky Technologies, CBS News).

---

### Provider D

**Precision**: High for companies where it returns results. Borouge coverage is excellent — 10 articles all genuinely about Borouge (plant fires, dividend approval, Borouge International formation, NOVA Chemicals acquisition, leadership appointments). Commerzbank coverage is thorough and relevant — 9 articles covering UniCredit's bid, Commerzbank's rejection, German government opposition, buyback program. ExxonMobil gets 17 genuinely relevant articles covering Q1 impact from Middle East conflict, Texas refinery maintenance, Nigeria investment, Golden Pass LNG, Venezuela, Guyana, Supreme Court climate case. HPCL Mittal Energy gets 5 directly relevant articles. Husky Technologies gets 3 directly relevant articles (CEO appointment, CFO departure, service president appointment). Klöckner Pentaplast gets 5 directly relevant articles including restructuring completion and product launches. Linklaters gets 7 relevant articles. Westrock gets 8 relevant articles covering both Smurfit Westrock and Westrock Coffee. Jindal Films gets 9 articles, though these are about "Jindal Poly Films" specifically — which is the correct company match. Sigma Chemtrade gets 7 articles, but most are about Sigma Lithium (wrong company) or Chemtrade Logistics Income Fund (wrong company) — only the general chemical industry article has potential relevance.

**Coverage**: Returns 0 articles with errors for CBS News, KRC Custom Manufacturing, Universal McCann, and Klöckner Pentaplast (with umlaut). Also returns 0 for L M Goes Embalagens, Braroll, Fritz Foss, Dine Cartonnages, Little Island Productions, and Jiangin Yonghe Packaging Products (these aren't listed, implying 28 errors across these companies). The 28 errors indicate the system fails silently for companies it cannot find.

**Date quality**: All articles have dates. Dates appear accurate.

**Summary usability**: Good. Summaries are substantive and professionally written. Example: Borouge article — "Borouge and Borealis combined to create Borouge International and acquired NOVA Chemicals, with OMV and XRG each holding 50%. The company is headquartered in Austria with regional HQ in UAE and operates over 50 production sites globally." Clear, informative, actionable.

**Source quality**: Strong. Bloomberg, Reuters, Financial Times, The National, Business Standard, GlobeNewswire, PR Newswire, industry publications (Packaging Europe, Interplas Insights). No Facebook posts, no TradingView junk.

**Hallucination risk**: Low for returned articles. The Sigma Chemtrade results about Sigma Lithium and Chemtrade Logistics are false positives from entity confusion, not hallucination.

**Overall verdict**: Provider D delivers high-precision, well-sourced results for companies it can find, but fails completely (with errors) for obscure companies and has entity disambiguation problems for Sigma Chemtrade.

---

### Provider E

**Precision**: High for well-known companies, moderate overall. Bloomberg gets 4 articles — 2 are genuinely about Bloomberg (BCOM indices launch, BFIX integration), 1 is about a BNN Bloomberg anchor retiring (relevant), and 1 is about Chrome Horse Society Tequila partnering with the Longines Global Champions Tour (irrelevant). Borouge gets 8 articles, all genuinely relevant (Borouge International formation, leadership, recycling partnerships, Q4 results). CBS News gets 20 articles, overwhelmingly relevant and high-quality — comprehensive coverage of layoffs, radio closure, Bari Weiss overhaul, streaming walkout, and programming changes. Commerzbank gets 20 articles, all relevant and covering the UniCredit saga from multiple angles. ExxonMobil gets 20 articles, all relevant with strong diversity (Nigeria, Guyana, Texas, Alaska, Brazil, immersion cooling with Infosys, recycling plants, Fife closure). HPCL Mittal Energy gets 6 relevant articles. Husky Technologies gets 10 articles, all directly about the company (CEO appointment, CFO departure, service president, India expansion, short selling report, M&A history). International Paper gets 20 articles covering the company split, plant closures, new Mississippi facility, and Georgetown mill sale — all relevant. Westrock gets 20 articles with strong coverage of Smurfit Westrock's operations, Q4 results, Ecuador acquisition, Wakefield strike, Florence mill upgrade, and board changes.

For obscure companies: Jindal Films gets only 2 articles (Q3FY26 results and compliance officer appointment for "Jindal Poly Films") — relevant if "Jindal Poly Films" is the intended match. Klöckner Pentaplast gets 4 genuinely relevant articles (Chapter 11 emergence, product launch). Linklaters gets only 1 article (office expansion) — thin coverage. Entertainment Partners gets 3 articles about "Brillstein Entertainment Partners" — which is a different company from "Entertainment Partners" (the payroll/production services firm).

No results visible for: Braroll, Dine Cartonnages, Fritz Foss, Jiangin Yonghe Packaging Products, KRC Custom Manufacturing, L M Goes Embalagens, Little Island Productions, Sigma Chemtrade, Universal McCann.

**Coverage**: 152 total articles. Appears to return 0 results for 9 of 20 companies rather than padding with noise. This is a significant coverage gap but avoids the precision catastrophe of Providers A and B.

**Date quality**: All articles have dates. Timestamps are precise (often to the second). Dates appear accurate.

**Summary usability**: Good but brief. Many summaries are single-sentence extractions rather than comprehensive summaries. Example: "Adnoc's XRG and OMV complete deal to create chemicals giant Borouge International." Useful but could include more detail. Better example: ExxonMobil article — "ExxonMobil has confirmed plans to make a final investment decision (FID) on its $8 billion Owowo gas project in Nigeria by 2025, marking a major step in the country's energy sector." Clear and actionable.

**Source quality**: Strong. Reuters, AP, Bloomberg, Business Wire, GlobeNewswire, Variety, Deadline, Packaging Europe, Plastics News, Resource Recycling, industry trade publications. Very few aggregators. No Facebook posts, no TradingView junk.

**Hallucination risk**: Low. URLs appear legitimate. No suspiciously neat URL patterns.

**Overall verdict**: Provider E delivers high-precision, well-dated results from quality sources for companies it covers, with the strongest single-company coverage depth (20 articles for major companies), but returns nothing for roughly half the obscure companies in the test set.

---

## 2. Ranking (1st to 5th)

**1st: Provider E** — Highest precision for companies it covers, with 20-article deep dives on major companies using quality sources, accurate dates, and no hallucinated content, though it returns nothing for ~9 of 20 companies.

**2nd: Provider D** — Comparable precision and source quality to Provider E for companies it covers, but returns fewer articles per company and has 28 errors (complete failures) across obscure companies, plus entity disambiguation problems with Sigma Chemtrade.

**3rd: Provider C** — Excellent summaries and honest restraint in article count, but hallucinated Braroll articles, entity disambiguation failures (KRC, Husky Technologies, CBS News), and returning only 1-4 articles per company limits its usefulness for deep meeting prep.

**4th: Provider A** — Returns relevant results for well-known companies but floods obscure companies with completely unrelated noise, includes raw scraped boilerplate as summaries, and relies heavily on Facebook posts and press release spam.

**5th: Provider B** — Returns the most articles but the worst precision, with zero dates on any article, systematic inclusion of TradingView feed pages as "results," and paywalled content with no extractable information, making it functionally useless for the stated use case.

---

## 3. What Each Provider Needs to Fix

### Provider D (2nd → 1st)
- **Fix errors for missing companies**: The 28 errors across CBS News, KRC Custom Manufacturing, Universal McCann, Klöckner Pentaplast (umlaut version), and all obscure companies need resolution — return an honest "no results" instead of an error, or expand source coverage.
- **Fix entity disambiguation for Sigma Chemtrade**: Stop returning Sigma Lithium and Chemtrade Logistics articles for a search on "Sigma Chemtrade."
- **Increase article depth for covered companies**: 4-10 articles per company is thin compared to Provider E's 20. Add more sources to increase coverage depth for major companies.
- **Cover more obscure companies**: Partner with regional/industry sources to find news about companies like HPCL Mittal Energy (which it does cover) but also Braroll, Dine Cartonnages, etc.

### Provider C (3rd → 1st)
- **Eliminate hallucinated articles**: The Braroll articles must be verified or removed. If the system cannot find real news about a company, it must say so (as it did for Dine Cartonnages) rather than generate plausible-sounding fake articles.
- **Fix entity disambiguation**: KRC Custom Manufacturing ≠ Kilroy Realty Corp. Husky Technologies ≠ CC-330 Husky military aircraft. CBS News results should be about CBS News, not pharmaceutical supply chains.
- **Increase coverage depth**: 1-4 articles per company is insufficient for meeting prep. A user needs 5-15 substantive articles to understand a company's recent trajectory.
- **Expand source base**: Add more industry trade publications, regional business news, and wire services to find coverage of obscure companies.

### Provider A (4th → 1st)
- **Implement a relevance threshold**: Stop returning articles that have zero connection to the queried company. For Braroll, Fritz Foss, KRC Custom Manufacturing, Husky Technologies, and others, every article is irrelevant. It is better to return 0 results than 50 false positives.
- **Fix entity disambiguation**: "Jindal Films" ≠ "Jindal Stainless" ≠ "Jindal Steel." "Sigma Chemtrade" ≠ "Sigma Lithium." "Westrock" results should not conflate "Smurfit Westrock" with "Westrock Coffee" without distinction.
- **Stop using Facebook posts as news sources**: Facebook embeds provide no usable summary and are not news articles.
- **Clean up summaries**: Replace raw scraped boilerplate (navigation menus, "Facebook Log In," cookie banners) with actual article content extraction.
- **Remove duplicate/boilerplate results**: The Honeywell proxy statement appearing for multiple unrelated companies indicates a broken relevance algorithm.
- **Fundamental problem**: The system appears to fill a fixed article quota regardless of whether relevant content exists, which is architecturally wrong.

### Provider B (5th → 1st)
- **Add date extraction**: Zero dates across 1,974 articles is a fundamental failure. This must be fixed before anything else.
- **Implement a relevance threshold and stop returning TradingView feed pages**: The vast majority of articles for obscure companies are TradingView market feed index pages that contain no information about the queried company. These must be filtered out entirely.
- **Stop returning paywalled content with no extractable information**: Bloomberg.com, WSJ, and other paywalled sources that return only "Bloomberg Connecting decision makers to a dynamic network..." are useless.
- **Reduce volume, increase precision**: Returning 100 articles for Braroll when zero are relevant is worse than returning 0. Implement minimum relevance scoring.
- **Extract actual summaries**: Replace "More news from Reuters Image 19 Image 20 Image 21" with actual article content.
- **Fundamental problems**: The combination of no dates, no relevance filtering, and no usable summaries means this system is architecturally unsuited for the use case. Every major component (date extraction, relevance scoring, content extraction) needs to be rebuilt.

---

## 4. Top Provider's Weaknesses (Provider E)

1. **Returns nothing for ~9 of 20 companies**: Braroll, Dine Cartonnages, Fritz Foss, Jiangin Yonghe Packaging Products, KRC Custom Manufacturing, L M Goes Embalagens, Little Island Productions, Sigma Chemtrade, and Universal McCann appear to have zero results. A business professional preparing for a meeting with one of these companies gets nothing.

2. **Entity disambiguation failures**: "Entertainment Partners" results are about "Brillstein Entertainment Partners," a talent management company, not "Entertainment Partners," the entertainment industry payroll and production services company. This is a false match.

3. **Thin coverage for some companies**: Linklaters gets only 1 article (an office lease expansion). Jindal Films gets only 2 articles. A user preparing for a Linklaters meeting needs to know about partner promotions, major deals, and strategic direction — not just a real estate transaction.

4. **Summaries are often too brief**: Many summaries are single-sentence extractions that tell you what happened but not enough context. For meeting prep, a 2-3 sentence summary with key numbers and names is more useful.

5. **Some irrelevant results slip through**: The Chrome Horse Society Tequila article in Bloomberg results has no connection to Bloomberg L.P.

6. **No coverage of non-English language sources for non-English companies**: Companies like Braroll (Brazilian), Dine Cartonnages (French), L M Goes Embalagens (Portuguese/Brazilian), and Jiangin Yonghe (Chinese) may have coverage in their local languages that Provider E cannot access.

7. **Westrock entity conflation**: Results mix "Smurfit Westrock" (packaging) coverage without clearly distinguishing it from the original WestRock or "Westrock Coffee." While most articles are about Smurfit Westrock, a user searching for "Westrock" as a standalone entity may be confused.