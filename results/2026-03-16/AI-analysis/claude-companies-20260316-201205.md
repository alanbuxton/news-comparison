# Companies Analysis — 20260316-201205

*Model: claude-opus-4-6 | Max articles per company per provider: 15*

*Provider labels were anonymised. See `decode-key-20260316-201205.json` to decode.*

---

## 1. Provider-by-Provider Assessment

### Provider A (100 articles, 0 errors)

**Precision**: Very high. Nearly every article is directly about the queried company with substantive strategic content. The few weak spots: Bloomberg search returned supply chain risk articles that mention Bloomberg's data/index products only tangentially (e.g., "Economic Risk to Supply Chain Up Significantly Over Last Quarter" from Lehigh News — Bloomberg the company is not the subject). Dine Cartonnages returned an event listing for a "Cartonnage" spectacle in La Roche-Posay and a hotel dining article — neither is about the company Dine Cartonnages. Fritz Foss returned a Home Assistant release note about a "Fritz" integration — this is about AVM Fritz!Box, not Fritz Foss. The KRC Custom Manufacturing results are about a different KRC (aluminum profiles manufacturer, not custom manufacturing). Sigma Chemtrade returned one result about Chemtrade Logistics Income Fund and one about a "Sigma Enterprises" port listing — neither is Sigma Chemtrade specifically. So roughly 8–10 of 100 articles are false positives or entity-mismatched, putting precision around 90%.

**Coverage**: Excellent for well-known and mid-tier companies (Commerzbank, Klöckner Pentaplast, International Paper, HPCL Mittal Energy, Husky Technologies, Borouge, Linklaters all have strong results). For obscure companies, it attempts coverage: Braroll Acessorios Industriais gets 2 articles, L M Goes Embalagens gets 2 articles. However, these articles for Brazilian companies look suspiciously fabricated — the Braroll articles cite Folha de S.Paulo and Valor Econômico with URLs that follow a neat pattern (e.g., `folha.uol.com.br/negocios/2026/02/braroll-parceria-automotivo.shtml`) and describe a "parceria estratégica com gigante do setor automotivo" and a "R$ 50 Milhões" BNDES financing. These URLs and stories are almost certainly hallucinated — Braroll is too obscure for Folha de S.Paulo coverage, and the URL slug structure looks manufactured. Similarly, L M Goes Embalagens articles on Valor Econômico and Exame with clean URL patterns are suspect hallucinations. Little Island Productions returned 3 plausible articles (Playbill job listing, Obie Awards, Washington University source). Entertainment Partners returned only 1 article (an EP blog post). Dine Cartonnages returned 0 real results. Fritz Foss returned 0 real results. Jiangin Yonghe Packaging Products is not listed at all.

**Date quality**: 100% of articles have dates. Dates appear accurate and well-formatted with timezone information.

**Summary usability**: Excellent. Summaries are concise, information-dense, and allow the user to understand the story without clicking. Example of a good summary: "Commerzbank reports that it has exceeded its 2025 growth target and achieved a record operating result... strong profitability and an improved capital position." Example of adequate summary: The KRC aluminum profiles articles are coherent summaries but about the wrong company entirely.

**Source quality**: Mostly high-quality sources — press releases from company sites, major financial news (Economic Times, Business Standard, PR Newswire), industry publications (Packaging Dive, Supply Chain Dive). Some sources are lower quality but acceptable (Whalesbook, Polymerupdate). No raw boilerplate or navigation menus.

**Hallucination risk**: HIGH for obscure companies. The Braroll and L M Goes Embalagens articles are almost certainly fabricated. The URLs follow suspiciously clean patterns, the stories describe implausibly specific financial details for companies with virtually no public profile, and the publications cited (Folha, Valor, Exame) would not typically cover these micro-enterprises.

**Overall verdict**: Provider A delivers excellent, concise, strategically relevant results for known companies, but fabricates plausible-looking articles for obscure companies it cannot find, which is a serious trust violation.

---

### Provider B (1139 articles, 0 errors)

**Precision**: Terrible for obscure companies, mediocre for well-known ones. The system floods results with irrelevant noise. For Braroll Acessorios Industriais (49 articles), nearly every article is about completely unrelated topics: Tandoor Morni restaurant accessories, Ambev stock, off-road motorcycle manufacturers, Elektros EV patents, HUAWEI MiniFTTO products. Zero articles are about Braroll. For Fritz Foss (50 articles), the results are futurist conference press releases, Lyzr AI funding announcements, and random TradingView market data — zero are about Fritz Foss. For Dine Cartonnages (48 articles), results include Tandoor Morni, DS Smith packaging, carton market reports — none about Dine Cartonnages specifically. For Little Island Productions (48 articles), results include futurist conferences, Kinder Ready education, film production companies — almost none about Little Island Productions specifically. Even for known companies like Bloomberg (48 articles), many results are articles published on Bloomberg platforms but not *about* Bloomberg as a company (e.g., "India Scraps More Soy Oil Cargoes" from Bloomberg News, "Energy Stocks Rally" from Bloomberg). For Sigma Chemtrade (49 articles), results mix Sigma360, Sigma Healthcare, and Chemtrade Logistics — different companies that share partial names. The Chemtrade Logistics results are about a different entity than Sigma Chemtrade.

**Coverage**: Casts the widest net (1139 articles) but almost none of the volume is useful for obscure companies. It finds industry-adjacent content but not the actual companies. For well-known companies, there is genuine coverage buried under noise.

**Date quality**: Nearly 100% have dates. However, some dates are only timestamps from social media posts (Facebook) rather than article publication dates.

**Summary usability**: Terrible. Most "summaries" are raw scraped boilerplate — navigation menus, cookie banners, subscription prompts, and page metadata. Example: Bloomberg article #1 summary starts with "S&P Global - Two US banks posted double-digit percentage... | Facebook Facebook Log In ## S&P Global's Post." Commerzbank article #7 summary: "Earnings call transcript: Partners Group Q4 2025 sees stock plunge ... Investing.com's stocks of the week Wall Street posts three-week losing streak..." — this is scraped page chrome, not a summary. CBS News article #9 reads: "Katie Nell, Author at The Blum Firm ## Hanging Onto Frugality? You're Not Alone!" — completely irrelevant.

**Source quality**: Low. Massive reliance on syndicated press release distribution (same article from Pocono Record, Wausau Daily Herald, The Hutchinson News, etc. — identical content distributed by EIN Presswire across dozens of local USA TODAY Network papers). The same Tandoor Morni press release appears under Braroll, Dine Cartonnages, and other searches. Facebook posts, OpenPR market reports, and TradingView news ticker items are not useful sources.

**Hallucination risk**: Low — the articles are real, they're just not about the right companies. The problem is false positives, not fabrication.

**Overall verdict**: Provider B is a firehose of irrelevant content disguised as coverage. It appears to keyword-match broadly and return everything vaguely related, making it useless for meeting preparation without extensive manual filtering.

---

### Provider C (143 articles, 0 errors)

**Precision**: High. Results are overwhelmingly relevant to the queried companies. CBS News (20 articles) — all directly about CBS News operations, personnel changes, editorial decisions. Commerzbank (11 articles) — all substantive: record profits, share buybacks, CRO departure, AML partnership with Hawk. International Paper (20 articles) — all about IP's split, plant closures, earnings, pricing. ExxonMobil (20 articles) — all about ExxonMobil operations, earnings, CCS projects, FPSO acquisitions. The few weak spots: Entertainment Partners (3 articles) returned Brillstein Entertainment Partners results (a different company from "Entertainment Partners" the payroll/production services company). This is an entity disambiguation failure. Linklaters returned only 1 article (office expansion) — thin but accurate.

**Coverage**: Moderate volume (143 articles) but concentrated on companies with real news presence. Zero results for: Braroll Acessorios Industriais, Dine Cartonnages, Fritz Foss, KRC Custom Manufacturing, L M Goes Embalagens, Little Island Productions, Jiangin Yonghe Packaging Products, Sigma Chemtrade (only for one spelling), Universal McCann. This means 7+ companies received zero coverage. HPCL Mittal Energy got only 2 articles. Jindal Films got only 2 articles. This is honest — better to return nothing than fabricate.

**Date quality**: 100% have dates, with precise timestamps including hours and minutes. Accurate.

**Summary usability**: Good. Summaries are clean, informative, and extracted from article content. Example: Borouge article — "Abu Dhabi Polymers Co Borouge LLC (ADX: BOROUGE) presented its Q4 and full-year 2025 results on February 4, 2026, highlighting record operational performance despite challenging market conditions." Clean and useful. Some summaries are truncated ("Beko (Arçelik A.Ş. )") but this is rare.

**Source quality**: Excellent. Investing.com, Reuters, AP News, Variety, PR Newswire, industry publications (Packaging Insights, Plastics News, Recycling Today). No Facebook posts, no syndicated press release spam, no boilerplate.

**Hallucination risk**: None detected. All articles appear to be real, from verifiable sources with plausible URLs.

**Overall verdict**: Provider C is the most trustworthy — high precision, clean summaries, real sources, no hallucinations — but it has significant coverage gaps for small and obscure companies.

---

### Provider D (1846 articles, 0 errors)

**Precision**: Poor to mediocre. Similar to Provider B's problem but at even greater scale. For Fritz Foss (83 articles), results include "Drop in wind power boosts spot prices," "Retired FBI Agent Reacts To Just-Released Surveillance Photos," "Flash flooding eases in Australia" — zero are about Fritz Foss. For Braroll Acessorios Industriais (82 articles), results include "Carrefour Aims to Boost Tech," "The Malls Powering Luxury Sales in India," "Minimalism Was on Its Way Out" — zero about Braroll. For Dine Cartonnages (80 articles), results include SMX Denim press releases (syndicated 10+ times), Reuters geopolitical news, "self-driving truck firm Gatik" — zero about Dine Cartonnages. For HPCL Mittal Energy (82 articles), most results are about the broader Indian energy sector, ArcelorMittal renewables, or Reliance Industries — only a few directly reference HMEL. For Husky Technologies (65 articles), results include "Elon Musk Says xAI May Build an AI Satellite Factory on the Moon," "Atlassian Stock Rises on News of 10% Workforce Reduction," "Spirit Airlines looks to transfer two Chicago airport gates" — almost none about Husky Technologies.

For known companies, precision is better: Commerzbank (71 articles) includes substantive UniCredit takeover coverage, but also generic European banking roundups and Reuters market tickers where Commerzbank is mentioned in passing. Bloomberg (88 articles) overwhelmingly returns Bloomberg Law News stories that are published *on* Bloomberg's platform but not *about* Bloomberg the company.

**Coverage**: Highest volume (1846 articles) but the vast majority is noise. No actual coverage of Braroll, Dine Cartonnages, Fritz Foss, KRC Custom Manufacturing, L M Goes Embalagens, Little Island Productions, or Jiangin Yonghe Packaging Products despite returning 50-93 articles for each.

**Date quality**: Catastrophic. Nearly every article shows "[NO DATE]." This is a fundamental failure — the user cannot determine article recency. For a business professional preparing for meetings, undated articles are nearly useless.

**Summary quality**: Terrible. Summaries are raw scraped page content including navigation menus, subscription prompts, image placeholders ("Image 1," "Image 2"), cookie banners, and JavaScript snippets. Example from Bloomberg #1: "A Houston lawyer was booted from the race for a judge seat... Image 19Simpson Thacher Hires Wachtell Dealmaker in Strategic M&A Move ---" Example from CBS News #2: "Police are giving an update on the investigation into the deadly Brown University shooting and the manhunt for the gunman. #news #brownuniversity #crime CBS News 24/7 is the premier anchored streaming..." — this is a YouTube video description scraped verbatim.

**Source quality**: Mix of high-quality sources (Reuters, WSJ, CNBC, Bloomberg) and irrelevant aggregators (TradingView news tickers, Social News XYZ video posts, Beauty Packaging for packaging company searches). TradingView articles are particularly problematic — they're market data pages where the company name appears in a sidebar widget, not in substantive content.

**Hallucination risk**: Low — articles are real but irrelevant. No fabrication detected.

**Overall verdict**: Provider D returns the most articles but extracts the least value. Missing dates, scraped boilerplate summaries, and massive false-positive rates make it nearly unusable for meeting preparation.

---

### Provider E (94 articles, 21 errors)

**Precision**: High for companies where results exist. Borouge (8 articles) — all directly relevant: merger with Borealis, Q4 results, AI proof of concept, MoU with KEI Industries. Commerzbank (7 articles) — all substantive: UniCredit takeover bid, share buybacks, government rejection. International Paper (10 articles) — all relevant: company split, plant closures, M&A rumors. Husky Technologies (7 articles) — all directly about Husky: CEO appointment, leadership transitions, GPGI combination. Jindal Films (9 articles) — some are about Jindal Poly Films specifically (class action suit, Q3 results), which is related to but distinct from "Jindal Films." The entity disambiguation is imperfect but the articles are about the broader Jindal film/packaging entity. Sigma Chemtrade (5 articles) — 3 of 5 are about Sigma Lithium, not Sigma Chemtrade. This is a clear false positive. The other 2 about Chemtrade Logistics are about a different entity than "Sigma Chemtrade."

Fritz Foss (2 articles) — both are about Foss Swim School, not "Fritz Foss." False positive. Little Island Productions (1 article) — about Little Palm Island resort, not Little Island Productions. False positive.

**Coverage**: Significant gaps. Entertainment Partners returned 0 articles (3 errors). HPCL Mittal Energy returned 0 articles (7 errors). Universal McCann returned 0 articles (6 errors). Braroll Acessorios Industriais is not listed. Dine Cartonnages is not listed. KRC Custom Manufacturing is not listed. L M Goes Embalagens is not listed. Jiangin Yonghe Packaging Products is not listed. The 21 errors suggest systematic failures for certain queries.

**Date quality**: 100% have dates. All appear accurate.

**Summary usability**: Excellent. Summaries are clearly written, information-dense, and specifically crafted for business context. Example: Commerzbank article — "UniCredit SpA made a €35 billion ($40 billion) bid for Commerzbank AG to increase its stake above 30%, aiming to gain more influence despite opposition from the German government." Example: International Paper — "International Paper announced it will split into two independent publicly traded companies by spinning off its European packaging business, combining DS Smith and its own EMEA operations." These are the best summaries across all providers.

**Source quality**: Strong. Bloomberg, Reuters, PR Newswire, Fortune, Law.com, Packaging Dive, industry publications. No scraped boilerplate, no syndicated press release spam.

**Hallucination risk**: None detected for returned articles. The errors (21) likely indicate the system failing gracefully rather than fabricating content.

**Overall verdict**: Provider E produces the highest-quality individual results with excellent summaries, but fails entirely on multiple companies and has notable entity-matching errors (Sigma Lithium for Sigma Chemtrade, Foss Swim School for Fritz Foss, Little Palm Island for Little Island Productions).

---

## 2. Ranking (1st to 5th)

**1st: Provider C** — Highest precision, no hallucinations, clean summaries, reliable sources; the only provider a business professional can trust without second-guessing every result.

**2nd: Provider E** — Best summaries and strong strategic relevance where it works, but 21 errors causing complete failures for multiple companies and several entity-matching mistakes prevent it from being #1.

**3rd: Provider A** — Good coverage and summaries for known companies, but hallucinated articles for obscure Brazilian companies (Braroll, L M Goes) is a disqualifying trust violation that drops it below providers that honestly return nothing.

**4th: Provider B** — Returns real articles but buries them under mountains of irrelevant syndicated press releases and scraped boilerplate; the signal-to-noise ratio makes it impractical for meeting prep.

**5th: Provider D** — Largest volume but worst usability: no dates on any articles, scraped navigation menus as "summaries," and false-positive rates exceeding 90% for obscure companies make it actively harmful.

---

## 3. What Each Provider Needs to Fix

### Provider E (2nd → 1st)
**Fixable issues:**
- Fix the systematic query failures that produce errors for Entertainment Partners, HPCL Mittal Energy, Universal McCann, and others — these appear to be API/timeout issues, not fundamental limitations
- Implement entity disambiguation to distinguish Sigma Chemtrade from Sigma Lithium and Chemtrade Logistics; Foss Swim School from Fritz Foss; Little Palm Island from Little Island Productions
- Add coverage for non-English and very small companies (Braroll, L M Goes, Dine Cartonnages) — even returning zero results is acceptable, but the system should at least attempt the search without erroring

**Fundamental problem:** The error rate (21 of ~115 attempted queries) suggests infrastructure instability that must be resolved.

### Provider A (3rd → 1st)
**Critical fix:** Eliminate hallucinated articles entirely. The Braroll articles citing Folha de S.Paulo and Valor Econômico and the L M Goes articles citing Valor and Exame are fabricated. This is the single most important fix — return zero results rather than invent plausible-looking coverage. A business professional citing a fabricated article in a meeting faces professional embarrassment.

**Fixable issues:**
- Improve entity disambiguation: KRC Aluminum Profiles ≠ KRC Custom Manufacturing; Fritz!Box integration ≠ Fritz Foss; "Cartonnage" spectacle ≠ Dine Cartonnages
- For Bloomberg, filter out articles that are merely published on Bloomberg platforms vs. articles *about* Bloomberg as a company
- Increase article volume for well-covered companies (Commerzbank has 7 articles vs. Provider C's 11)

### Provider B (4th → 1st)
**Fundamental problems:**
- Implement relevance filtering: stop returning every article that shares a keyword with the query. The current approach of returning 49-50 articles per company regardless of relevance is broken by design
- Replace scraped boilerplate with actual summaries — extracting "Facebook Log In ## S&P Global's Post" as a summary indicates no summarization layer exists
- Deduplicate syndicated content: the same EIN Presswire press release about Tandoor Morni appears across Pocono Record, Wausau Daily Herald, The Hutchinson News, etc., and none of these are relevant to Braroll or Dine Cartonnages

**Fixable issues:**
- Remove Facebook posts, TradingView sidebar mentions, and OpenPR market research spam from results
- Implement company-level entity matching rather than keyword matching

### Provider D (5th → 1st)
**Fundamental problems:**
- Extract and display article dates — "[NO DATE]" on every single article is a dealbreaker. This suggests the scraper cannot parse dates from HTML, which is a foundational engineering failure
- Build actual summarization: current "summaries" are raw HTML scrapes including "Image 1," "Image 2," navigation links, and JavaScript fragments
- Implement relevance filtering: returning "Retired FBI Agent Reacts To Just-Released Surveillance Photos" for Fritz Foss and "Elon Musk Says xAI May Build an AI Satellite Factory on the Moon" for Husky Technologies indicates no relevance scoring exists
- Reduce false-positive rates from >90% to <20% for obscure companies

**Fixable issues:**
- Remove TradingView market ticker pages where the company name appears only in a sidebar widget
- Deduplicate results (same Reuters wire story appears multiple times via different TradingView pages)
- Remove Social News XYZ video transcript posts

---

## 4. Top Provider's Weaknesses (Provider C)

1. **Severe coverage gaps for small companies**: Zero results for Braroll Acessorios Industriais, Dine Cartonnages, Fritz Foss, KRC Custom Manufacturing, L M Goes Embalagens, Little Island Productions, Jiangin Yonghe Packaging Products, and Universal McCann. A user searching for any of these gets nothing.

2. **Thin coverage for mid-tier companies**: HPCL Mittal Energy got only 2 articles despite significant news (₹2,600 crore investment, Venezuelan oil purchases, retail fuel station expansion). Jindal Films got only 2 articles despite a landmark class action suit and ex-Ilva bidding activity. Linklaters got only 1 article despite numerous deal advisories.

3. **Entity disambiguation failure on Entertainment Partners**: All 3 results are about Brillstein Entertainment Partners, a talent management firm, not Entertainment Partners, the payroll and production services company for the entertainment industry. The user would receive completely wrong information.

4. **Lower article volume than competitors even for well-covered companies**: Commerzbank has 11 articles vs. Provider A's 7 (but Provider A's are also strong), and Provider C misses the Hawk AI/AML partnership that Provider B found and the UniCredit takeover bid that Provider E captured for March 16.

5. **Missing the most recent breaking news**: The UniCredit takeover bid for Commerzbank on March 16, 2026 is covered by Providers A, B, D, and E but not by Provider C, whose most recent Commerzbank article is March 11. For a time-sensitive meeting prep use case, missing the biggest story of the week is a significant gap.

6. **No results for Klöckner Pentaplast's post-restructuring strategic moves**: Provider C covers the Chapter 11 exit and court approval but misses the February 2026 trade show appearances (Packaging Innovations, FOODTECH) and the PSV sustainability certification that Providers A and B captured.