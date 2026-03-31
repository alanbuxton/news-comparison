# Companies Analysis — 20260331-214203

*Model: claude-opus-4-6 | Max articles per company per provider: 15*

*Provider labels were anonymised. See `decode-key-20260331-214203.json` to decode.*

---

## 1. Provider-by-Provider Assessment

### Provider A

**Precision**: Abysmal for obscure companies, mediocre for well-known ones. For **Braroll Acessorios Industriais** (a Brazilian industrial accessories company), zero of the 100 articles shown are about Braroll — they are generic manufacturing news, TradingView market feeds, and beauty packaging articles. The same pattern repeats for **Fritz Foss** (96 articles, none about Fritz Foss — instead generic TradingView feeds, WSJ market roundups, and an FBI story), **Dine Cartonnages** (85 articles, none about Dine Cartonnages — food news, CSP Daily News, beauty packaging), **Husky Technologies** (84 articles, none about Husky Technologies — mining news, TradingView feeds), **Jindal Films** (79 articles — dominated by Jindal Stainless results and TradingView noise, not Jindal Films specifically), **KRC Custom Manufacturing** (67 articles, none about KRC — IndustryWeek generics, TradingView), **Jiangin Yonghe Packaging Products** (83 articles, none about the actual company — Beauty Packaging, TradingView), **L M Goes Embalagens** (92 articles, none about L M Goes), **Sigma Chemtrade** (100 articles — dominated by Sigma Lithium, an entirely different company, plus generic chemicals industry news). For **Westrock**, it returns articles about Westrock Coffee Company, not the packaging company (now Smurfit Westrock). Even for well-known companies like **Bloomberg**, the results are almost entirely paywalled Bloomberg articles with boilerplate subscription prompts as summaries. For **Commerzbank AG** and **ExxonMobil**, results are relevant but summaries are often truncated paywall text.

**Coverage**: Returns high article counts (1,943 total) but this is illusory — for roughly half the companies, it found zero genuinely relevant articles while padding the count with noise. It returns nothing useful for Braroll, Fritz Foss, Dine Cartonnages, Husky Technologies, KRC Custom Manufacturing, Jiangin Yonghe, L M Goes Embalagens, or Little Island Productions.

**Date quality**: Zero dates on any article. Every entry shows "[NO DATE]". This is a fundamental failure — a business professional cannot assess recency.

**Summary usability**: Terrible. Summaries are raw scraped boilerplate. Bloomberg articles read "Bloomberg Connecting decision makers to a dynamic network of information, people and ideas…" or "See Breaking News in Context Bloomberg Law provides trusted coverage…" The Borouge results from TradingView read as navigation chrome: "Image 22 Reuters United Carton Industries…" The beauty packaging articles for L M Goes read "View all About Us #### About Us elebrating 30+ years of connecting beauty brand marketers…"

**Source quality**: Heavy reliance on TradingView sidebar feeds (which are just aggregated headline lists, not articles), paywalled Bloomberg/WSJ/FT content with no usable text, and industry publication homepages scraped as articles.

**Hallucination risk**: No obvious fabricated URLs, but the volume of completely irrelevant articles for obscure companies suggests the system is returning any vaguely keyword-adjacent content rather than finding genuine matches.

**Overall verdict**: Provider A is a keyword-matching firehose that buries users in noise, strips all dates, and delivers paywall boilerplate instead of summaries — it is the worst provider in this evaluation by a wide margin.

---

### Provider B

**Precision**: Significantly better than A for well-known companies but still poor for obscure ones. For **Borouge**, top results are directly relevant (ADNOC/OMV Borouge Group International leadership announcements). For **Commerzbank**, strong — UniCredit bid coverage, Commerzbank payout records. For **ExxonMobil**, relevant results like Golden Pass LNG, Guyana FPSO. However, there is a severe spam problem: the same irrelevant "filler" articles appear across many company searches. "NurExone Strengthens U.S. Manufacturing Strategy" (a BioSpace press release about a completely unrelated Israeli biotech) appears in results for Braroll, Borouge, Deloitte, Dine Cartonnages, ExxonMobil, Fritz Foss, Husky Technologies, International Paper, Jiangin Yonghe, Jindal Films, KRC Custom Manufacturing, Klockner Pentaplast, Klöckner Pentaplast, L M Goes, Linklaters, Sigma Chemtrade, and Universal McCann. Similarly, "Nigeria–United Kingdom State Visit" from Mondaq appears in nearly every company search. "DOL Alternative Assets Rule Passes White House Review" and "Biocytogen Announces FDA IND Clearance" appear across 10+ companies. This is clearly systematic filler content injected when the provider cannot find genuine matches.

For **Braroll Acessorios Industriais**, approximately 5-7 of 50 articles are Brazilian business news vaguely related to industrial manufacturing, but none are about Braroll specifically. For **Fritz Foss**, 1 article is marginally relevant ("Fritz öffnet sein Smart Home" — about AVM Fritz!Box, not Fritz Foss). For **Sigma Chemtrade**, the top result is Sigma Lithium (wrong company). For **Husky Technologies**, most "Huskeys" results are about a cybersecurity startup called Huskeys, not Husky Technologies the injection molding company. The Canada.ca article about CC-330 Husky fleet is about military aircraft.

**Coverage**: Returns articles for all companies (1,139 total) but real coverage for obscure companies is padded with filler. Had 8 errors (failed queries).

**Date quality**: All articles have dates, which is a major advantage over Provider A. Dates appear accurate based on article content.

**Summary usability**: Mixed. Some summaries are informative (CBS News layoffs, Commerzbank takeover bid details), but many are just the first paragraph of scraped text with navigation elements. The filler articles obviously provide zero useful information about the queried company.

**Source quality**: Real journalism sources are present (Reuters, Bloomberg, CNBC, BBC) alongside BioSpace press releases, Mondaq legal articles, and other filler that has nothing to do with the queried companies. The systematic injection of identical irrelevant articles across searches is a serious quality problem.

**Hallucination risk**: No fabricated URLs detected, but the systematic filler problem means the provider is knowingly returning irrelevant content to pad results.

**Overall verdict**: Provider B finds real news for well-known companies and provides dates, but its filler problem — identical irrelevant articles injected across 15+ different company searches — wastes the user's time and signals an inability to handle obscure companies honestly.

---

### Provider C

**Precision**: The highest of any provider. For **Borouge**, all 8 results (minus 1 error) are directly and substantively about Borouge — the OMV/ADNOC merger, Borouge 4 agreement, leadership appointments. For **Commerzbank**, all 8 are about Commerzbank — UniCredit bid, earnings beat, buyback, profitability pledges. For **ExxonMobil**, all 10 are about ExxonMobil — Q4 earnings, Guyana projects, Venezuela, CCS, Supreme Court climate suit. For **HPCL Mittal Energy**, all 5 are about HMEL — Rs 2,600 crore investment, NCLT merger approval, Venezuelan crude purchase. For **Husky Technologies**, all 6 are directly about Husky — GPGI CEO appointment, CEO/CFO departures, HyPET system, CompoSecure combination. For **International Paper**, all 4 are directly about IP — split into two companies, containerboard pricing. For **Klöckner Pentaplast**, all results are about the company — restructuring, EcoVadis rating, trade show debuts. For **Sigma Chemtrade**, however, all 7 results are about **Sigma Lithium**, a completely different company — this is a clear false-positive problem on this specific query. For **Jindal Films**, all 8 results are about Jindal Poly Films (the parent company of Jindal Films), which is defensible but imprecise.

**Coverage**: This is the critical weakness. Provider C returned only 85 articles total across all companies — by far the lowest count. It returned **zero articles** for **Entertainment Partners**, **KRC Custom Manufacturing**, and **Linklaters** (all marked as errors). It returned only **1 article** for **CBS News** (a tangential Paramount deal story), **1 article** for **Dine Cartonnages** (about Dine Brands, not Dine Cartonnages — wrong company), and **1 article** for **Universal McCann**. It had 26 errors total, the most of any provider. For **Bloomberg**, only 3 articles (all tangential mentions in Reuters stories). For **L M Goes Embalagens**, **Braroll**, and **Little Island Productions**, zero results.

**Date quality**: All articles have dates. Dates appear accurate.

**Summary usability**: Excellent — the best of any provider. Summaries are clearly written, informative, and tell the user what happened without needing to click. Example: "Commerzbank CEO Bettina Orlopp pledged to accelerate efforts to increase profitability to demonstrate the bank's strength as an independent entity, following UniCredit's takeover bid." Another: "HPCL-Mittal Energy Limited (HMEL) announced a Rs 2,600 crore investment in Punjab's speciality and fine chemicals sector and plans to open 500 new retail fuel outlets across India equipped with modern amenities." Compare this to Provider A's boilerplate or Provider B's raw scraped text.

**Source quality**: High-quality sources: Reuters, Bloomberg, Financial Times, PR Newswire, industry-specific publications (Packaging Gateway, Financier Worldwide, Interplas Insights). No junk.

**Hallucination risk**: Low. No suspicious URL patterns. However, the Sigma Chemtrade → Sigma Lithium false positive is a disambiguation failure.

**Overall verdict**: Provider C delivers the highest-quality individual results with genuinely useful summaries, but its coverage is so thin that it fails the user entirely for half the companies in the test set, making it unreliable as a sole news source.

---

### Provider D

**Precision**: Very high for companies where it returns results. For **Borouge**, all 6 articles are directly about Borouge (merger completion, leadership team, circular waste management partnership). For **Commerzbank**, all 5 are relevant (UniCredit exchange offer, Hawk AI partnership, share buyback, Q4 results, BESS financing). For **ExxonMobil**, all 7 are about ExxonMobil (2025 results, redomiciling to Texas, Proxxima resins, synthetic graphite, PlastIndia). For **International Paper**, all 8 are about IP (Mississippi plant, split into two companies, closures, CEO commentary). For **Husky Technologies**, all 4 are about Husky. For **Klöckner Pentaplast** (both spellings), all results are on-target. For **Entertainment Partners**, all 4 are from EP's own website — directly relevant.

However, there are serious problems with certain companies. For **Braroll Acessorios Industriais**, the single result is about ADATA Technology at CES — completely unrelated. For **L M Goes Embalagens**, all 4 results appear to be **hallucinated articles**. The URLs follow suspicious patterns: `www.valor.com.br/negocios/lm-goes-parceria-nestle`, `exame.com/empresas/lm-goes-financiamento-expansao`, `www.folha.uol.com.br/mercado/anvisa-embalagens-lm-goes`, `gazetamercantil.com.br/inovacao/lm-goes-embalagem-rfid`. These URLs are suspiciously neat, and the summaries describe specific partnerships (with Nestlé), financing rounds (R$ 150 million), regulatory impacts, and product launches that cannot be verified. Gazeta Mercantil ceased publication in 2009. This is strong evidence of hallucinated content. Similarly, for **Husky Technologies**, the article citing a "$500M Financing Deal" from Reuters (`reuters.com/business/husky-technologies-500m-financing-2026-03-15`) and the "Berry Global partnership" from Plastics News and the "HyPET HPP6e" from Packaging World and the "EU Regulatory Changes" from Chemical Week all have suspiciously clean URLs and cannot be verified as real published articles. **This is hallucination.**

For **CBS News**, 2 of 5 results are about "cbs Corporate Business Solutions" (a German consulting firm), not CBS News — entity disambiguation failure. For **Jiangin Yonghe Packaging Products**, 1 of 2 results is a Scribd document with no mention of the company; the other is a Walt Disney manufacturing list that doesn't mention the company either. For **Sigma Chemtrade**, 1 of 2 results is about Chemtrade Logistics Income Fund (different company). For **Universal McCann**, 1 of 2 results is about "Universal Media, Inc." (a different company), and the other mentions a former UM executive who left.

**Coverage**: Low volume (97 total articles) but better distributed than C. Returns something for every company except none are completely blank. However, quality for obscure companies is poor.

**Date quality**: All articles have dates. Most appear accurate, though the hallucinated articles naturally have plausible but unverifiable dates.

**Summary usability**: Good. Summaries are informative and structured, often including specific financial figures and strategic details. Example: "International Paper to invest $225 million in a new 468,000-square-foot sustainable packaging facility in Brandon, Mississippi, replacing an aging Richland box plant."

**Source quality**: Mix of legitimate sources (Reuters, PR Newswire, Packaging Dive, Financier Worldwide) and the hallucinated articles which appear to come from real publication names but have fabricated URLs.

**Hallucination risk**: **HIGH.** The L M Goes Embalagens results are almost certainly fabricated. The Husky Technologies results from Reuters, Plastics News, Packaging World, and Chemical Week cannot be verified. This is a disqualifying flaw for a business professional who needs to trust the information.

**Overall verdict**: Provider D shows strong precision and useful summaries for well-known companies, but it hallucinated entire articles for at least two companies, which makes it fundamentally untrustworthy despite otherwise good quality.

---

### Provider E

**Precision**: Very high. For **Borouge**, all 8 articles are directly about Borouge — AI-driven control room, Q4 2025 results, Indonesia recycling partnership, leadership appointments. For **Commerzbank**, all 20 articles are about Commerzbank/UniCredit — bid, share buyback, Hawk AI partnership, analyst coverage. For **ExxonMobil**, all 20 are about ExxonMobil — Golden Pass LNG, Guyana operations, Alaska lease sale, chemical recycling plant, Fife ethylene closure, immersion cooling with Infosys. For **CBS News**, all 20 are about CBS News — radio shutdown, layoffs, Bari Weiss overhaul, staff departures, contract protests. For **HPCL Mittal Energy**, all 5 are directly about HMEL — Rs 2,600 crore investment, Venezuelan crude purchase. For **Husky Technologies**, all 11 are about Husky — CompoSecure combination, CEO/CFO departures, new CEO appointment, India expansion, short seller report. For **International Paper**, all 20 are about IP — Mississippi plant, split into two companies, plant closures. For **Deloitte**, all 12 are about Deloitte — job title overhaul, ConnectSafe facility, Birmingham HQ move, new alliances. For **Klöckner Pentaplast** (both spellings), all 3 are directly relevant. For **Westrock**, all 20 are about Smurfit Westrock — Ecuador acquisition, Q4 earnings, board changes, analyst coverage, plant closures, Ryder Cup partnership. For **Linklaters**, only 1 article (office expansion) — low but relevant. For **Entertainment Partners**, 3 of 4 results are about Brillstein Entertainment Partners (a different company), not Entertainment Partners the production payroll company. This is a disambiguation failure.

For obscure companies, Provider E is thin. **Braroll**, **Dine Cartonnages**, **Fritz Foss**, **KRC Custom Manufacturing**, **Jiangin Yonghe**, **L M Goes Embalagens**, **Little Island Productions**, and **Sigma Chemtrade** return zero results. This is honest — Provider E does not fabricate results when it cannot find them — but it means coverage of small, non-English companies is absent.

**Coverage**: 152 total articles. Strong depth for well-known companies (20 articles each for CBS News, Commerzbank, ExxonMobil, International Paper, Westrock) but zero for 8 obscure companies.

**Date quality**: All articles have precise dates and timestamps (often to the second). Dates are accurate and verifiable.

**Summary usability**: Good but inconsistent. Many summaries are fragmentary, starting with a keyword or phrase: "closing down: CBS News Radio is closing down after 100 years of operation." Others are more complete: "BOLTON, Ontario - Husky Technologies, a segment of GPGI, Inc. (NYSE: GPGI), announced Wednesday that Chief Executive Officer Bradley Selleck and Chief Financial Officer John Linker will be leaving." The keyword-prefix format is slightly unusual but still informative enough to understand the story.

**Source quality**: Excellent. Reuters, AP, Bloomberg, Business Wire, GlobeNewswire, Variety, Deadline, Investing.com, industry-specific trade publications (Plastics News, Paper Advance, Packaging Insights, Drilling Contractor). No junk filler, no TradingView sidebar scrapes, no beauty packaging noise.

**Hallucination risk**: Very low. No suspicious URL patterns detected. Where the provider cannot find results, it returns nothing rather than fabricating content.

**Overall verdict**: Provider E delivers the most reliable and useful results for well-known and mid-profile companies, with strong precision, real dates, quality sources, and no hallucination — but it cannot find news about small/obscure companies.

---

## 2. Ranking (1st to 5th)

**1st: Provider E** — Highest overall reliability: precise results, real dates, quality sources, no hallucination, and the deepest coverage for well-known companies (20 articles each for multiple companies).

**2nd: Provider C** — Highest per-article quality with the best summaries and near-perfect precision, but total coverage is so thin (85 articles, 26 errors, zero results for 3+ companies) that it cannot serve as a standalone source.

**3rd: Provider B** — Provides dates, finds real news for well-known companies, and has broad coverage, but the systematic injection of identical irrelevant filler articles (NurExone, Mondaq Nigeria, DOL Alternative Assets) across 15+ company searches is a major quality problem.

**4th: Provider D** — Strong precision and summaries for known companies, but the hallucinated articles for L M Goes Embalagens and Husky Technologies are disqualifying for any use case requiring trust, and the entity disambiguation failures (CBS News vs. cbs consulting, Sigma Chemtrade vs. Chemtrade Logistics) further undermine reliability.

**5th: Provider A** — Zero dates on any article, summaries are paywall boilerplate or scraped navigation chrome, and for at least 8 of 20 companies it returned zero relevant articles while padding results with 80-100 pieces of noise. It is unusable for the stated purpose.

---

## 3. What Each Provider Needs to Fix

### Provider C (2nd → 1st)
- **Fixable: Expand coverage.** The provider needs to index more sources and return more than 1-8 articles per company. For well-known companies like CBS News, Bloomberg, and Deloitte, returning only 1-5 articles when competitors find 20+ is unacceptable.
- **Fixable: Eliminate error rate.** 26 errors out of 20 companies is too high. Zero results for Entertainment Partners, KRC Custom Manufacturing, and Linklaters (the latter being a major global law firm) suggests indexing gaps.
- **Fixable: Fix entity disambiguation for Sigma Chemtrade.** All 7 results were about Sigma Lithium. The system needs to distinguish companies that share the "Sigma" prefix.
- **Fixable: Fix Dine Cartonnages disambiguation.** The single result was about Dine Brands (Applebee's/IHOP), not Dine Cartonnages the French packaging company.
- **Fundamental problem: The provider appears to return only results it is highly confident about.** This is a sound philosophy but needs a larger source corpus to make it work.

### Provider B (3rd → 1st)
- **Fixable: Eliminate the filler article injection system.** The identical articles appearing across 15+ company searches (NurExone BioSpace, DOL Alternative Assets, Nigeria-UK State Visit, Biocytogen FDA clearance, CapsoVision financing) must be removed. If the provider cannot find relevant articles for a company, it should return fewer results rather than padding with unrelated content.
- **Fixable: Fix entity disambiguation.** Husky Technologies returns results about "Huskeys" (a cybersecurity startup). Sigma Chemtrade returns Sigma Lithium results.
- **Fixable: Improve summary quality.** Many summaries are raw scraped text with navigation elements. They should be cleaned or synthesized.
- **Fundamental problem: The provider's approach to obscure companies appears to be "return something, anything" rather than "return nothing if nothing is relevant."**

### Provider D (4th → 1st)
- **Critical: Eliminate hallucinated articles.** The L M Goes Embalagens results (fake Valor Econômico, Exame, Folha de S.Paulo, and defunct Gazeta Mercantil URLs) and the Husky Technologies results (fake Reuters, Plastics News, Packaging World, Chemical Week URLs with suspiciously clean paths and unverifiable content) must be eliminated. This is the single most important fix. A business professional making decisions based on fabricated news could suffer real consequences.
- **Fixable: Fix entity disambiguation.** CBS News results included cbs Corporate Business Solutions (a German consulting firm). Sigma Chemtrade returned Chemtrade Logistics. Universal McCann returned Universal Media, Inc.
- **Fixable: Increase coverage.** 97 total articles is thin, and 1-3 articles per obscure company is inadequate.
- **Fundamental problem: The hallucination issue suggests the underlying model generates plausible content when it cannot find real results. This is architecturally dangerous and may require fundamental changes to the retrieval approach.**

### Provider A (5th → 1st)
- **Critical: Add date extraction.** Zero dates across 1,943 articles is a total failure for a time-sensitive use case.
- **Critical: Fix summary extraction.** Summaries must not be paywall prompts ("See Breaking News in Context Bloomberg Law provides trusted coverage…"), navigation menus, or cookie banners. The system needs to extract actual article content or, failing that, generate a meaningful summary from the headline.
- **Critical: Implement relevance filtering.** For 8+ companies, 100% of returned articles were irrelevant. The system is matching on broad industry keywords (packaging, manufacturing, industrial) rather than the specific company name. It must verify that the queried company is actually mentioned substantively in the article.
- **Critical: Stop returning TradingView sidebar feeds as articles.** These are not articles; they are lists of headlines from a financial charting platform.
- **Fundamental problem: Provider A appears to be a search engine without a relevance model. It returns anything that matches broad keywords, without filtering for the actual company. Fixing this requires building a company-entity-matching system from scratch.**

---

## 4. Top Provider's Weaknesses (Provider E)

1. **Zero coverage for obscure/small companies.** Braroll Acessorios Industriais, Dine Cartonnages, Fritz Foss, KRC Custom Manufacturing, Jiangin Yonghe Packaging Products, L M Goes Embalagens, Little Island Productions, and Sigma Chemtrade all returned zero results. A user researching a meeting with any of these companies gets nothing.

2. **Entertainment Partners disambiguation failure.** 3 of 4 results are about Brillstein Entertainment Partners, a talent management firm, not Entertainment Partners, the production payroll/accounting company. This is a meaningful error that could mislead meeting preparation.

3. **Linklaters severely undercovered.** Only 1 article (an office lease expansion) for a Magic Circle law firm that has been involved in multiple major deals during the period. Provider B found 47 articles including major M&A advisory work. Provider C found zero, but that's an error — Provider E's 1 article is barely better.

4. **Jindal Films undercovered.** Only 2 articles, both about Jindal Poly Films (the parent). Providers B and C found 45 and 8 articles respectively about Jindal Films and related Jindal entities.

5. **Summary format is inconsistent.** The keyword-prefix format ("closing down:", "Added Texas:", "purchase:") is functional but less polished than Provider C's complete narrative summaries. Some summaries are fragments rather than complete thoughts.

6. **Bloomberg coverage is weak.** Only 3 articles, none about Bloomberg as a company (they are about Bloomberg Indices products and a Beko CEO transition that mentions Bloomberg tangentially). For a major financial data company, this is thin.

7. **Klöckner Pentaplast coverage is thin.** Only 3 articles (same 3 for both spellings). Provider B found 50 and Provider C found 5 with much richer detail about the Chapter 11 restructuring and post-emergence strategy.