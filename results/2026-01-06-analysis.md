
# Results

## Date run: 2026-06-06

## Industry & Region
||Perplexity|Syracuse|Linkup|Notes|Winner|False Positives|
|---|---|---|---|---|---|---|
|PE Resins, US|4|0|2||P||
|Film Distribution, Midwest|1|0|1|Perplexity is about Window Film, not Movies|L|P|
|Film Entertainment -> Film Distribution, Midwest|0|0|1||L||
|Packaging Boxes, IN|1|2|10|Perplexity doesn't have news, Linkup has article with wrong date (March 2025)|S|P,L|
|Packaging -> Packaging Boxes, IN|4|2|10|Perplexity doesn't have news, Linkup has article with wrong date (March 2025)|S|P,L|
|Road Freight, Europe|17|13|2|Perplexity has generic "top 10" lists and is not Europe|S|P|
|MRO, South America|2|0|10||L||
|Film (BOPP Film, BOPET, PE Film etc), CN|4|0|3|Perplexity has generic content, Linkup is about movie business|-|P,L|
|Flexible Packaging -> Film (BOPP Film, BOPET, PE Film etc) - CN|6|0|2|Perplexity has generic content|L|P|
|Distribution Services (Distribution, Mastering, Localization etc), Northern America|3|20|10|All are confused between Film distribution and logistics|-|P,S,L|
|Film Entertainment -> Distribution Services (Distribution, Mastering, Localization etc), Northern America|1|20|0|Perplexity doesn't have false positives, but also misses most stories|-|S|

## Company Name
||Perplexity|Syracuse|Linkup|Notes|Winner(P/S/L)|False Positives|
|---|---|---|---|---|---|---|
|ExxonMobil|10|13|6||-||
|Borouge|8|2|0||P||
|Sigma Chemtrade|0|0|0||-||
|HPCL Mittal Energy|5|5|1|Perplexity has newer stories|P||
|L M Goes Embalagens|0|0|0||-||
|Westrock|9|4|5||P|L|
|International Paper|9|3|4||P|S|
|Dine Cartonnages|1|0|0||-||
|Jiangin Yonghe Packaging Products|3|0|0||-|P|
|Fritz Foss|1|0|0|Perplexity story is about Gary Fritz|-|P|
|Husky Technologies|8|2|10|All same stories covered, Linkup includes a 2025 story with a 2026 date|P|L|
|KRC Custom Manufacturing|1|0|1|Perplexity is a false positive|-|P|
|Braroll Acessorios Industriais|2|0|0|Perplexity links are to pages that don't open (DNS error)|-|-|
|Jindal Films|4|1|6|Syracuse doesn't find "Jindal Poly Films"|L||
|Klöckner Pentaplast|7|6|2|Some of the Perplexity results are non-English duplicates|S||
|Klockner Pentaplast|6|6|9|L||
|Entertainment Partners|1|1|0|Perplexity story is about partnership with London Film School, Syracuse story is about senior hire|P,S||
|Universal McCann|2|0|7||L||
|Little Island Productions|3|0|0|Perplexity links are job ads|-|P|
|Commerzbank AG|5|4|10||L|
|Linklaters|7|1|7||L||

# Detailed Analysis

GOOD RESULT = content is relevant and publish time is accurate
GOOD RESULT PROBLEM DATE = content is relevant and publish time is up to 1 month wrong
GOOD RESULT BAD DATE = content is relevent and publish time is 1-3 months wrong
CLOSE RESULT = content is close but not exact and date is accurate
CLOSE RESULT PROBLEM DATE = content is close and publish time is up to 1 month wrong
CLOSE RESULT BAD DATE = content is close and publish time is 1-3 months wrong
WRONG RESULT = content is not relevant or publish time is more than 3 months wrong

## Packaging -> Packaging Boxes, IN

None of the 3 are amazing, but at least Syracuse doesn't have very bad results in. Perplexity and Linkup both have lots of bad results.

### Perplexity
Board Converting News - 2025-12-15 00:00:00+00:00 
https://boardconvertingnews.com/kelly-box-celebrates-70-years-of-packaging-excellence/ <- GOOD RESULT BAD DATE, date = Oct 10, 2025

EFP, LLC - 2025-11-20 00:00:00+00:00 
https://www.efppackaging.com <- WRONG RESULT, just landing page, not a story

Graphic Packaging International - 2025-11-05 00:00:00+00:00 
https://www.graphicpkg.com <- WRONG RESULT, just landing page, not a story

Marion Paper Box Company - 2025-10-15 00:00:00+00:00 
https://marionpaperboxco.com/about/ <- WRONG RESULT, just landing page, not a story

_I suspect that Perplexity is interpreting "IN" as the US state of Indiana, not as the country of India. Next time I'll test with full country names. But even if you're charitable and allow Indiana results, this is still a poor set of results._

### Syracuse
mint - 2025-12-18 10:39:09+00:00  - CorporateFinanceActivity
https://www.livemint.com/companies/l-catterton-invests-haldirams-snacks-india-11766044962327.html <- CLOSE RESULT - it's about packaged snacks, not packaging itself

News9live - 2025-12-18 07:42:19+00:00  - CorporateFinanceActivity
https://www.news9live.com/business/biz-news/led-by-former-hul-chief-l-catterton-acquires-stake-in-snacks-major-haldiram-2913015 <- CLOSE RESULT - it's about packaged snacks, not packaging itself


### Linkup

THE PACKMAN - 2026-01-03 00:00:00+00:00 
https://thepackman.in/packaging-innovations-empack-2026-sees-surge-in-visitor-demand/ <- GOOD RESULT PROBLEM DATE, real date is December 18, 2025

7knetwork - 2026-01-02 00:00:00+00:00 
https://7knetwork.com/packaging-companies-in-india/ <- GOOD RESULT PROBLEM DATE, real date is December 17, 2025

PrintWeekIndia - 2026-01-01 00:00:00+00:00 
https://www.printweek.in/features/why-pamex-2026-matters-now-61460 <- GOOD RESULT (but real date is 02 Jan 2026)

Packaging Gateway - 2025-12-30 00:00:00+00:00 
https://www.packaging-gateway.com/features/major-packaging-stories-of-2025-with-big-impact-on-2026/ <- GOOD RESULTS (but date shown now is January 5, 2026)>

Hindustan Times - 2025-12-28 00:00:00+00:00 
https://www.hindustantimes.com/ht-insight/climate-change/revolutionising-india-s-packaging-industry-101738328612786.html <- WRONG RESULT, real date is Jan 31, 2025 06:43 pm IST

Packaging Gateway - 2025-12-20 00:00:00+00:00 
https://www.packaging-gateway.com/features/future-packaging-industry-in-india/ <- WRONG RESULT, real date is April 18, 2019

IBEF - 2025-12-15 00:00:00+00:00 
https://www.ibef.org/blogs/the-future-of-packaging-india-s-role-in-global-paper-packaging-trends <- WRONG RESULT, real date is Mar 07, 2025, 10:35

IBEF - 2025-12-10 00:00:00+00:00 
https://www.ibef.org/industry/paper-packaging <- GOOD RESULT PROBLEM DATE, real date is Oct, 2025

Invest India - 2025-12-05 00:00:00+00:00 
https://www.investindia.gov.in/team-india-blogs/indian-packaging-sector-outlook-industry <- WRONG RESULT, real date is October 18, 2021

Technavio - 2025-11-25 00:00:00+00:00 
https://www.technavio.com/report/flexible-packaging-market-in-india-industry-analysis <- WRONG RESULT, real date is Jan 2025


## Road Freight, Europe

Most of the Perplexity results are dated 2026-01-06 18:49:00 - this suggests a problem handling the data returned by Perplexity. Has a fair amount of good content in.

Linkup has two good quality articles but with some errors in the dates.

Syracuse has some duplicates, some generic freight results, and some articles about drones/air freight which are wrong

### Perplexity
Adexin - 2026-01-06 18:49:00+00:00 
https://adexin.com/blog/logistics-companies-147/ <- CLOSE RESULT BAD DATE, real date is Nov 12, 2025, but if date was correct this would be an OK result - it's about global logistics, not Europe

UK Startup Blog - 2026-01-06 18:49:00+00:00 
https://directory.ukstartupblog.co.uk/top-10-uk-haulage-companies/ <- CLOSE RESULT BAD DATE, real date is Nov 28, 2025, it's a top 10 list of suppliers, not a news story

Vizion API - 2026-01-06 18:49:00+00:00 
https://www.vizionapi.com/blog/global-container-trade-2025-performance-review-and-2026-forecasts <- CLOSE RESULT BAD DATE - it's about global container trade and date is November 25, 2025

IBISWorld - 2026-01-06 18:49:00+00:00 
https://www.ibisworld.com/europe/industry/freight-forwarding-customs-agents/200619/ <- GOOD RESULT BAD DATE - real date is November 2025

Röhlig Logistics - 2026-01-06 18:49:00+00:00 
https://www.rohlig.com/offices/europe/ <- WRONG RESULT - it's just a company info page 

Logistics Business - 2026-01-06 18:49:00+00:00 
https://www.logisticsbusiness.com/jobs-training/europes-driver-shortage-demands-a-long-term-strategy/ <- GOOD RESULT BAD DATE - date is November 13, 2025

3P Logistics - 2026-01-06 18:49:00+00:00 
https://www.3plogistics.com/3pl-market-info-resources/3pl-market-information/aas-top-25-global-freight-forwarders-list/ <- WRONG RESULT - it's just a company list and date is October 9, 2025

Statista - 2026-01-06 18:49:00+00:00 
https://www.statista.com/statistics/640120/top-25-logistics-companies-europe/ <- WRONG RESULT - just list of top companies (and BAD DATE, real date is  Nov 29, 2025)

Panteia - 2026-01-06 18:49:00+00:00 
https://panteia.com/updates/news/road-transport-costs-in-the-netherlands-to-rise-in-2026-introduction-of-truck-toll-to-cause-further-increase-mid-2026 <- GOOD RESULT PROBLEM DATE (there is no date provided)>

Upply - 2026-01-06 18:49:00+00:00 
https://market-insights.upply.com/en/road-transport-analysis-of-the-european-top-10-in-2024 <- GOOD RESULT BAD DATE, real updated date is  05/11/2025 (5th nov)

Axell Group - 2026-01-06 18:49:00+00:00 
https://axell-group.com/en/news/truck-driving-bans-during-christmas-and-new-year-2025-2026/ <- GOOD RESULT PROBLEM DATE, real date is 19 Dec 2025>

Dachser - 2026-01-06 18:49:00+00:00 
https://www.dachser.com/en/ <- WRONG RESULT

Upply - 2026-01-06 18:49:00+00:00 
https://market-insights.upply.com/en <- WRONG RESULT (list of pages, though possibly it meant https://market-insights.upply.com/en/france-road-transport-prices-remain-stagnant-in-november)

CEVA Logistics - 2026-01-06 18:49:00+00:00 
https://www.cevalogistics.com/en <- WRONG RESULT

Avenga - 2026-01-06 18:49:00+00:00 
https://www.avenga.com/magazine/major-transportation-industry-trends/ <- CLOSE RESULT PROBLEM DATE, real date December 8, 2025

ACEA - 2025-12-22 00:00:00+00:00 
https://www.acea.auto/news/demand-side-measures-seen-as-an-important-lever-to-scale-europes-zero-emission-truck-market-new-study-finds/ <- GOOD RESULT

Ritra Cargo - 2025-10-30 00:00:00+00:00 
https://ritra.nl/en/forecasts-for-road-transport-in-2026/ <- GOOD RESULT


### Syracuse
GlobeNewswire News Room - 2026-01-05 00:00:00+00:00  - CorporateFinanceActivity
https://www.globenewswire.com/news-release/2026/01/05/3212446/0/en/TonnerDrones-reiterates-press-release-dated-December-31-2025.html <- WRONG RESULT (it's about drones)

GlobeNewswire News Room - 2025-12-31 00:00:00+00:00  - CorporateFinanceActivity
https://www.globenewswire.com/news-release/2025/12/31/3211692/0/en/Tonner-Drones-to-Receive-1-25M-from-the-Sale-of-Part-of-its-Shareholding-in-Donecle.html <- WRONG RESULT (it's about drones)

PR Newswire UK - 2025-12-29 14:22:00+00:00  - PartnershipActivity
https://www.prnewswire.co.uk/news-releases/europi-property-group-and-incus-capital-form-strategic-joint-venture-to-create-a-leading-iberian-logistics-platform-302650178.html <- CLOSE RSULT (about logistics in general)

PR Newswire - 2025-12-29 14:22:00+00:00  - PartnershipActivity
https://www.prnewswire.com/news-releases/europi-property-group-and-incus-capital-form-strategic-joint-venture-to-create-a-leading-iberian-logistics-platform-302650178.html <- DUPLICATE 

Cision PR Newswire - 2025-12-17 13:30:00+00:00  - RoleActivity
https://www.prnewswire.com/news-releases/freightos-announces-ceo-succession-process-302644713.html <- CLOSE RESULT (about freight)

PR Newswire - 2025-12-17 13:30:00+00:00  - RoleActivity
https://www.prnewswire.com/il/news-releases/freightos-announces-ceo-succession-process-302644713.html <- CLOSE RESULT (about freight)>

AviTrader - 2025-12-16 10:28:21+00:00  - PartnershipActivity
https://avitrader.com/2025/12/16/kuehnenagel-and-swiss-deepen-sustainable-aviation-partnership/ <- WRONG RESULT (air freight)

PR Newswire UK - 2025-12-15 11:58:00+00:00  - CorporateFinanceActivity
https://www.prnewswire.co.uk/news-releases/einride-and-legato-merger-corp-iii-announce-confidential-submission-of-draft-registration-statement-on-form-f-4-302642191.html <- CLOSE RESULT (freight in general)

PR Newswire - 2025-12-15 11:58:00+00:00  - CorporateFinanceActivity
https://www.prnewswire.com/news-releases/einride-and-legato-merger-corp-iii-announce-confidential-submission-of-draft-registration-statement-on-form-f-4-302642191.html <- DUPLICATE

Cision PR Newswire - 2025-12-15 11:54:00+00:00  - CorporateFinanceActivity
https://www.prnewswire.com/news-releases/einride-and-legato-merger-corp-iii-announce-confidential-submission-of-draft-registration-statement-on-form-f-4-302642187.html <- DUPLICATE

PR Newswire UK - 2025-12-10 11:59:00+00:00  - PartnershipActivity
https://www.prnewswire.co.uk/news-releases/einride-and-ionq-partnership-uses-quantum-computing-to-optimize-the-logistics-of-electric-and-autonomous-freight-302637859.html <- GOOD RESULT

PR Newswire - 2025-12-10 11:59:00+00:00  - PartnershipActivity
https://www.prnewswire.com/news-releases/einride-and-ionq-partnership-uses-quantum-computing-to-optimize-the-logistics-of-electric-and-autonomous-freight-302637859.html <- DUPLICATE

Cision PR Newswire - 2025-12-10 11:57:00+00:00  - PartnershipActivity
https://www.prnewswire.com/news-releases/einride-and-ionq-partnership-uses-quantum-computing-to-optimize-the-logistics-of-electric-and-autonomous-freight-302637855.html <- DUPLICATE


### Linkup
CtrlChain - 2025-12-10 00:00:00+00:00 
https://ctrlchain.com/en/blogs/top-5-european-transport-and-logistics-trends-to-watch-in-2026 <- GOOD RESULT BAD DATE, date should be 27 Nov 25

Upply Market Insights - 2025-11-30 00:00:00+00:00 
https://market-insights.upply.com/en/2025-review-of-road-transport-in-europe <- GOOD RESULT BAD DATE, date should be 11/12/2025
(i.e. 11 December)


## Husky Technologies

Perplexity stories are all about the Husky Technologies/CompoSecure M&A. This happpened on 2025-11-03 so I'll assume that any problem dates that appear after 3rd Nov are because the underlying article was updated after the initial news.

LinkUp introduces some new stories, but has two articles that are from Jan and March 2025.

Syracuse only covers the M&A activity, but doesn't include any wrong stories.

### Perplexity 

Investing.com - 2025-12-01 00:00:00+00:00 
https://www.investing.com/news/company-news/composecure-stockholders-approve-husky-technologies-merger-93CH-4422534 <- GOOD RESULT PROBLEM DATE, date should be 12/24/2025, 07:37 AM

Husky Technologies - 2025-11-03 00:00:00+00:00 
https://www.husky.co/en/about-us/news/composecure-announces-business-combination-with-husky-technologies/ <- GOOD RESULT

EcoPlastics in Packaging - 2025-11-03 00:00:00+00:00 
https://ecoplasticsinpackaging.com/mergers-acquisitions/composecure-to-acquire-husky-technologies-in-5bn-deal/ <- GOOD RESULT PROBLEM DATE, date should be November 7, 2025

Platinum Equity - 2025-11-03 00:00:00+00:00 
https://www.platinumequity.com/news/composecure-announces-business-combination-with-husky-technologies/ <- GOOD RESULT

Recycling Today - 2025-11-03 00:00:00+00:00 
https://www.recyclingtoday.com/news/composecure-to-acquire-husky-technologies-in-5-billion-dollar-transaction/ <- GOOD RESULT

Latham & Watkins LLP - 2025-11-03 00:00:00+00:00 
https://www.lw.com/en/news/2025/11/latham-advises-husky-technologies-on-business-combination-with-composecure <- CLOSE RESULT (it's the same story as above but from point of view of the legal adviser, so not relevant to Husky Technologies the company)

Plastics Technology - 2025-11-03 00:00:00+00:00 
https://www.ptonline.com/news/husky-combines-with-composecure-in-5-billion-deal- <- GOOD RESULT

S&P Global Ratings - 2025-11-03 00:00:00+00:00 
https://www.spglobal.com/ratings/en/regulatory/article/-/view/type/HTML/id/3480140 <- GOOD RESULT

### Syracuse

Finimize - 2025-11-03 19:19:14.532344+00:00  - CorporateFinanceActivity
https://finimize.com/content/biotech-deals-and-breakthroughs-spark-heavy-trading-across-markets <- GOOD RESULT

GlobeNewswire News Room - 2025-11-03 00:00:00+00:00  - CorporateFinanceActivity
https://www.globenewswire.com/news-release/2025/11/03/3178950/0/en/CompoSecure-Reports-Strong-3Q25-Financial-Results-and-Announces-Business-Combination-with-Husky-Technologies.html <- GOOD RESULT


### Linkup

Medical Device & Diagnostic Industry (MD+DI) - 2026-03-18 00:00:00+00:00 
https://www.mddionline.com/design-engineering/husky-technologies-expands-multi-material-injection-molding-capabilities-with-acquisition <- WRONG RESULT, date should be March 16, 2025

Husky Technologies - 2026-02-05 00:00:00+00:00 
https://www.husky.co/en/resources/blog/plastindia2026/ <- GOOD RESULT BAD DATE, date should be December 16, 2025

Investing.com - 2025-12-03 00:00:00+00:00 
https://www.investing.com/news/company-news/composecure-stockholders-approve-husky-technologies-merger-93CH-4422534 <- GOOD RESULT PROBLEM DATE, should be 12/24/2025, 07:37 AM

Recycling Today - 2025-11-03 00:00:00+00:00 
https://www.recyclingtoday.com/news/composecure-to-acquire-husky-technologies-in-5-billion-dollar-transaction/ <- GOOD RESULT

Husky Technologies - 2025-11-03 00:00:00+00:00 
https://www.husky.co/en/about-us/news/composecure-announces-business-combination-with-husky-technologies/ <- GOOD RESULT

Plastics Today - 2025-11-03 00:00:00+00:00 
https://www.plasticstoday.com/business/husky-to-merge-with-composecure-in-5-billion-deal <- GOOD RESULT

Plastics Technology - 2025-11-03 00:00:00+00:00 
https://www.ptonline.com/news/husky-combines-with-composecure-in-5-billion-deal- <- GOOD RESULT

citybiz - 2025-11-03 00:00:00+00:00 
https://www.citybiz.co/article/766526/composecure-and-husky-technologies-to-merge/ <- GOOD RESULT

Reuters - 2025-11-03 00:00:00+00:00 
https://www.reuters.com/business/composecure-unveil-5-billion-deal-husky-technologies-wsj-reports-2025-11-03/ <- GOOD RESULT

Plastics News - 2025-10-15 00:00:00+00:00 
https://www.plasticsnews.com/news/husky-wins-innovation-award-industry-40-project/ <- WRONG RESULT, date should be January 10, 2025 02:24 PM EST

