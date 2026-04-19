# Industries Analysis — 20260420-025630

*Model: claude-opus-4-6 | Max articles per topic per provider: 15*

*Provider labels were anonymised. See `decode-key-20260420-025630.json` to decode.*

---

## 1. Provider-by-Provider Assessment

### Provider A

**Topic relevance**: Generally strong. Most topics return articles genuinely about the queried industry and geography. The ALUMINIUM | Northern America set includes tariff news, Century Aluminum expansion, Section 232 changes — all on-target. CONSTRUCTION | Central Asia returns Kazakhstan highway deals, Kyrgyzstan HPP construction, Turkmenistan autobahn completion. ENERGY & UTILITY | South-eastern Asia includes Vietnam LNG projects, Malaysia's TNB renewables, Thai energy summits. However, there is persistent noise from generic macro-economic filler articles that appear across multiple topics: the IMF World Economic Outlook PDF, the OECD Caribbean Development Dynamics report, the SWP Berlin geoeconomics piece, and the Facebook posts from IMF/Brookings appear as padding in BOARD | Eastern Asia, CONSTRUCTION | Central Asia, FACILITIES MANAGEMENT | New England, HR SERVICES | Mid Atlantic, PAPER | Northern Europe, and others. These are not relevant to the specific industry/geography and appear to be injected as "related" content. The BOARD | Eastern Asia topic is almost entirely about China's ChiNext stock exchange listing reform — which is "board" in the sense of a stock exchange board, not the packaging/paper board material the query likely targets. This is a systemic false-positive from term ambiguity. Film Distribution | Midwest contains articles about Iowa gubernatorial candidates, Wisconsin wildlife, and Minnesota farmers — clearly wrong-topic noise. The Film Entertainment: Film Distribution | Midwest feed is essentially identical to Film Distribution | Midwest, including the same off-topic articles (FGN apprenticeship games, PEAK26 conference, beavers vs. trout in Wisconsin). The LIQUIDS | Southern Africa topic returns articles about Liquid Intelligent Technologies (a telecom/tech company), not liquid packaging or liquid commodities — a false-positive from matching the word "Liquid" in a company name.

**Error rate**: 0 errors. Clean execution.

**Coverage breadth**: All topic combinations return substantial article counts (43–50 articles each). Full coverage.

**Date presence & recency**: no-date: 0, stale: 4. Excellent. Nearly all articles fall within the 90-day window.

**Summary usability**: Summaries are truncated HTML scrapes rather than clean editorial summaries. Many include navigation menus, cookie notices, and boilerplate (e.g., "Filipino Malay Swahili Tamil Telugu Gujarati Marathi Kannada Malayalam Punjabi Urdu" from alcircle.com). The user must click through in many cases to understand the article's substance.

**Source quality**: Draws from real industry publications (Alcircle, Canmaking News, DairyReporter, Plastics News, trans.info). Also includes Facebook posts (IMF, Brookings, SBA) which are low-value social media reposts. The CRAN packages list (cran.rstudio.com) appears twice — an R statistical software package repository, which is not news. The Purdue Libraries research guide is not news. Multiple market research report landing pages appear (IndexBox, OpenPR, Future Market Insights).

**Hallucination risk**: No obviously hallucinated URLs or fabricated content detected. The dates appear legitimate.

**Overall verdict**: Provider A delivers the highest volume of genuinely relevant, dated articles across the widest range of topics, but is significantly polluted by generic filler content (IMF/OECD/Facebook padding), term-ambiguity false positives (BOARD, LIQUIDS), and raw HTML scrapes as summaries.

---

### Provider B

**Topic relevance**: Topical relevance is frequently strong where articles are genuinely about the queried subject. ALUMINIUM | Northern America includes Century Aluminum expansion, Alcoa data center site sales, Gulf smelter disruptions — all relevant. Cheese, Cultures, Milk Powders | Western Europe covers Lactalis baby formula recalls, EU dairy outlook, DalterFood acquisition. MRO | Eastern Africa has African MRO Summit coverage, Ethiopian Airlines. However, massive off-topic pollution exists in several categories. BOARD | Eastern Asia is dominated by generic financial market roundups from TradingView/Reuters with no connection to the board materials industry (e.g., "Spanish stocks - Factors to watch on Feb 5," "Egypt's SODIC FY Consol Profit Rises," "US oil may extend loss to $60.74"). HR SERVICES | Mid Atlantic returns articles about winter storms, climate change stress, Florida housing bills, BNPL rent payments — almost entirely off-topic. Film Distribution | Midwest is overwhelmed by Hollywood industry news (Warner Bros. merger, Netflix deal, Oscars) with no specific Midwest geography relevance. Distribution Services | Northern America returns "The Manufacturer" manufacturing roundups repeatedly, most of which are about general manufacturing, not distribution/mastering/localization services.

**Error rate**: 0 errors.

**Coverage breadth**: All topic combinations return articles (44–100 per topic). Volume is highest of all providers.

**Date presence & recency**: **no-date: 2,089 out of 2,089 articles. Every single article lacks a date.** This is a catastrophic, disqualifying failure. The user cannot determine whether any article is current. The entire dataset is unusable for a time-sensitive monitoring task.

**Summary usability**: Summaries are generally better extracted than Provider A's, with more readable text snippets. But without dates, this advantage is meaningless.

**Source quality**: Sources include Bloomberg, Reuters, WSJ, Variety, Deadline, Aviation Week — premium publications. Also includes TradingView aggregator pages that are just headline lists with no substance.

**Hallucination risk**: No hallucinated content detected. The articles appear real.

**Overall verdict**: Provider B returns the largest volume of articles from high-quality sources, but is completely disqualified by having zero dates on all 2,089 articles. This is not a minor gap — it is a fundamental product failure that renders the entire output worthless for the stated use case.

---

### Provider C

**Topic relevance**: Highly variable and often poor. Many topics return 0–1 articles. The Distribution Services | Northern America results are dominated by York Water Company stock offering news (5 of 14 articles) — a water utility, not distribution/mastering/localization services. The ENERGY & UTILITY | South-eastern Asia topic returns articles about US-Russia oil waivers and Middle East oil recovery — global energy stories with only tangential Southeast Asia relevance. Film Distribution | Midwest returns exactly 1 article (Marcus Theatres president appointment) — a personnel change, not substantive industry intelligence. Fruits & Vegetables | Oceania returns 1 article — a market forecast press release. PE Resins | US is the strongest category with 18 articles covering LyondellBasell price hikes, Dow/Exxon increases, Drake Plastics expansion, and other genuinely relevant content.

**Error rate**: 0 errors.

**Coverage breadth**: Extremely poor. Of the listed topics: BOARD | Eastern Asia (0 articles shown), CONSTRUCTION | Central Asia (0 articles shown), EQUIPMENT & MACHINERY | Southern Asia (0 articles shown), FACILITIES MANAGEMENT | New England (0 articles shown), Film (BOPP Film) | CN (0 articles shown), Flexible Packaging | CN (0 articles shown), HR SERVICES | Mid Atlantic (0 articles shown), LIQUIDS | Southern Africa (0 articles shown), LOGISTICS | Western Africa (1 article — a pharmaceutical logistics market forecast, not Western Africa logistics), MRO | Eastern Africa (0 articles shown), MRO | South America (0 articles shown), PACKAGING | Oceania (0 articles shown), PAPER | Northern Europe (0 articles shown), PROFESSIONAL SERVICES | Southern Europe (0 articles shown), Packaging Boxes | IN (0 articles shown). The provider returns nothing for the majority of topics.

**Date presence & recency**: no-date: 0, stale: 0. Dates are present and within range. One article dated 2032 (Aluminium Equipment Industry market forecast) is a forward projection date, which is technically valid but confusing.

**Summary usability**: Summaries are concise single-sentence extractions, generally clear. The user can understand the gist without clicking.

**Source quality**: Mix of Investing.com earnings snapshots, GlobeNewswire press releases, EIN Presswire, Argus Media. Legitimate but narrow. Market research report landing pages (IMARC Group, Mordor Intelligence) appear.

**Hallucination risk**: None detected.

**Overall verdict**: Provider C has clean dates and concise summaries but returns trivially few articles for most topics, often zero, making it useless for comprehensive industry monitoring.

---

### Provider D

**Topic relevance**: Where results exist, relevance is generally reasonable. Film Entertainment: Distribution Services | Northern America returns NEON acquiring Korean film distribution, new US indie distributors, LAIKA/Fathom partnership — all genuinely relevant. IT & TELECOM | Northern Africa includes DR Congo digital plan, MTN-IHS acquisition, Huawei Northern Africa transformation — all on-target. Whey Ingredients | Northern Europe covers FrieslandCampina Borculo expansion, DCA benchmark pricing, Verley animal-free whey — strong relevance. However, ENERGY & UTILITY | South-eastern Asia returns articles entirely about South Asia (World Bank South Asia update, Sri Lanka energy crisis, Saudi Aramco cuts to Asia) rather than Southeast Asia — a geographic mismatch. EQUIPMENT & MACHINERY | Southern Asia returns articles about Southeast Asia construction equipment markets and China component exports to Southeast Asia — again, not Southern Asia (India/Pakistan/Bangladesh). The EXTERNAL MANUFACTURING | Northern America topic returns a single article about US chip export restrictions to China — tangentially related at best.

**Error rate**: **199 errors out of 249 total rows (50 articles + 199 errors). An 80% failure rate.** Complete topic failures (0 articles, all errors) for: ALUMINIUM | Northern America, BOARD | Eastern Asia, CONSTRUCTION | Central Asia, Cheese/Milk Powders | Western Europe, Cocoa/Nuts | US, Film (BOPP) | CN, Film Distribution | Midwest, Flexible Packaging | CN, HR SERVICES | Mid Atlantic, LIQUIDS | Southern Africa, MRO | South America, PACKAGING | Oceania, PAPER | Northern Europe, PROFESSIONAL SERVICES | Southern Europe, Packaging Boxes | IN.

**Coverage breadth**: Returns articles for only 10 of ~25 topics. 15 topics return zero articles due to errors.

**Date presence & recency**: no-date: 0, stale: 0. Dates are present and valid where articles exist.

**Summary usability**: Summaries are well-written, synthetic paragraphs that clearly explain the strategic relevance of each article. Best summary quality of all providers. For example: "South Asia's economic growth is expected to slow to 6.3% in 2026 due to global energy market disruptions."

**Source quality**: Strong mix — Reuters, Variety, Screen Daily, Aviation Week, NutraIngredients, World Bank, Argus Media. No junk sources detected.

**Hallucination risk**: None detected.

**Overall verdict**: Provider D produces the best-quality individual articles with excellent summaries and clean dates, but an 80% error rate means it fails to deliver results for most topics, making it unreliable for production use.

---

### Provider E

**Topic relevance**: Mixed. Several topics return articles that are about the right general industry but miss the specific geography or sub-sector. BOARD | Eastern Asia returns articles about Southeast Asia trade shows, Hong Kong supply chain role, and China dependency — these relate to manufacturing boards/circuit boards more broadly but are not clearly about the "board" material (paperboard, corrugated board) the query likely targets, and the geography spans far beyond Eastern Asia. FACILITIES MANAGEMENT | New England returns a Mitie press release page (UK company), an Avetta blog about subcontractor visibility, an Ivalua supplier compliance guide, and an AP errors report — none specifically about New England. Film Distribution | Midwest returns Franchise FastLane (a franchise consulting firm — not film), NFP acquiring Hamilton Group (insurance broker — not film), and Midland Paper acquiring Wetoska Packaging Distributors (paper distribution — not film distribution). These are false positives from matching the word "distribution" without industry context. Film Entertainment: Film Distribution | Midwest returns Roberts Camera (a camera retailer — not a film distributor) and Illinois film production news that is about production, not distribution. HR SERVICES | Mid Atlantic returns CACI army modernization (government contracting, not HR services), Clutch.co rankings (a directory page, not news), Brown Plus and Matern Staffing (company profile pages, not news), and Randstad staffing (a location page, not news).

**Error rate**: 0 errors.

**Coverage breadth**: All topics return articles (1–6 per topic). Low volume per topic — typically 2–5 articles.

**Date presence & recency**: no-date: 0, stale: 0. All dates present. However, many articles have suspiciously uniform dates (e.g., multiple articles dated exactly "2026-04-19 00:00:00+00:00" including a Mordor Intelligence market report, an Exporters India listicle, and an Economic Times article — suggesting the date may be the retrieval date rather than the publication date).

**Summary usability**: Summaries are clear and well-structured, written in a procurement-oriented style with specific relevance framing. They consistently note implications for "supplier risk," "procurement strategies," "regulatory changes" — suggesting these are AI-generated summaries tailored to a procurement use case.

**Source quality**: Mix of press releases (PR Newswire, Business Wire), market intelligence (Mordor Intelligence, IndexBox, Ken Research), company pages (Mitie, OMA Group, FilmNation, Roberts Camera), and news outlets (Fortune, Reuters, Atlantic Council). Several results are company "About" pages or product pages rather than news: Roberts Camera (retailer homepage), FilmNation Entertainment (company website), OMA Group (company homepage), Clutch.co (directory listing), Randstad (local office page), Matern Staffing (service page), Brown Plus (service page).

**Hallucination risk**: Dates may be artificial (retrieval dates rather than publication dates). Some "articles" appear to be static company pages repackaged as news articles, which borders on manufactured content.

**Overall verdict**: Provider E returns dated, well-summarized articles but suffers from severe false positives caused by keyword matching without industry disambiguation, returns many company pages and directories instead of news, and delivers very low volume per topic.

---

## 2. Ranking (1st to 5th)

**1st: Provider A** — Delivers the highest volume of genuinely relevant, dated articles across the widest range of topics, despite significant noise from filler content and some term-ambiguity failures.

**2nd: Provider D** — Produces the highest-quality individual results with the best summaries and strong source quality, but an 80% error rate makes it unable to deliver results for most topics.

**3rd: Provider E** — Returns dated articles with good summaries but critically low volume, pervasive false positives from poor industry disambiguation, and many company pages masquerading as news.

**4th: Provider C** — Clean dates and concise summaries but returns zero articles for the majority of topics, making it functionally useless for comprehensive monitoring.

**5th: Provider B** — Despite having the largest volume and strongest source quality (Bloomberg, Reuters, WSJ), the complete absence of dates on all 2,089 articles is a fundamental, disqualifying failure that makes every result unusable for time-sensitive intelligence.

---

## 3. What Each Provider Needs to Fix

### Provider D (2nd → 1st)
- **Fix the 80% error rate.** This is the single blocking issue. The provider must resolve whatever API/scraping/query failures cause 199 of 249 rows to return errors. If the underlying retrieval system worked, this provider would likely rank 1st given its superior summary quality and source selection.
- **Fix geographic precision.** "South-eastern Asia" queries must not return South Asia results. "Southern Asia" queries must not return Southeast Asia results. Implement geographic entity disambiguation.
- **Increase article volume per topic.** Even successful topics return only 1–9 articles. Target 15–30 to provide meaningful coverage.

### Provider E (3rd → 1st)
- **Fix industry disambiguation.** "Film Distribution | Midwest" must not return franchise consulting firms, insurance brokers, or paper distributors. "BOARD | Eastern Asia" must distinguish paperboard from circuit boards from corporate boards. "HR SERVICES" must not return military IT modernization contracts. This requires semantic filtering, not just keyword matching.
- **Stop returning company pages, directories, and service pages as news.** Roberts Camera's homepage, Clutch.co directory listings, Randstad office pages, and Mitie's press page are not articles. Implement content-type classification.
- **Increase volume to 15–30 articles per topic.** Current 2–6 articles per topic is insufficient for strategic monitoring.
- **Verify dates are publication dates, not retrieval dates.** Multiple articles sharing the exact same timestamp (2026-04-19) across different sources is suspicious.

### Provider C (4th → 1st)
- **Drastically expand coverage.** Returning 0 articles for 15+ topics is a fundamental retrieval failure. The query pipeline must be rebuilt to handle niche industry/geography combinations.
- **Eliminate market research report landing pages** (IMARC Group, Mordor Intelligence forecasts) that sell reports rather than containing news.
- **Fix false positives in Distribution Services** — York Water Company stock offerings are not distribution/mastering/localization services.
- **Increase per-topic volume from 0–6 to 15–30 articles.**

### Provider B (5th → 1st)
- **Add dates to every article.** This is not optional. Every single one of 2,089 articles lacks a date. Until this is fixed, the entire provider is worthless regardless of source quality. Extract publication dates from article metadata, HTML time tags, URL patterns, or article body text.
- **Fix topic disambiguation.** BOARD | Eastern Asia must not return Spanish stock factors, Egyptian real estate earnings, or US oil price analysis. HR SERVICES | Mid Atlantic must not return articles about winter storms, Florida housing bills, or BNPL rent payments. Film Distribution | Midwest must not return global Hollywood merger coverage that has no Midwest relevance.
- **Reduce volume of generic financial roundups.** TradingView "Market Talk" roundups that mention dozens of unrelated topics are not useful industry intelligence.

---

## 4. Top Provider's Weaknesses

Provider A has the following specific weaknesses:

1. **Generic macro-economic filler pollutes every topic.** The same IMF World Economic Outlook PDF, OECD Caribbean Development Dynamics report, and SWP Berlin geoeconomics article appear across BOARD | Eastern Asia, CONSTRUCTION | Central Asia, EXTERNAL MANUFACTURING | Northern America, FACILITIES MANAGEMENT | New England, HR SERVICES | Mid Atlantic, PAPER | Northern Europe, Packaging Boxes | IN, Road Freight | Europe, and others. These waste the user's time and inflate article counts without providing industry-specific value.

2. **Facebook posts are low-value.** IMF, Brookings, and SBA Facebook posts appear in multiple topic feeds. They are social media reposts of content available elsewhere, contain truncated text, and require logging into Facebook to read.

3. **Term-ambiguity false positives are unresolved.** "BOARD | Eastern Asia" returns China's ChiNext stock exchange board reform — not paperboard/corrugated board. "LIQUIDS | Southern Africa" returns Liquid Intelligent Technologies (a telecom company). "Film Distribution | Midwest" returns agricultural and political news from the Midwest that matches on geography but not industry.

4. **Summaries are raw HTML scrapes, not editorial summaries.** Articles routinely include navigation menus, language selectors ("Filipino Malay Swahili Tamil Telugu Gujarati Marathi Kannada"), cookie notices, and site boilerplate. The user cannot quickly assess article relevance from the summary alone.

5. **Duplicate and near-duplicate articles.** FrieslandCampina Borculo expansion appears 4 times across different regional editions of the same publication. Australia-EU tariff removal for fruit/vegetables appears 5 times from freshplaza.com regional URLs. BEML export order appears 3 times across different Indian outlets. These inflate counts without adding value.

6. **Non-news content slips through.** CRAN R package listings (cran.rstudio.com), Purdue Libraries research guides, Ed2Go course catalogs, and market research report storefronts (IndexBox, OpenPR) are not news articles.

7. **Some articles are off-geography.** The Cocoa, Nuts & Seeds | US topic includes an Irish Times article about Easter egg pricing in Ireland, and a UK nut butter brand profile from managementtoday.co.uk. Film (BOPP Film) | CN includes articles about Kenyan tea pricing, German fuel prices, Brazilian sugar exports, and Indian cement disputes — none about Chinese film.