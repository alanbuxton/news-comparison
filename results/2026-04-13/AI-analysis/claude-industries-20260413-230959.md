# Industries Analysis — 20260413-230959

*Model: claude-opus-4-6 | Max articles per topic per provider: 15*

*Provider labels were anonymised. See `decode-key-20260413-230959.json` to decode.*

---

# Provider-by-Provider Assessment

## Provider A

**Topic relevance**: Mixed. Many results are genuinely on-topic and strategically valuable, but there is significant noise. The "BOARD | Eastern Asia" topic is a disaster — it has been interpreted as corporate boards/governance rather than physical board materials (paperboard, PCB, etc.). Articles like "SEBI Initiates Large-Scale Capacity Building for Independent Directors" (article #2), "Rupee opens 125 paise higher as RBI clamps down on speculative bets" (articles #11-12), and "HKMA Delays Stablecoin Licenses" (#8) have nothing to do with board manufacturing. A few PCB-related articles sneak in (#1 about Shudiangufen's PCB expansion in China is correct), but the majority are wrong-industry. Similarly, "Film Distribution | Midwest" is polluted with completely irrelevant results: "Iowa GOP gubernatorial candidate qualifies for primary ballot by one signature" (#11), "Wisconsin wildlife advocates weighing how beavers, trout can coexist" (#12). "Film (BOPP Film, BOPET, PE Film etc) | CN" includes "Kenyan tea set for high prices in France-linked market push" (#3), "Brazil to cut sugar exports" (#9), and "Germany news: Bundestag approves fuel station price brake" (#10) — none about packaging film in China. The "Construction | Central Asia" topic includes articles about Bulgaria energy trends (#4), EU oil contingency (#5), India SEZ duty (#6), and Pakistan LNG (#8) — wrong geography entirely. "Liquids | Southern Africa" includes a cricket article about CSA charging Swanepoel (#7) and multiple duplicate Eversheds-Sutherland regulatory updates from different regional URLs (#10-15).

**Error rate**: Zero errors. Clean execution.

**Coverage breadth**: All 28 topic combinations return results with substantial article counts (44-50 per topic).

**Date quality**: All articles have dates. Dates appear accurate and recent (March-April 2026).

**Summary usability**: Summaries are often raw boilerplate scraped from the page — navigation elements, site menus, and cookie notices are frequently included. For example, the FADA CE Sales Report (#2 in Equipment & Machinery) starts with "Infra Equipment's ki Dunia ki har news, Sirf Infra Junction Whatsapp Par." The Facilities Management results include summaries like "High-Profile Monthly Newton, MA – Chapman Construction/Design announced..." mixing site chrome with content. Usable but messy.

**Source quality**: Mix of legitimate news, press releases, and some low-value sources. Facebook posts appear regularly as top results (e.g., SBAgov, WorldBankGroup, PierrePoilievreMP, McKinsey posts). An R CRAN packages list appears as result #1 for "Film Entertainment: Distribution Services" — this is a software repository listing, not news. "Business & Entrepreneurship - Purdue Libraries Research Guides" appears twice as #1 for Film Distribution topics. "Flagship Advisory Partners" homepage (#6 in Board | Eastern Asia) is not news. Market research report landing pages appear (e.g., "Logistics Market Size, Share & Global Trends Report 2035" from marketresearchfuture.com).

**Hallucination risk**: No evidence of hallucinated articles. URLs appear genuine.

**Overall verdict**: Provider A delivers high volume with dates and decent industry sources, but suffers from severe misinterpretation of ambiguous industry terms ("Board" as governance, "Film" confused between cinema and packaging) and heavy geographic drift, plus noisy summaries stuffed with boilerplate.

---

## Provider B

**Topic relevance**: Similar ambiguity problems as Provider A but arguably worse on certain topics. "BOARD | Eastern Asia" is completely off-target — results are dominated by generic financial market roundups: "Asia shares becalmed by holidays, dire Japan data" (#3), "US oil may extend loss to $60.74" (#10), "Egypt's SODIC FY Consol Profit Rises" (#11), "Take Five: Our currency, your problem" (#12). Not a single result in the visible 15 is about physical board materials. "PACKAGING | Oceania" is dominated by Beauty Packaging articles about cosmetics brands (Debut skincare #1, Clinique #2, Balmain Beauty #3, CosRx Peptide Eye Patches #4) with no connection to Oceania or industrial packaging. "Packaging Boxes | IN" is similarly filled with Beauty Packaging articles irrelevant to India — "Matrix Expands Its 2026 Brand Ambassador Roster," "Private Equity Firm Finances Pat McGrath Labs." "FACILITIES MANAGEMENT | New England" includes press releases about a longevity startup (#1), a heavy machinery IT system (#2), a furnace repair initiative in Oshawa, Ontario (#3), a resilient garden (#4), a glycobiology lab (#5) — none about facilities management in New England. "HR SERVICES | Mid Atlantic" includes many generic HR industry articles from HR Dive that are national/general, not Mid-Atlantic specific. The "Film Distribution | Midwest" topic returns national/global film industry articles (Netflix/Warner Bros merger, Berlin Film Festival, etc.) with no Midwest specificity.

**Error rate**: Zero errors.

**Coverage breadth**: All 28 topics receive results with generous article counts (42-92 per topic). Volume is the highest of all providers.

**Date quality**: This is Provider B's most glaring flaw — **zero articles have dates**. Every single article shows "[NO DATE]." This is a fundamental failure for a news search tool where recency matters enormously.

**Summary usability**: Summaries are generally more informative than Provider A's — they tend to contain actual article excerpts rather than site chrome. However, many are truncated with "[...]" and some contain navigation boilerplate. TradingView results frequently show only "More news from Reuters Image 17 Image 18 Image 19..." which is useless.

**Source quality**: Mix of high-quality sources (Reuters, Bloomberg, WSJ, Variety, Deadline) and significant noise. Many WSJ and Bloomberg articles are paywalled. TradingView results are essentially news aggregator stubs that add no value — they show almost no content. Multiple "North America Manufacturing News Digest – The Manufacturer" results appear as separate articles but are really weekly roundups. Beauty Packaging articles dominate packaging topics regardless of geography or sub-industry. IndexBox market research landing pages appear repeatedly. OpenPR press releases are market research report promotions, not news.

**Hallucination risk**: No hallucinated articles detected.

**Overall verdict**: Provider B offers the highest volume and accesses premium sources like Reuters and Bloomberg, but the complete absence of dates is disqualifying for a time-sensitive news monitoring tool, and precision is poor — many topics are drowned in irrelevant results from keyword-matching without industry or geography filtering.

---

## Provider C

**Topic relevance**: Strikingly high precision. Nearly every article is genuinely relevant to both the industry and geography queried. "ALUMINIUM | Northern America" returns Rio Tinto's CBA acquisition (#3), Section 232 tariff overhaul (#1), and Sutter Metals acquisition (#2) — all directly relevant. "CONSTRUCTION | Central Asia" returns Selena Group's Kazakhstan plant (#4), IFC-backed Kazakhstan reform (#2), and ZoomInfo's Uzbekistan construction firms list (#1). "Packaging Boxes | IN" returns India's 40% recycled packaging mandate, India packaging industry $92B projection, and rigid box manufacturers in India — all precisely on-target. However, some results are not news: ZoomInfo company lists (#1 in Construction | Central Asia), Lenovo supplier list (#2 in Board | Eastern Asia), and MM Group's corporate "About" page (#1 in Paper | Northern Europe). The "FACILITIES MANAGEMENT | New England" topic returns only 2 articles, neither of which is about facilities management in New England — they're about AP errors and supply chain risk surveys.

**Error rate**: Zero errors.

**Coverage breadth**: Coverage is thin. Many topics have only 1-5 articles. "EQUIPMENT & MACHINERY | Southern Asia" has just 1 article. "HR SERVICES | Mid Atlantic" has 1 article. "LIQUIDS | Southern Africa" has 1 article. Several topics have 2-3 articles. This is insufficient for strategic monitoring.

**Date quality**: All articles have dates. Some dates appear to be "retrieved" dates rather than publication dates (e.g., multiple articles dated 2026-04-13, which appears to be the scrape date for corporate pages like ENGIE, Maersk, FilmNation, OMA Group, and MM Group).

**Summary usability**: Summaries are the best of all providers — clearly written, informative, and focused on strategic content. They read like analyst briefings rather than scraped text. Example from "CONSTRUCTION | Central Asia" #2: "Kazakhstan advances reforms to attract private investment in infrastructure via IFC support, including financing, risk insurance, and guarantees to reduce premiums and crowd in capital for large projects."

**Source quality**: Mixed. Legitimate news and press releases alongside corporate "About" pages (ENGIE, Maersk, FilmNation, OMA Group, MM Group, Atos), market research report pages (Mordor Intelligence, Ken Research), and company directory listings (ZoomInfo, F6S). The Mordor Intelligence and similar pages are report landing pages selling research, not containing news.

**Hallucination risk**: Low, but some "articles" may be AI-generated summaries rather than actual article excerpts, given their unusually clean and structured format. The summary for "Maersk Acquires Performance Team" describes a strategic acquisition in detail, but the URL points to a general warehousing page, not a news article.

**Overall verdict**: Provider C has the best precision and summary quality by far, but delivers so few results per topic that it fails the basic coverage requirement for strategic monitoring — a user monitoring "Equipment & Machinery in Southern Asia" gets one article about SME finance in Pakistan, which isn't even about equipment.

---

## Provider D

**Topic relevance**: When it returns results, precision is generally good. "ALUMINIUM | Northern America" delivers 10 highly relevant articles: Century Aluminum's JV with EGA (#5), aluminum price trends (#6), Gulf supply disruptions (#7-9), and US demand signals (#10). "ENERGY & UTILITY | South-eastern Asia" is strong with 10 relevant articles covering Southeast Asian energy transition, nuclear plans, and LNG supply disruptions. However, geography drift occurs: article #1 in Energy ("South Asia growth to slow") and #5 ("South Korea's renewable energy pivot") are about South Asia and East Asia, not Southeast Asia. "Film Entertainment: Distribution Services | Northern America" returns 9 well-targeted articles about film distribution trends, new distribution companies, and AI impacts on the industry. "EQUIPMENT & MACHINERY | Southern Asia" returns 2 articles, both about Southeast Asia, not Southern Asia (India/Pakistan/Bangladesh/Sri Lanka).

**Error rate**: 149 errors across the dataset — the worst of any provider. Multiple entire topics returned zero results due to errors: "BOARD | Eastern Asia" (8 errors, 0 articles), "CONSTRUCTION | Central Asia" (5 errors, 0 articles), "EXTERNAL MANUFACTURING / TOLLING | Northern America" (8 errors, 0 articles), "Film Distribution | Midwest" (5 errors, 0 articles), "Flexible Packaging: Film | CN" (10 errors, 0 articles), "HR SERVICES | Mid Atlantic" (10 errors, 0 articles), "LIQUIDS | Southern Africa" (8 errors, 0 articles), "MRO | South America" (4 errors, 0 articles), "PROFESSIONAL SERVICES | Southern Europe" (9 errors, 0 articles), "Packaging Boxes | IN" (17 errors, 0 articles), "RESINS | Western Europe" (10 errors, 0 articles). This means 11 of 28 topics are completely empty.

**Coverage breadth**: Only 17 of 28 topics return any results at all. Of those, many have only 1-6 articles.

**Date quality**: All returned articles have dates. Two articles in "Film | CN" have future dates (2026-06-10 and 2026-05-26) from Fujian Taian — these are likely event previews, which is fine but unusual.

**Summary usability**: Summaries are clean and informative, written in a professional style. Example: "Century Aluminum formed a joint venture with Emirates Global Aluminium to build a 750,000-tonne smelter in Oklahoma using energy-efficient technology."

**Source quality**: Good sources when available — Reuters, Bloomberg, CNBC, S&P Global, Aviation Week, industry-specific outlets. Some market research report pages (Mordor Intelligence in Energy & SEAA, GlobeNewswire market research reports).

**Hallucination risk**: No hallucinated articles detected.

**Overall verdict**: Provider D delivers high-quality, well-summarized results when it works, but catastrophic error rates leave 11 of 28 topics completely empty — this is an unreliable service that cannot be depended on for comprehensive monitoring.

---

## Provider E

**Topic relevance**: Generally good precision within narrow scope. "ALUMINIUM | Northern America" returns 8 directly relevant articles about Ford tariff relief, aluminum premium increases, Century Aluminum stock performance, and Kibar/Assan Alüminyum's US acquisition. "PE Resins | US" is Provider E's best topic with 18 articles covering LyondellBasell price hikes, Iran war impacts on PE/PP prices, Drake Plastics headquarters, plastics M&A activity — all directly relevant. "Distribution Services | Northern America" is dominated by Universal Music Group takeover news (Pershing Square's $64B bid) — 8 of 13 articles are about this single deal. While technically about distribution (music distribution), this is arguably a different industry than what the query intends (physical distribution/logistics/content localization). "Film Entertainment: Distribution Services | Northern America" returns mostly Jeff Shell/Paramount news (5 of 8 articles), which is relevant but extremely narrow.

**Error rate**: Zero errors.

**Coverage breadth**: Very thin. Many topics have only 1-2 articles: "BOARD | Eastern Asia" (1 article about Seek/Zhaopin — wrong industry), "FACILITIES MANAGEMENT | New England" (1 article), "Film Distribution | Midwest" (1 article), "Film Entertainment: Film Distribution | Midwest" (1 article), "LOGISTICS | Western Africa" (1 article), "PACKAGING | Oceania" (1 article). Total across all topics is only 85 articles. Multiple topics are essentially uncovered.

**Date quality**: All articles have dates, and they appear accurate.

**Summary usability**: Summaries are very short — often just a sentence fragment preceded by a keyword tag. Example: "acquired: Nickolas Asset Management has acquired Associated Plastics Corp." This is useful for quick scanning but lacks context. Some are truncated to the point of being uninformative: "Faces Energy Price Shock: European Paper Market Faces Energy Price Shock."

**Source quality**: Mix of mainstream business news (Reuters, Bloomberg, Argus Media, Investing.com) and industry sources (Plastics News, Plastics Today, Paper Advance). Some low-value sources: LatestLY for a Pakka Ltd appointment, openPR market research reports, and EIN Presswire market forecast press releases.

**Hallucination risk**: No hallucinated articles detected.

**Overall verdict**: Provider E delivers clean, date-stamped results with no errors, but volume is far too low for comprehensive monitoring and many topics are essentially empty — it appears to be a general business news search that occasionally hits industry-relevant results rather than a purpose-built industry monitoring tool.

---

## 2. Ranking (1st to 5th)

**1st: Provider A** — Despite significant noise and misinterpretation of ambiguous terms, it is the only provider that combines full topic coverage, dated articles, zero errors, and a meaningful density of genuinely relevant strategic content across most topics.

**2nd: Provider B** — Highest volume and best source quality (Reuters, Bloomberg, WSJ), but the complete absence of dates is a critical failure for news monitoring, and precision is poor with entire topic sets filled with irrelevant results.

**3rd: Provider D** — Delivers the cleanest, most precisely targeted results when it works, but 149 errors leaving 11 of 28 topics completely empty makes it fundamentally unreliable.

**4th: Provider C** — Best precision and summary quality of any provider, but returns so few articles (76 total vs. 1,332 for Provider A) that it fails as a monitoring tool, and includes corporate "About" pages and report landing pages as "articles."

**5th: Provider E** — Fewest total articles (85), many topics with only 1 result, and narrow topical coverage that misses the breadth needed for strategic monitoring. Clean execution but insufficient output.

---

## 3. What Each Provider Needs to Fix

### Provider B (2nd → 1st)
- **Critical fix: Add dates to every article.** This is non-negotiable. A news search tool without dates is broken. Implement date extraction from article metadata, publication tags, or page content.
- **Fix precision filtering**: "BOARD | Eastern Asia" should not return generic financial market roundups. Build industry disambiguation that distinguishes physical board materials from corporate governance boards.
- **Eliminate beauty packaging spam from Packaging | Oceania and Packaging Boxes | IN**: These topics are returning irrelevant cosmetics brand news from beautypackaging.com regardless of geography or sub-industry.
- **Filter out TradingView stubs**: Articles showing only "More news from Reuters Image 17 Image 18..." add zero value.
- **Reduce duplicate roundups**: Multiple "North America Manufacturing News Digest" entries from the same source are redundant.

### Provider D (3rd → 1st)
- **Fundamental fix: Eliminate the error rate.** 149 errors leaving 11 topics empty is a showstopper. This requires infrastructure work — either API reliability, query handling, or fallback mechanisms.
- **Expand coverage**: Even when working, many topics return only 0-6 articles. Broaden source indexing.
- **Fix geography disambiguation**: "EQUIPMENT & MACHINERY | Southern Asia" returning Southeast Asia results (Vietnam, Thailand) instead of India/Pakistan/Sri Lanka.
- **These are mostly fixable issues** — the quality of results when delivered is high, suggesting the underlying search logic is sound but the execution pipeline is brittle.

### Provider C (4th → 1st)
- **Fundamental problem: Volume.** 76 total articles across 28 topics is insufficient. The service needs to index dramatically more sources.
- **Remove non-news pages**: Corporate homepages (ENGIE, Maersk, Atos, OMA Group, MM Group, FilmNation), company directories (ZoomInfo, F6S), and market research landing pages (Mordor Intelligence) are not news articles.
- **Fix date attribution**: Pages dated 2026-04-13 that are corporate "About" pages clearly have retrieval dates, not publication dates.
- **Scale the approach**: The precision and summary quality are best-in-class — the challenge is applying that quality at 10-20x the current volume.

### Provider E (5th → 1st)
- **Fundamental problem: Coverage breadth and depth.** 85 total articles is far too few. Most topics get 1-2 results.
- **Fix industry disambiguation**: "Distribution Services | Northern America" should not be dominated by Universal Music Group M&A news when the query context is about physical distribution, mastering, and localization services.
- **Improve summary depth**: One-sentence fragments preceded by keyword tags are insufficient for strategic decision-making without clicking through.
- **Expand beyond event-driven news**: Provider E seems to capture M&A and corporate announcements well but misses pricing trends, regulatory shifts, and market analysis content.
- **These are fundamental problems** — the service appears to be a general-purpose news alert tool rather than an industry monitoring product.

---

## 4. Top Provider's Weaknesses (Provider A)

1. **Severe industry term disambiguation failures**: "BOARD | Eastern Asia" returns corporate governance articles instead of board materials. "Film Distribution | Midwest" returns Iowa gubernatorial candidates and Wisconsin beaver debates. This is not an edge case — it corrupts entire topic categories.

2. **Heavy geographic drift**: "CONSTRUCTION | Central Asia" returns articles about Bulgaria energy, EU oil contingency, India SEZ duty, Pakistan LNG, and Focus Graphite in Canada. "ENERGY & UTILITY | South-eastern Asia" returns articles about India and Bulgaria. Many supposedly region-specific topics include articles from completely different continents.

3. **Boilerplate-contaminated summaries**: Summaries frequently include site navigation, cookie notices, and page chrome rather than clean article excerpts. "Infra Equipment's ki Dunia ki har news, Sirf Infra Junction Whatsapp Par" is not a useful summary.

4. **Irrelevant sources polluting results**: Facebook posts appear as top results for multiple topics. An R CRAN packages listing appears as #1 for Film Entertainment: Distribution Services. Purdue Libraries research guides appear as #1 for Film Distribution. These are not news.

5. **Duplicate articles**: The same article appears multiple times with different regional URLs (e.g., Eversheds-Sutherland "FS+ Country Updates" appears 6 times in "LIQUIDS | Southern Africa" from different country-specific site mirrors). "Rupee opens 125 paise higher" appears twice with different URLs in "BOARD | Eastern Asia."

6. **Market research report landing pages**: Results from marketresearchfuture.com, openpr.com (market report promotions), and indexbox.io are report sales pages, not news.

7. **Trivial mentions inflating results**: Articles mentioning an industry or region in passing without substantive insight are included. The Honeywell Annual Report PDF appearing in both "LIQUIDS | Southern Africa" and "HR SERVICES | Mid Atlantic" is a generic corporate document, not targeted industry news.